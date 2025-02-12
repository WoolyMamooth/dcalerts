import requests

class MessageHandler:
    """
    This class let's you send messages via a given webhook.
    """
    def __init__(self, webhook_url):
        self.webhook_url=webhook_url

    def send(self, message):
        """
        Send a message to the classes given webhook.
        """
        send_message(webhook_url=self.webhook_url, message=message)

def send_message(webhook_url, message):
    """
    Send a message to a Discord webhook.
    """
    payload = {"content": message}
    requests.post(webhook_url, json=payload)