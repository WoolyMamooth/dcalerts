from .messages import MessageHandler
from functools import wraps

def notify(func):
    """
    Decorator that sends a Discord message before and after the function is run.\n
    Include a ***settings*** dict to set messages and url, for example:\n
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

def notify_complex(func):
    """
    Decorator that sends a Discord message before and after the function is run.
    Include a ***settings*** dict to set messages and url.
    Accepts lists and functions as messages, which will be evaluated and sent together as one message.
    You can specify a list item separator as well.
    For example:\n
    settings={\n
        \t"webhook_url" : WEBHOOK_URL,
        \t"message_before" : ["Before", "running", foo()],
        \t"message_after" : ["Results:", foo_results()],
        \t"list_item_sep" : "\\t"
    }\n
    If a message isn't given it will not be sent, so you can notify only after running.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        settings=kwargs.pop("settings")
        message_handler=MessageHandler(settings["webhook_url"])
        list_item_sep=settings.get("list_item_sep", "\n")

        # ------ Before ------ #
        before=settings.get("message_before")
        if before:
            message_handler.send(_make_message(before, list_item_sep=list_item_sep))
        # -------------------- #

        result = func(*args, **kwargs)

        # ------ After ------ #
        after=settings.get("message_after")
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
                item=str(item())
            final_message+=str(item)+list_item_sep
    else:
        final_message+=str(input)

    return final_message