import bcrypt
from db import db, cursor 
def login(username, password):
    cursor.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result:
        stored_hash = result[0].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            print(" Authentification réussie !")
        else:
            print(" Mot de passe incorrect.")
    else:
        print(" Utilisateur non trouvé.")
        return False