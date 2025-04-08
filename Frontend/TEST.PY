import tkinter as tk
import os
import cv2
import pyaudio
import wave
import threading
import time
from tkinter import PhotoImage
from tkinter import ttk

# Créer un style personnalisé



def enregistrer_audio(nom_fichier="message_audio.wav", duree=4):
    # Configuration pour l'enregistrement audio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CANAUX = 1
    TAUX = 44100
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CANAUX,
                    rate=TAUX,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print(f"Enregistrement audio pendant {duree} secondes...")
    frames = []
    
    for i in range(0, int(TAUX / CHUNK * duree)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Enregistrement terminé")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Sauvegarde dans un fichier WAV
    wf = wave.open(nom_fichier, 'wb')
    wf.setnchannels(CANAUX)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(TAUX)
    wf.writeframes(b''.join(frames))
    wf.close()

def jouer_audio(nom_fichier="message_audio.wav"):
    # Vérifier si le fichier existe d'abord
    if not os.path.exists(nom_fichier):
        print(f"Le fichier {nom_fichier} n'existe pas")
        return
        
    # Sur Windows, utiliser le lecteur par défaut
    os.system(f"start {nom_fichier}")

def enregistrer_video(nom_fichier="message_video.avi", duree=5):
    cap = cv2.VideoCapture(0)
    # Définir la résolution
    cap.set(3, 640)
    cap.set(4, 480)
    
    # Définir le codec
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(nom_fichier, fourcc, 20.0, (640, 480))
    
    start_time = time.time()
    print(f"Enregistrement vidéo pendant {duree} secondes...")
    
    while(cap.isOpened() and time.time() - start_time < duree):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Enregistrement vidéo', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Enregistrement terminé")

def jouer_video(nom_fichier="message_video.avi"):
    # Vérifier si le fichier existe d'abord
    if not os.path.exists(nom_fichier):
        print(f"Le fichier {nom_fichier} n'existe pas")
        return
        
    cap = cv2.VideoCapture(nom_fichier)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Lecture vidéo", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):  # Arrêter avec "q"
            break
    
    cap.release()
    cv2.destroyAllWindows()

def enregistrer_audio_thread():
    threading.Thread(target=enregistrer_audio).start()

def enregistrer_video_thread():
    threading.Thread(target=enregistrer_video).start()

def afficher_page(page):
    for p in pages.values():
        p.pack_forget()
    page.pack()

def on_inscription():
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()
    print(f"Tentative d'inscription avec : {username} / {email} / {password}")

def envoyer_message():
    message = entry_message.get()
    if message:
        print(f"Message envoyé : {message}")
        entry_message.delete(0, tk.END)

root = tk.Tk()
root.title("Messagerie sécurisée")

# Page de connexion
page_login = tk.Frame(root)
label_login = tk.Label(page_login, text="Page de connexion")
label_login.pack()
button_to_register = tk.Button(page_login, text="S'inscrire", command=lambda: afficher_page(page_register))
button_to_register.pack()
button_to_main = tk.Button(page_login, text="Se connecter", command=lambda: afficher_page(page_main))
button_to_main.pack()

# Page d'inscription
page_register = tk.Frame(root)
label_register = tk.Label(page_register, text="Page d'inscription")
label_register.pack()

label_username = tk.Label(page_register, text="Nom d'utilisateur :")
label_username.pack()
entry_username = tk.Entry(page_register)
entry_username.pack()

label_email = tk.Label(page_register, text="Email :")
label_email.pack()
entry_email = tk.Entry(page_register)
entry_email.pack()

label_password = tk.Label(page_register, text="Mot de passe :")
label_password.pack()
entry_password = tk.Entry(page_register, show="*")
entry_password.pack()

button_register = tk.Button(page_register, text="S'inscrire", command=on_inscription)
button_register.pack()
button_to_login = tk.Button(page_register, text="Retour", command=lambda: afficher_page(page_login))
button_to_login.pack()

# Page principale (liste des conversations)
page_main = tk.Frame(root)
label_main = tk.Label(page_main, text="Liste des conversations")
label_main.pack()
button_to_conversation = tk.Button(page_main, text="Ouvrir une conversation", command=lambda: afficher_page(page_conversation))
button_to_conversation.pack()

# Page de conversation
page_conversation = tk.Frame(root)
label_conversation = tk.Label(page_conversation, text="Conversation avec Alice")
label_conversation.pack()

# Ajout des boutons pour l'audio et la vidéo
frame_media = tk.Frame(page_conversation)
frame_media.pack(pady=10)

button_record_audio = tk.Button(frame_media, text="🎤 Enregistrer audio", command=enregistrer_audio_thread)
button_record_audio.pack(side=tk.LEFT, padx=5)

button_play_audio = tk.Button(frame_media, text="🎧 Écouter audio", command=lambda: jouer_audio())
button_play_audio.pack(side=tk.LEFT, padx=5)

button_record_video = tk.Button(frame_media, text="📹 Enregistrer vidéo", command=enregistrer_video_thread)
button_record_video.pack(side=tk.LEFT, padx=5)

button_play_video = tk.Button(frame_media, text="📽️ Voir vidéo", command=lambda: jouer_video())
button_play_video.pack(side=tk.LEFT, padx=5)

button_to_send_message = tk.Button(page_conversation, text="Envoyer un message", command=lambda: afficher_page(page_send_message))
button_to_send_message.pack()
button_to_main = tk.Button(page_conversation, text="Retour", command=lambda: afficher_page(page_main))
button_to_main.pack()


# Page envoyer un message
page_send_message = tk.Frame(root)
label_send_message = tk.Label(page_send_message, text="Envoyer un message")
label_send_message.pack()

entry_message = tk.Entry(page_send_message, width=50)
entry_message.pack()

button_send = tk.Button(page_send_message, text="Envoyer", command=envoyer_message)
button_send.pack()
button_to_conversation = tk.Button(page_send_message, text="Retour", command=lambda: afficher_page(page_conversation))
button_to_conversation.pack()
style = ttk.Style()
style.configure("TButton", foreground="red", background="yellow", font=("Helvetica", 12))


pages = {
    "login": page_login,
    "register": page_register,
    "main": page_main,
    "conversation": page_conversation,
    "send_message": page_send_message,
}

# Afficher la page de connexion au démarrage
afficher_page(page_login)

root.mainloop()