import psutil
import pyautogui
import os
import datetime

SCREENSHOT_DIR = "screenshots"

def monitor_hardware():

    cpu_usage = psutil.cpu_percent(interval=1)
    battery = psutil.sensors_battery()

    hardware_status = f"CPU usage is at {cpu_usage} percent."
    if battery is not None:
        hardware_status += f" Battery is at {battery.percent} percent."
        if battery.power_plugged:
            hardware_status += " The system is currently plugged in."
    return hardware_status

def take_screenshot():

    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")

    try:
        image = pyautogui.screenshot()
        image.save(filename)
        return f"Screenshot saved successfully."
    except Exception as e:
        return "There was an error taking the screenshot."

def process_system(query):

    if "hardware" in query or ("cpu" in query and "battery" in query) or "system status" in query:
        return monitor_hardware()
    elif "screenshot" in query or "capture" in query:
        return take_screenshot()
    return None
