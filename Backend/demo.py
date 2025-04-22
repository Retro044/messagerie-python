import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from register import register
from send_message import send_message
from receive_messages import receive_messages

# Création des utilisateurs
register("alice", "alice@email.com", "mdp123")
register("bob", "bob@email.com", "mdp456")

# Envoi d’un message de Alice à Bob
send_message("alice", "bob", "Salut Bob ! Ce message est chiffré 🔐")

# Bob reçoit et déchiffre ses messages
receive_messages("bob")
