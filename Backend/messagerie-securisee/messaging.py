import db
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

def send_message(data):
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')

    if not sender or not receiver or not message:
        return {"error": "Missing data"}, 400

    conn = db.get_db_connection()
    cursor = conn.cursor()

    # Récupérer la clé publique du destinataire
    cursor.execute("SELECT public_key FROM users WHERE username=%s", (receiver,))
    result = cursor.fetchone()
    if not result:
        return {"error": "Receiver not found"}, 404

    public_key = serialization.load_pem_public_key(result[0].encode())

    # Chiffrer le message
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # Stocker le message
    cursor.execute("INSERT INTO messages (sender, receiver, content) VALUES (%s, %s, %s)",
                   (sender, receiver, encrypted_message))
    conn.commit()

    return {"message": "Message sent successfully"}, 201

def get_messages(sender, receiver):
    conn = db.get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT content FROM messages WHERE sender=%s AND receiver=%s", (sender, receiver))
    messages = cursor.fetchall()

    decrypted_messages = []

    # Charger la clé privée du receiver
    try:
        with open(f"private_keys/{receiver}_private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        return {"error": "Private key not found"}, 500

    # Déchiffrer chaque message
    for (enc_message,) in messages:
        try:
            decrypted = private_key.decrypt(
                enc_message,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            decrypted_messages.append(decrypted.decode())
        except Exception as e:
            decrypted_messages.append("Failed to decrypt")

    return {"messages": decrypted_messages}, 200

# Fonction pour générer une clé de chiffrement (à faire une seule fois et à conserver)
def generate_key():
    return Fernet.generate_key()

# Fonction pour chiffrer un message
def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())  # Chiffre le message
    return encrypted_message

# Fonction pour déchiffrer un message
def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()  # Déchiffre le message
    return decrypted_message