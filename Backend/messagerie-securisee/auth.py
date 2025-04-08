import bcrypt
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import db
import mysql.connector

def register(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"error": "Missing username or password"}, 400

    conn = db.get_db_connection()
    cursor = conn.cursor()

    # Vérifier si l'utilisateur existe déjà
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        return {"error": "Username already exists"}, 409

    # Hash + salage du mot de passe
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Génération des clés
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Sérialisation des clés
    private_bytes = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )
    public_bytes = public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Enregistrer la clé publique et le mot de passe hashé
    cursor.execute("INSERT INTO users (username, password_hash, public_key) VALUES (%s, %s, %s)",
                   (username, hashed, public_bytes.decode()))
    conn.commit()

    # Sauvegarder la clé privée en local (simulateur)
    if not os.path.exists("private_keys"):
        os.makedirs("private_keys")
    with open(f"private_keys/{username}_private_key.pem", "wb") as f:
        f.write(private_bytes)

    return {"message": "User registered successfully"}, 201

def login(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"error": "Missing username or password"}, 400

    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if not user:
        return {"error": "User not found"}, 404

    if not bcrypt.checkpw(password.encode(), user[0].encode()):
        return {"error": "Invalid password"}, 401

    return {"message": "Login successful"}, 200
