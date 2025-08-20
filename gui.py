import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading


def play_video(canvas, video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    def update_frame():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video when it ends
            ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            canvas.create_image(0, 0, anchor=tk.NW, image=frame)
            canvas.image = frame

        canvas.after(10, update_frame)

    update_frame()


def start_gui():
    root = tk.Tk()
    root.title("Jarvis AI")
    root.geometry("1200x700")  # Adjust size as needed

    canvas = tk.Canvas(root, width=1900, height=850)
    canvas.pack()

    video_path = r"C:\Users\Chandrashekhar B N\Downloads\WhatsApp Video 2025-01-30 at 8.00.50 AM.mp4"
    video_thread = threading.Thread(target=play_video, args=(canvas, video_path), daemon=True)
    video_thread.start()

    root.mainloop()


if __name__ == "__main__":
    start_gui()
