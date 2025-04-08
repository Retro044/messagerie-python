from flask import Flask, request, jsonify
import auth
import messaging
from cryptography.fernet import Fernet

app = Flask(__name__)

# Route d'inscription
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    print("REGISTER: Requête reçue avec les données:", data)
    
    if 'username' not in data or 'password' not in data:
        return jsonify({"message": "Nom d'utilisateur ou mot de passe manquant"}), 400
    
    try:
        response = auth.register(data['username'], data['password'])
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": "Erreur pendant l'enregistrement"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print("LOGIN: Tentative de connexion avec les données:", data)
    return jsonify(auth.login(data['username'], data['password']))


KEY = Fernet.generate_key()  # La clé pour chiffrer/déchiffrer les messages

# Envoyer un message
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    print("SEND MESSAGE: Message reçu avec les données:", data)
    try:
        response = messaging.send_message(data['sender'], data['receiver'], data['message'])
        print("SEND MESSAGE: Réponse de l'envoi du message:", response)
        return jsonify({"message": "Message envoyé avec succès"}), 200
    except Exception as e:
        print(f"SEND MESSAGE: Erreur pendant l'envoi du message: {e}")
        return jsonify({"message": "Erreur pendant l'envoi du message"}), 400

# Recevoir les messages
@app.route('/get-messages', methods=['GET'])
def get_messages():
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')
    print(f"GET MESSAGES: Demande reçue pour l'envoi de messages entre {sender} et {receiver}")
    try:
        response = messaging.get_messages(sender, receiver)
        print("GET MESSAGES: Messages récupérés:", response)
        return jsonify(response), 200
    except Exception as e:
        print(f"GET MESSAGES: Erreur pendant la récupération des messages: {e}")
        return jsonify({"message": "Erreur pendant la récupération des messages"}), 400

@app.route('/')
def home():
    print("HOME: La route d'accueil a été appelée")
    return jsonify({"message": "Bienvenue sur l'API de messagerie sécurisée !"})

if __name__ == '__main__':
    app.run(debug=True)
