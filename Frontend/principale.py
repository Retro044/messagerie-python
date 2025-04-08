import tkinter as tk
import os
import cv2
import pyaudio
import wave
import numpy as np
import threading
import time
from crypto_utils import encrypt_file, decrypt_file

def send_file(filename):
    encrypt_file(filename)
    print(f"Fichier {filename} chiffré et envoyé")

def receive_file(filename):
    decrypt_file(filename)
    print(f"Fichier {filename} reçu et déchiffré")

def record_audio(filename="audio_message.wav", duration=4):
    # Configuration pour l'enregistrement audio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print(f"Enregistrement audio pendant {duration} secondes...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Enregistrement terminé")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Sauvegarde dans un fichier WAV
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    send_file(filename)

def play_audio(filename="audio_message.wav"):
    # Vérifier si le fichier existe d'abord
    if not os.path.exists(filename):
        print(f"Le fichier {filename} n'existe pas")
        return
        
    # Sur Windows, utiliser le lecteur par défaut
    os.system(f"start {filename}")

def record_video(filename="video_message.avi", duration=4):
    cap = cv2.VideoCapture(0)
    # Définir la résolution
    cap.set(3, 640)
    cap.set(4, 480)
    
    # Définir le codec
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
    
    start_time = time.time()
    print(f"Enregistrement vidéo pendant {duration} secondes...")
    
    while(cap.isOpened() and time.time() - start_time < duration):
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
    
    send_file(filename)

def play_video(filename="video_message.avi"):
    # Vérifier si le fichier existe d'abord
    if not os.path.exists(filename):
        print(f"Le fichier {filename} n'existe pas")
        return
        
    cap = cv2.VideoCapture(filename)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Lecture vidéo", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):  # Arrêter avec "q"
            break
    
    cap.release()
    cv2.destroyAllWindows()

def record_audio_thread():
    threading.Thread(target=record_audio).start()

def record_video_thread():
    threading.Thread(target=record_video).start()

def show_page(page):
    for p in pages.values():
        p.pack_forget()
    page.pack()

def on_register():
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()
    print(f"tentative d'inscription avec : {username} / {email} / {password}")

def send_message():
    message = entry_message.get()
    if message:
        print(f"message envoyé : {message}")
        entry_message.delete(0, tk.END)

root = tk.Tk()
root.title("messagerie sécurisée")

# page de connexion
page_login = tk.Frame(root)
label_login = tk.Label(page_login, text="page de connexion")
label_login.pack()
button_to_register = tk.Button(page_login, text="s'inscrire", command=lambda: show_page(page_register))
button_to_register.pack()
button_to_login = tk.Button(page_login, text="se connecter", command=lambda: show_page(page_main))
button_to_login.pack()

# page d'inscription
page_register = tk.Frame(root)
label_register = tk.Label(page_register, text="page d'inscription")
label_register.pack()

label_username = tk.Label(page_register, text="nom d'utilisateur :")
label_username.pack()
entry_username = tk.Entry(page_register)
entry_username.pack()

label_email = tk.Label(page_register, text="email :")
label_email.pack()
entry_email = tk.Entry(page_register)
entry_email.pack()

label_password = tk.Label(page_register, text="mot de passe :")
label_password.pack()
entry_password = tk.Entry(page_register, show="*")
entry_password.pack()

button_register = tk.Button(page_register, text="s'inscrire", command=on_register)
button_register.pack()
button_to_login = tk.Button(page_register, text="retour", command=lambda: show_page(page_login))
button_to_login.pack()






# page principale (liste des conversations)
page_main = tk.Frame(root)
label_main = tk.Label(page_main, text="liste des conversations")
label_main.pack()
button_to_conversation = tk.Button(page_main, text="ouvrir une conversation", command=lambda: show_page(page_conversation))
button_to_conversation.pack()

# page de conversation
page_conversation = tk.Frame(root)
label_conversation = tk.Label(page_conversation, text="conversation avec alice")
label_conversation.pack()

# Ajout des boutons pour l'audio et la vidéo
frame_media = tk.Frame(page_conversation)
frame_media.pack(pady=10)

button_record_audio = tk.Button(frame_media, text="🎤 Enregistrer audio", command=record_audio_thread)
button_record_audio.pack(side=tk.LEFT, padx=5)

button_play_audio = tk.Button(frame_media, text="🎧 Écouter audio", command=lambda: play_audio())
button_play_audio.pack(side=tk.LEFT, padx=5)

button_record_video = tk.Button(frame_media, text="📹 Enregistrer vidéo", command=record_video_thread)
button_record_video.pack(side=tk.LEFT, padx=5)

button_play_video = tk.Button(frame_media, text="📽️ Voir vidéo", command=lambda: play_video())
button_play_video.pack(side=tk.LEFT, padx=5)

button_to_send_message = tk.Button(page_conversation, text="envoyer un message", command=lambda: show_page(page_send_message))
button_to_send_message.pack()
button_to_main = tk.Button(page_conversation, text="retour", command=lambda: show_page(page_main))
button_to_main.pack()

# page envoyer un message
page_send_message = tk.Frame(root)
label_send_message = tk.Label(page_send_message, text="envoyer un message")
label_send_message.pack()

entry_message = tk.Entry(page_send_message, width=50)
entry_message.pack()

button_send = tk.Button(page_send_message, text="envoyer", command=send_message)
button_send.pack()
button_to_conversation = tk.Button(page_send_message, text="retour", command=lambda: show_page(page_conversation))
button_to_conversation.pack()

# stocker les pages dans un dictionnaire
pages = {
    "login": page_login,
    "register": page_register,
    "main": page_main,
    "conversation": page_conversation,
    "send_message": page_send_message,
}

# afficher la page de connexion au démarrage
show_page(page_login)

root.mainloop()