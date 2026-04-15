import pyttsx3
import speech_recognition as sr
import pyaudio
import threading

def speak(text, update_status_cb=None):

    if update_status_cb:
        update_status_cb(f"JARVIS: {text}")
    try:
        engine = pyttsx3.init()

        engine.setProperty('rate', 175)

        voices = engine.getProperty('voices')

        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def listen(update_status_cb=None):

    r = sr.Recognizer()
    with sr.Microphone() as source:
        if update_status_cb:
            update_status_cb("Listening...")

        r.pause_threshold = 1.5
        r.operation_timeout = 15

        r.energy_threshold = 400
        r.dynamic_energy_threshold = True

        if update_status_cb:
            update_status_cb("Listening... SPEAK NOW")

        try:

            audio = r.listen(source, timeout=5)
            if update_status_cb:
                update_status_cb("Analyzing...")
            query = r.recognize_google(audio, language='en-in')
            if update_status_cb:
                update_status_cb(f"You: {query}")
        except sr.WaitTimeoutError:
            return "none"
        except sr.UnknownValueError:
            return "none"
        except sr.RequestError:
            if update_status_cb:
                update_status_cb("Error: Could not request results from service.")
            return "none"
        except Exception as e:
            print(f"Listen Error: {e}")
            return "none"
    return query.lower()

class ManualVoiceRecorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024

    def start_recording(self, update_status_cb=None):
        if self.is_recording:
            return
            
        self.frames = []
        self.is_recording = True
        
        try:
            self.stream = self.p.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
        except Exception as e:
            print(f"Failed to open audio stream: {e}")
            self.is_recording = False
            return
            
        if update_status_cb:
            update_status_cb("Listening... SPEAK NOW")
        
        def record():
            while self.is_recording and self.stream:
                try:
                    data = self.stream.read(self.chunk, exception_on_overflow=False)
                    self.frames.append(data)
                except Exception as e:
                    break
        
        threading.Thread(target=record, daemon=True).start()

    def stop_recording_and_recognize(self, update_status_cb=None):
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
        if not self.frames:
            return "none"
            
        if update_status_cb:
            update_status_cb("Analyzing...")

        raw_data = b''.join(self.frames)
        r = sr.Recognizer()
        audio_data = sr.AudioData(raw_data, self.rate, 2)
        
        try:
            query = r.recognize_google(audio_data, language='en-in')
            if update_status_cb:
                update_status_cb(f"You: {query}")
            return query.lower()
        except sr.UnknownValueError:
            return "none"
        except sr.RequestError:
            if update_status_cb:
                update_status_cb("Error: Could not request results from service.")
            return "none"
        except Exception as e:
            print(f"Listen Error: {e}")
            return "none"
