from cryptography.hazmat.primitives.asymmetric import rsa, padding # type: ignore
from cryptography.hazmat.primitives import serialization, hashes # type: ignore
from cryptography.fernet import Fernet # type: ignore

# Génération d'une clé unique (à faire une seule fois)
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_file(filename):
    with open(filename, "rb") as file:
        data = file.read()
    
    encrypted_data = cipher.encrypt(data)

    with open(filename + ".enc", "wb") as file:
        file.write(encrypted_data)
    print(f"🔒 Fichier chiffré : {filename}.enc")

def decrypt_file(filename):
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    
    decrypted_data = cipher.decrypt(encrypted_data)

    original_filename = filename.replace(".enc", "")
    with open(original_filename, "wb") as file:
        file.write(decrypted_data)
    print(f"🔓 Fichier déchiffré : {original_filename}")
