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

def notify_extended(func):
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
        \t"separator" : "\\t"
    }\n
    If a message isn't given it will not be sent, so you can notify only after running.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        settings=kwargs.pop("dcalerts_settings")
        message_handler=MessageHandler(settings["webhook"])
        list_item_sep=settings.get("separator", "\n")

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

def notify(func=None, dcalerts_settings=None):
    """
    Decorator that sends a Discord message before and after the function is run.
    Include a ***dcalerts_settings*** dict to set messages and url.
    Accepts lists and functions as messages, which will be evaluated and sent together as one message.
    You can specify a list item separator and send error messages as well.
    For example:\n
    settings={\n
        \t"webhook" : WEBHOOK_URL,
        \t"before" : ["Before", "running", foo()],
        \t"after" : ["Results:", foo_results()],
        \t"separator" : "\\t",
        \t"send_error" : True,
        \t"error_message" : "An error occurred:"
    }\n
    If a message isn't given it will not be sent. If an error occurs, the error message will be sent.
    This function can also be used in multiple different ways:\n
    @notify(settings)\n
    def foo():\n
    Or:\n
    @notify\n
    def foo()\n
    foo(dcalerts_settings=settings)\n
    Or:\n
    foo=notify(settings)(foo)\n
    foo()
    """
    # Handle case where settings are provided directly
    if func is None or not callable(func):
        # This handles @notify(settings) and notify(settings)(foo)
        _settings = func if dcalerts_settings is None else dcalerts_settings

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                # Get settings from kwargs if present, otherwise use empty dict
                settings = kwargs.pop("dcalerts_settings", {})

                # Combine settings with priority to explicitly passed kwargs
                effective_settings = {}
                if _settings is not None:
                    effective_settings.update(_settings)
                effective_settings.update(settings)

                # Make sure webhook exists
                if "webhook" not in effective_settings:
                    raise ValueError("Missing webhook in dcalerts_settings")
                
                message_handler = MessageHandler(effective_settings["webhook"])
                list_item_sep = effective_settings.get("separator", "\n")

                # ------ Before ------ #
                before = effective_settings.get("before")
                if before:
                    message_handler.send(_make_message(before, list_item_sep=list_item_sep))
                # -------------------- #

                try:
                    result = f(*args, **kwargs)  # Use f here, not func
                    
                    # ------ After ------ #
                    after = effective_settings.get("after")
                    if after:
                        message_handler.send(_make_message(after, list_item_sep=list_item_sep))
                    # ------------------- #
                    
                    return result
                except Exception as e:
                    # Optionally handle error notifications
                    if effective_settings.get("send_error"):
                        message_handler.send(_make_message([effective_settings.get("error_message", "ERROR:"),str(e)], list_item_sep=list_item_sep))
                    raise
                
            return wrapper
        return decorator
    
    # Handle case where @notify is used without parentheses
    @wraps(func)
    def wrapper(*args, **kwargs):
        settings = kwargs.pop("dcalerts_settings")
        
        # Make sure webhook exists
        if "webhook" not in settings:
            raise ValueError("Missing webhook in dcalerts_settings")
            
        message_handler = MessageHandler(settings["webhook"])
        list_item_sep = settings.get("separator", "\n")

        # ------ Before ------ #
        before = settings.get("before")
        if before:
            message_handler.send(_make_message(before, list_item_sep=list_item_sep))
        # -------------------- #

        try:
            result = func(*args, **kwargs)
            
            # ------ After ------ #
            after = settings.get("after")
            if after:
                message_handler.send(_make_message(after, list_item_sep=list_item_sep))
            # ------------------- #
            
            return result
        except Exception as e:
            # Optionally handle error notifications
            if settings.get("send_error"):
                message_handler.send(_make_message([settings.get("error_message", "ERROR:"),str(e)], list_item_sep=list_item_sep))
            raise
            
    return wrapper


def _make_message(input, list_item_sep="\n"):
    final_message=""
    
    if type(input)==str:
        final_message+=input

    elif callable(input):
        final_message+=str(input())

    elif type(input)==list:
        for item in input:
            final_message+=_make_message(item, list_item_sep=list_item_sep)+list_item_sep
    else:
        final_message+=str(input)

    return final_message