import tkinter as tk
import os
import cv2
from crypto_utils import encrypt_file, decrypt_file  
def play_video(filename="video_message.avi"):
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
    button_play_video = tk.Button(open_conversation, text="📽️ Regarder la vidéo", command=play_video)
    button_play_video.pack()




def open_conversation(contact):
    print(f"ouverture de la conversation avec {contact}")


root = tk.Tk()
root.title("liste des conversations")

contacts = ["alice", "bob", "charlie"]

for contact in contacts:
    frame = tk.Frame(root)
    frame.pack(pady=5)

    label_contact = tk.Label(frame, text=contact)
    label_contact.pack(side=tk.LEFT)

    button_open = tk.Button(frame, text="ouvrir", command=lambda c=contact: open_conversation(c))
    button_open.pack(side=tk.RIGHT)

def play_audio(filename="audio_message.wav"):
    os.system(f"start {filename}")  # Ouvre avec le lecteur par défaut sur Windows

    button_play_audio = tk.Button(open_conversation, text="🎧 Écouter le message audio", command=play_audio)
    button_play_audio.pack()




root.mainloop()