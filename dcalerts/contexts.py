from .messages import MessageHandler, make_message
from .utils import code_block

class Notifier:
    def __init__(self,dcalerts_settings):
        if "webhook" not in dcalerts_settings:
            raise ValueError("Missing webhook in dcalerts_settings")
        
        self.messagehandler=MessageHandler(dcalerts_settings.get("webhook"))
        self.before=dcalerts_settings.get("before")
        self.after=dcalerts_settings.get("after")
        self.list_item_sep = dcalerts_settings.get("separator", " ")
        self.send_error=dcalerts_settings.get("send_error")
        self.error_message=dcalerts_settings.get("error_message")

    def __enter__(self):
        if self.before:
            self.send(self.before)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None and self.send_error:
            error_message = ["ERROR:" if self.error_message is None else self.error_message, code_block(str(exc_val))]
            self.send(error_message)
            return False
        
        if self.after:
            self.send(self.after)
    
    def send(self,message):
        message=make_message(message, self.list_item_sep)
        self.messagehandler.send(message)