import requests

class MessageHandler:
    """
    This class lets you send messages via the given webhook.
    """
    def __init__(self, webhook_url:str|object):
        if type(webhook_url)==MessageHandler:
            self.webhook_url=webhook_url.webhook_url
        else:
            self.webhook_url=webhook_url

    def send(self, message):
        """
        Send a message to the objects given webhook.
        """
        send_message(webhook_url=self.webhook_url, message=message)

def send_message(webhook_url:str|dict, message:str):
    """
    Send a message to a Discord webhook.
    """
    if( type(webhook_url)== dict):
        webhook_url=webhook_url["webhook_url"]
    payload = {"content": str(message)}
    requests.post(webhook_url, json=payload)

def make_message(input, list_item_sep=" "):
    """
    Converts strings, lists of strings, functions and other inputs into a single string and returns it.
    """
    final_message=""
    
    if type(input)==str:
        final_message+=input

    elif callable(input):
        final_message+=str(input())

    elif type(input)==list:
        for item in input:
            final_message+=make_message(item, list_item_sep=list_item_sep)+list_item_sep
    else:
        final_message+=str(input)

    return final_message