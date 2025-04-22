import base64
import sys
import os
import tkinter as tk

from db import db, cursor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def receive_messages(username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        print(f"❌ Utilisateur '{username}' introuvable dans la base de données.")
        return []

    user_id = user[0]

    try:
        with open(f"{username}_private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
    except FileNotFoundError:
        print(f"❌ Clé privée '{username}_private_key.pem' introuvable.")
        return []

    cursor.execute("SELECT sender_id, encrypted_content FROM messages WHERE receiver_id = %s", (user_id,))
    messages = cursor.fetchall()

    if not messages:
        print(f"📩 Aucun message trouvé pour l'utilisateur '{username}'.")
        return []

    messages_recus = []

    for sender_id, encrypted_b64 in messages:
        cursor.execute("SELECT username FROM users WHERE id = %s", (sender_id,))
        sender = cursor.fetchone()
        if not sender:
            print(f"❌ Utilisateur expéditeur (ID: {sender_id}) introuvable.")
            continue  

        sender_name = sender[0]

        encrypted_data = base64.b64decode(encrypted_b64.encode('utf-8'))
        try:
            decrypted = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            messages_recus.append((sender_name, decrypted.decode()))
        except Exception as e:
            print(f"⚠️ Erreur de déchiffrement pour le message de {sender_name} : {e}")

    return messages_recus


