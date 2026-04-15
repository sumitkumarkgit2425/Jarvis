import datetime
import os
from src.utils import get_file_path

ABOUT_FILE = get_file_path("about.txt")

def wish_me():

    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good morning! I am ready for your commands."
    elif 12 <= hour < 18:
        return "Good afternoon! I am ready for your commands."
    else:
        return "Good evening! I am ready for your commands."

def get_identity():

    if not os.path.exists(ABOUT_FILE):
        with open(ABOUT_FILE, "w") as f:
            f.write("I am JARVIS, a native Python voice assistant created for a college lab project by a two-member team.")

    try:
        with open(ABOUT_FILE, "r") as f:
            identity_text = f.read().strip()
        return identity_text
    except Exception as e:
        return "I am JARVIS, your voice assistant."

def get_capabilities():

    capabilities = (
        "I can perform a variety of tasks for you. "
        "I can provide weather updates for any city, "
        "search for information on Wikipedia or Google, "
        "monitor your system's CPU and battery status, "
        "take screenshots, and help you with system power controls like shutdown or restart."
    )
    return capabilities

def process_personalization(query):

    if any(x in query for x in ["what can you do", "capabilities", "features", "what commands"]):
        return get_capabilities()

    elif "who are you" in query:
        return get_identity()

    elif any(x in query for x in ["how are you", "how's it going", "how are you doing", "whatsapp", "what's up"]):
        return "I am functioning at full capacity and ready to assist you. How can I help today?"

    elif any(x in query for x in ["hello", "hellow", "hi", "hey", "wake up", "good morning", "good afternoon", "good evening"]):
        return wish_me()

    return None
