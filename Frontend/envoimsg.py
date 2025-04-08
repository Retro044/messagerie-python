import tkinter as tk
import pyaudio
import wave
import cv2
import os

def play_audio(filename="audio_message.wav"):
    os.system(f"start {filename}")  # Ouvre avec le lecteur par défaut sur Windows


def send_message():
    message = entry_message.get()
    if message:
        print(f"message envoyé : {message}")
        entry_message.delete(0, tk.END)


root = tk.Tk()
root.title("conversation avec alice")

frame_messages = tk.Frame(root)
frame_messages.pack()

messages = [
    {"sender": "alice", "text": "salut !"},
    {"sender": "moi", "text": "coucou !"},
]

for message in messages:
    label = tk.Label(frame_messages, text=f"{message['sender']}: {message['text']}")
    label.pack(anchor=tk.W if message['sender'] == "alice" else tk.E)

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

entry_message = tk.Entry(frame_input, width=50)
entry_message.pack(side=tk.LEFT)

button_send = tk.Button(frame_input, text="envoyer", command=send_message)
button_send.pack(side=tk.RIGHT)

def record_video(filename="video_message.avi", duration=5):
    cap = cv2.VideoCapture(0)  # 0 = webcam
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    print("🔴 Enregistrement vidéo en cours...")
    frames_count = 0
    while frames_count < duration * 20:  # Enregistre pendant X secondes
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow("Enregistrement...", frame)
            frames_count += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):  # Arrêter avec "q"
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"📹 Vidéo enregistrée : {filename}")

# Test d'enregistrement
record_video()
button_record_video = tk.Button(send_message, text="📹 Enregistrer une vidéo", command=record_video)
button_record_video.pack()


def record_audio(filename="audio_message.wav", duration=5, sample_rate=44100, channels=1):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True, frames_per_buffer=1024)

    frames = []
    print("🔴 Enregistrement en cours...")
    
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("✅ Enregistrement terminé.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))

    print(f"🎤 Message audio enregistré : {filename}")

# Test d'enregistrement
record_audio()

button_record_audio = tk.Button(send_message, text="🎤 Enregistrer un audio", command= record_audio)
button_record_audio.pack()
root.mainloop()