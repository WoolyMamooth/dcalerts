from .messages import MessageHandler
from functools import wraps

def notify_simple(func):
    """
    Decorator that sends a Discord message before and after the function is run.\n
    Include a ***dcalerts_settings*** dict to set messages and url, for example:\n
    settings={\n
        \t"webhook" : WEBHOOK_URL,
        \t"before" : "Before running",
        \t"after" : "After running"
    }\n
    If a message isn't given it will not be sent, so you can notify only after running.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        settings=kwargs.pop("dcalerts_settings")
        message_handler=MessageHandler(settings["webhook"])
        message_before=settings.get("before")
        message_after=settings.get("after")

        if message_before:
            message_handler.send(message_before)

        result = func(*args, **kwargs)

        if message_after:
            message_handler.send(message_after)

        return result
    
    return wrapper

def notify(func):
    """
    Decorator that sends a Discord message before and after the function is run.
    Include a ***dcalerts_settings*** dict to set messages and url.
    Accepts lists and functions as messages, which will be evaluated and sent together as one message.
    You can specify a list item separator as well.
    For example:\n
    settings={\n
        \t"webhook" : WEBHOOK_URL,
        \t"before" : ["Before", "running", foo()],
        \t"after" : ["Results:", foo_results()],
        \t"list_item_sep" : "\\t"
    }\n
    If a message isn't given it will not be sent, so you can notify only after running.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        settings=kwargs.pop("dcalerts_settings")
        message_handler=MessageHandler(settings["webhook"])
        list_item_sep=settings.get("list_item_sep", "\n")

        # ------ Before ------ #
        before=settings.get("before")
        if before:
            message_handler.send(_make_message(before, list_item_sep=list_item_sep))
        # -------------------- #

        result = func(*args, **kwargs)

        # ------ After ------ #
        after=settings.get("after")
        if after:
            message_handler.send(_make_message(after, list_item_sep=list_item_sep))
        # ------------------- #

        return result
    
    return wrapper

def _make_message(input, list_item_sep="\n"):
    final_message=""
    
    if type(input)==str:
        final_message+=input

    elif callable(input):
        final_message+=str(input())

    elif type(input)==list:
        for item in input:
            if callable(item):
                item=item()
            final_message+=str(item)+list_item_sep
    else:
        final_message+=str(input)

    return final_message