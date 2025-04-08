import requests

BASE_URL = "http://127.0.0.1:5000"

# Inscription d'un utilisateur
def register(username, password):
    print(f"REGISTER: Tentative d'enregistrement de l'utilisateur {username}")
    r = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
    print("REGISTER status code:", r.status_code)
    try:
        print("REGISTER response json:", r.json())
    except ValueError:
        print("REGISTER: La réponse n'est pas au format JSON.")
        print("REGISTER response text:", r.text)

# Connexion d'un utilisateur
def login(username, password):
    print(f"LOGIN: Tentative de connexion de l'utilisateur {username}")
    r = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    print("LOGIN status code:", r.status_code)
    try:
        print("LOGIN response json:", r.json())
    except ValueError:
        print("LOGIN: La réponse n'est pas au format JSON.")
        print("LOGIN response text:", r.text)

# Envoi d'un message
def send_message(sender, receiver, message):
    print(f"SEND MESSAGE: Envoi du message de {sender} à {receiver}")
    r = requests.post(f"{BASE_URL}/send-message", json={"sender": sender, "receiver": receiver, "message": message})
    print("SEND MESSAGE status code:", r.status_code)
    try:
        print("SEND MESSAGE response json:", r.json())
    except ValueError:
        print("SEND MESSAGE: La réponse n'est pas au format JSON.")
        print("SEND MESSAGE response text:", r.text)

# Récupérer les messages
def get_messages(sender, receiver):
    print(f"GET MESSAGES: Récupération des messages entre {sender} et {receiver}")
    r = requests.get(f"{BASE_URL}/get-messages", params={"sender": sender, "receiver": receiver})
    print("GET MESSAGES status code:", r.status_code)
    try:
        print("GET MESSAGES response json:", r.json())
    except ValueError:
        print("GET MESSAGES: La réponse n'est pas au format JSON.")
        print("GET MESSAGES response text:", r.text)

# Test complet
register("bob", "password123")
login("bob", "password123")
send_message("bob", "alice", "Hello Alice!")
get_messages("bob", "alice")
