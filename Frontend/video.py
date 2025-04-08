import cv2

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
