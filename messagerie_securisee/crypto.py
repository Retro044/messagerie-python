from Crypto.PublicKey import RSA

#Fonction pour générer une paire de clés RSA (privée et publique)
def generate_keys():
    key = RSA.generate(2048)  # Clé de 2048 bits pour plus de sécurité
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

#Générer les clés
private_key, public_key = generate_keys()

#Sauvegarder les clés dans des fichiers
with open("private.pem", "wb") as private_file:
    private_file.write(private_key)

with open("public.pem", "wb") as public_file:
    public_file.write(public_key)

print("Clés RSA générées et sauvegardées.")

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

#Charger la clé publique depuis le fichier
with open("public.pem", "rb") as public_file:
    public_key = RSA.import_key(public_file.read())

#Créer un objet de chiffrement avec la clé publique
cipher_rsa = PKCS1_OAEP.new(public_key)

#Message à chiffrer
message = "Ceci est un message secret."

#Chiffrer le message
encrypted_message = cipher_rsa.encrypt(message.encode())

#Afficher le message chiffré
print("Message chiffré :", encrypted_message)

#Charger la clé privée depuis le fichier
with open("private.pem", "rb") as private_file:
    private_key = RSA.import_key(private_file.read())

#Créer un objet de déchiffrement avec la clé privée
cipher_rsa_private = PKCS1_OAEP.new(private_key)

#Déchiffrer le message
decrypted_message = cipher_rsa_private.decrypt(encrypted_message)

#Afficher le message déchiffré
print("Message déchiffré :", decrypted_message.decode())