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

class DcalertsSettings(dict):
    """A dictionary-like class that enforces a required 'webhook' key and allows optional keys with defaults."""

    def __init__(self, webhook, before=None, after=None, separator=" ", send_error=False, error_message="ERROR:"):
        if not webhook:
            raise ValueError("The 'webhook' parameter is required.")

        super().__init__({
            "webhook": webhook,
            "before": before,
            "after": after,
            "separator": separator,
            "send_error": send_error,
            "error_message": error_message
        })

    def __setitem__(self, key, value):
        allowed_keys = {"webhook", "before", "after", "separator", "send_error", "error_message"}
        if key not in allowed_keys:
            raise KeyError(f"Key '{key}' is not allowed. Allowed keys: {allowed_keys}")
        super().__setitem__(key, value)
