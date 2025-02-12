import requests

class MessageHandler:
    """
    This class lets you send messages via the given webhook.
    """
    def __init__(self, webhook_url:str):
        self.webhook_url=webhook_url

    def send(self, message):
        """
        Send a message to the objects given webhook.
        """
        send_message(webhook_url=self.webhook_url, message=message)

def send_message(webhook_url:str, message:str):
    """
    Send a message to a Discord webhook.
    """
    payload = {"content": message}
    requests.post(webhook_url, json=payload)