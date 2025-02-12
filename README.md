# dcalerts
Provides a wrapper function and other utilities that let the user send Discord messages when their code execution starts or finishes.

## Installation

You can install directly from GitHub:
```
pip install git+https://github.com/WoolyMamooth/dcalerts
```
## Usage

### MessageHandler

```python

from dcalerts import MessageHandler, send_message

message_handler = MessageHandler("your webhook url here")
message_handler.send("This is a message.")

# or you could just use send_message

send_message("your webhook url here", "This is a message.")

```

### notify decorator
```python

from dcalerts import notify, create_timer
from time import sleep

@notify
def foo(t):
    sleep(t)

settings={
    "webhook_url" : "your webhook url here",
    "message_before" : "Time until completion: "+create_timer(10),
    "message_after" : "After running"
}

foo(10, settings=settings)

```