from db import db, cursor
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def send_message(sender_username, receiver_username, message):
    # 1️⃣ Récupération des ID et de la clé publique
    cursor.execute("SELECT id FROM users WHERE username = %s", (sender_username,))
    sender = cursor.fetchone()
    cursor.execute("SELECT id, public_key FROM users WHERE username = %s", (receiver_username,))
    receiver = cursor.fetchone()

    if not sender or not receiver:
        print("❌ Utilisateur expéditeur ou destinataire introuvable.")
        return

    sender_id = sender[0]
    receiver_id = receiver[0]
    public_key_pem = receiver[1].encode('utf-8')

    # 2️⃣ Importer la clé publique
    public_key = serialization.load_pem_public_key(public_key_pem)

    # 3️⃣ Chiffrement du message
    encrypted = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 4️⃣ Encodage base64 pour stocker en texte
    encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')

    # 5️⃣ Insertion dans la base
    cursor.execute(
        "INSERT INTO messages (sender_id, receiver_id, encrypted_content) VALUES (%s, %s, %s)",
        (sender_id, receiver_id, encrypted_b64)
    )
    db.commit()

    print("✅ Message envoyé et chiffré avec succès.")
