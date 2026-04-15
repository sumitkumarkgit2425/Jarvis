import customtkinter as ctk
import threading
import time
import tkinter as tk

from src.speech_engine import speak, listen, ManualVoiceRecorder
from src.features.personalization import process_personalization, wish_me
from src.features.memory import process_memory
from src.features.knowledge import process_knowledge
from src.features.weather import process_weather
from src.features.system_utils import process_system
from src.features.power_control import process_power

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JARVIS - Voice Assistant")
        self.geometry("600x500")
        self.resizable(False, False)

        self.is_listening = False
        self.pulse_radius = 50
        self.pulse_growing = True
        self.recorder = ManualVoiceRecorder()

        self.create_widgets()
        self.after(500, self.startup_greeting)
        self.after(50, self.animate_pulse)

    def create_widgets(self):

        self.title_label = ctk.CTkLabel(self, text="J.A.R.V.I.S", font=("Roboto", 40, "bold"))
        self.title_label.pack(pady=15)

        self.status_label = ctk.CTkLabel(self, text="Initializing...", font=("Roboto", 16), text_color="gray")
        self.status_label.pack(pady=5)

        self.history_box = ctk.CTkTextbox(self, width=480, height=140, font=("Roboto", 14), state="disabled", wrap="word")
        self.history_box.pack(pady=5)

        self.canvas = tk.Canvas(self, width=150, height=150, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.circle = self.canvas.create_oval(
            75-self.pulse_radius, 75-self.pulse_radius,
            75+self.pulse_radius, 75+self.pulse_radius,
            fill="#1f538d", outline="#14375e"
        )

        self.listen_btn = ctk.CTkButton(self, text="Start Listening", command=self.toggle_listen, font=("Roboto", 16))
        self.listen_btn.pack(pady=10)

    def log_status(self, message):

        def update_gui():
            if message.startswith("JARVIS:") or message.startswith("You:"):

                self.history_box.configure(state="normal")
                self.history_box.insert("end", message + "\n\n")
                self.history_box.see("end")
                self.history_box.configure(state="disabled")
                self.status_label.configure(text="Idle")
            else:
                self.status_label.configure(text=message)
        self.after(0, update_gui)

    def animate_pulse(self):

        if self.is_listening:
            if self.pulse_growing:
                self.pulse_radius += 2
                if self.pulse_radius >= 70:
                    self.pulse_growing = False
            else:
                self.pulse_radius -= 2
                if self.pulse_radius <= 50:
                    self.pulse_growing = True

            pulse_color = "#2ecc71" if self.is_listening else "#1f538d"
            outline_color = "#27ae60" if self.is_listening else "#14375e"

            self.canvas.itemconfig(self.circle, fill=pulse_color, outline=outline_color)
            self.canvas.coords(self.circle, 75-self.pulse_radius, 75-self.pulse_radius, 75+self.pulse_radius, 75+self.pulse_radius)
        else:

            self.canvas.itemconfig(self.circle, fill="#1f538d", outline="#14375e")
            if self.pulse_radius > 50:
                self.pulse_radius -= 3
                self.canvas.coords(self.circle, 75-self.pulse_radius, 75-self.pulse_radius, 75+self.pulse_radius, 75+self.pulse_radius)

        self.after(30, self.animate_pulse)

    def startup_greeting(self):

        def greet():
            greeting = wish_me()
            speak(greeting, self.log_status)
            self.log_status("Idle. Press 'Start Listening'.")
        threading.Thread(target=greet, daemon=True).start()

    def toggle_listen(self):

        if not self.is_listening:
            self.is_listening = True
            self.listen_btn.configure(text="Stop Listening")
            self.recorder.start_recording(self.log_status)
        else:
            self.stop_listen()

    def stop_listen(self):

        if self.is_listening:
            self.is_listening = False
            self.listen_btn.configure(text="Start Listening")
            
            def finish_and_process():
                query = self.recorder.stop_recording_and_recognize(self.log_status)
                if query and query != "none":
                    self.process_query(query)
                else:
                    self.log_status("JARVIS: I didn't quite catch a valid command.")
                    
            threading.Thread(target=finish_and_process, daemon=True).start()

    def process_query(self, query):
        print(f"DEBUG: Processing query: {query}")
        response = process_personalization(query)
        
        if not response: response = process_memory(query)

        if not response: response = process_knowledge(query)

        if not response: response = process_weather(query)

        if not response: response = process_system(query)

        if not response:

            response = process_power(query, lambda cb=self.log_status: listen(cb), speak, self.log_status)

        if response:
            speak(response, self.log_status)
        else:
            if "stop" in query or "exit" in query or "quit" in query:
                speak("Goodbye!", self.log_status)
                self.is_listening = False
                self.after(1000, self.destroy)
            else:

                self.log_status("JARVIS: I didn't quite catch a valid command.")

if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()
