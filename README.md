# dcalerts
Provides a wrapper function and other utilities that let the user send Discord messages when their code execution starts or finishes.

## Installation

You can install directly from GitHub:
```
pip install git+https://github.com/WoolyMamooth/dcalerts
```
## Usage

### MessageHandler
A simple class you can use to send messages to the same Discord channel.
```python
from dcalerts import MessageHandler, send_message

message_handler = MessageHandler("your webhook url here")
message_handler.send("This is a message.")
```

or you could just use send_message

```python
send_message("your webhook url here", "This is a message.")
```
or
```python
dcalerts_settings={
    "webhook_url" : "your webhook url here"
}

send_message(settings, "This is a message")
```

### notify decorator
This decorator lets you send messages both before and after the execution of the function you use it on. If you don't set one of the messages it will not be sent, so you could for example only send a message after the execution.
Put everything you want to send into a dictionary together with your webhook link. Like so:
```python
settings={
    "webhook_url" : "your webhook url here",
    "message_before" : "Before running",
    "message_after" : "After running"
}
```
You can also put in lists or even functions. If you put in a list for a message all of it's contents will be casted to string, then concatenated and sent as one message. You can set the separating character under the name *list_item_sep* (by default it's '\\n'). If you put in a function it will be executed after the decorated function and it's return value casted to string and added to the message. For example:
```python
result_func():
    return "some return value"

settings={
    "webhook_url" : "your webhook url here",
    "message_before" : ["This", "is", "before"],
    "message_after" : ["Results", result_func()]
}
```
Then you have to pass your dictionary to your function as *dcalerts_settings*:
```python
from dcalerts import notify
from time import sleep

@notify
def foo(t):
    sleep(t)

foo(10, dcalerts_settings=settings)
``` 