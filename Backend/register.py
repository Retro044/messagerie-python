import bcrypt
from db import db, cursor
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

#  Inscription utilisateur
def register(username, email, password):
    # Hachage + salage du mot de passe
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    # Génération des clés RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    #  Vérification que le username ou l'email n'existent pas déjà
    cursor.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
    if cursor.fetchone():
        print("XXX Ce nom d'utilisateur ou cet email existe déjà.")
        return

    # Enregistrement dans la BDD
    cursor.execute("INSERT INTO users (username, email, password_hash, public_key) VALUES (%s, %s, %s, %s)",
                   (username, email, hashed_password, public_pem.decode('utf-8')))
    db.commit()

    # Sauvegarde locale de la clé privée (simulation d'une machine client)
    with open(f"{username}_private_key.pem", "wb") as f:
        f.write(private_pem)

    print(" Utilisateur enregistré avec succès et clés générées.")
