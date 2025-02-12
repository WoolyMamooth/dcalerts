import requests
import time
from functools import wraps

class MessageHandler:
    def __init__(self, webhook_url):
        self.webhook_url=webhook_url

    def send(self, message):
        """
        Send a message to a Discord webhook.
        """
        payload = {"content": message}
        requests.post(self.webhook_url, json=payload)

def create_timer(seconds_from_now):
    """
    Returns a string which Discord reads as a timer to a given second. You can include this in the settings dict of notify:\n
    settings={\n
        \tmessage_before="Time until completion: "+create_timer(42)\n
    }
    """
    return "<t:"+str(int(time.time()+seconds_from_now))+":R>"

def notify(func):
    """
    Decorator that sends a Discord message before and after the function is run.\n
    Include a settings dict to set messages and url, for example:\n
    settings={\n
        \t"webhook_url" : WEBHOOK_URL,
        \t"message_before" : "Before running",
        \t"message_after" : "After running"
    }\n
    If a message isn't given it will not be sent, so you can notify only after running.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        settings=kwargs.pop("settings")
        message_handler=MessageHandler(settings["webhook_url"])
        message_before=settings.get("message_before")
        message_after=settings.get("message_after")

        if message_before:
            message_handler.send(message_before)

        result = func(*args, **kwargs)

        if message_after:
            message_handler.send(message_after)

        return result
    
    return wrapper