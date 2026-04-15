import os
import time

def confirm_power_action(action, voice_listen_func, speak_func, update_status_cb):

    prompt = f"Are you sure you want to {action} the system? Please say yes or no."
    speak_func(prompt, update_status_cb)

    confirmation = voice_listen_func(update_status_cb)

    if confirmation and "yes" in confirmation:
        speak_func(f"Executing system {action}.", update_status_cb)
        time.sleep(1)
        if action == "shutdown":
            if os.name == 'nt':
                os.system("shutdown /s /t 1")
            else:
                os.system("shutdown -h now")
        elif action == "restart":
            if os.name == 'nt':
                os.system("shutdown /r /t 1")
            else:
                os.system("reboot")
        return f"System {action} initiated."
    else:
        return f"System {action} cancelled."

def process_power(query, voice_listen_func, speak_func, update_status_cb):

    if "shutdown" in query:
        return confirm_power_action("shutdown", voice_listen_func, speak_func, update_status_cb)
    elif "restart" in query:
        return confirm_power_action("restart", voice_listen_func, speak_func, update_status_cb)
    return None
