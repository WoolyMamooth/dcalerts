# dcalerts

Provides utilities that let the user send Discord messages from code.

## Installation

You can install directly from GitHub:
```
pip install git+https://github.com/WoolyMamooth/dcalerts
```
## TLDR
```python
from dcalerts import Notifier

dcalerts_settings={
            "webhook":webhook_url,
            "before":"Starting code execution",
            "after":"Code finished",
            "send_error":True
        }

with Notifier(dcalerts_settings) as notifier:
    print("Doing stuff")
```
# Usage

### Settings
---
`dcalerts` uses a simple `dict` to track what messages you want to send and where. In the code it is uniformly referred to as `dcalerts_settings`. It can have the following items:
 - `webhook` : Can be either a `str` or a `MessageHandler` object. It should be the link you get from your Discord channel. You can learn how to make one [HERE](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks). This is where your messages will be sent to.
 - `before` : Optional. This is the message that is sent before your given code starts execution. Used by *decorators* and *context managers*.
 - `after` : Optional. This is the message that is sent after your given code finishes. Used by *decorators* and *context managers*.
 - `separator` : Optional. Used to separate the multiple items in messages. (more on this below)
 - `send_error` : Optional. If it is set to `True` any errors that stop the program will be sent to the `webhook` as well. `False` by default.
- `error_message` : Optional. This will be the message sent together with the error text if an error is encountered. Default is `"ERROR:"`.

Messages can be *strings*, *lists*, *lists of lists*, or *functions*. If you use anything but the most basic sending functions your message will first pass through the `make_message` function. This will execute all functions in the message, cast everything to string and fuse together all items of the list in order putting the `separator` string between them. For example this is a valid message you could put in `after`:
```python
def result_function():
    return ["Something something", 42]

dcalerts_settings["after"] = ["Your code is done. Results:", code_block(result_function())]
```
### Simple messaging
---
For this you don't even need your `dcalerts_settings`. You can simply use a webhook url to send a message. But if you have a `dict` you can also use that:
```python
from dcalerts import send_message

send_message(webhook_url, "This is a message.")

# OR

send_message(dcalerts_settings, "This is a message.")
```
If you want to send many messages to the same channel, but don't need anything fancy, you can use a `MessageHandler`:
```python
from dcalerts import MessageHandler

message_handler = MessageHandler(webhook_url)
message_handler.send("This is a message.")
```
Keep in mind these only accept *strings*. If you want to send a fancy message this way, you should call `make_message` first.
```python
send_message(webhook_url, make_message(["This is a message.", 42]))
```
### Context manager
---
The package offers a context manager class called `Notifier`. You can use this to send messages before, during and after code execution. Note that this class automatically uses `make_message` before sending anything. For example:
```python
from dcalerts import Notifier
from time import sleep

def foo():
    return 42

with Notifier(dcalerts_settings) as notifier:
    # dcalerts_settings["before"] is sent here
    print("Doing stuff.")
    sleep(2)
    notifier.send(["Partial result:",foo()])
    print("Doing more stuff.")
    sleep(2)
    # dcalerts_settings["after"] is sent here
```

### Decorator
---
There is also a decorator you can use to send messages before and after running your function. You can use this in multiple ways:
```python
from dcalerts import notify
from time import sleep

@notify
def foo(t):
    sleep(t)

foo(10, dcalerts_settings=dcalerts_settings)
``` 
Or:
```python
@notify(dcalerts_settings=dcalerts_settings)
def foo(t)
    sleep(t)

foo(10)
```
Or:
```python
def foo(t):
    sleep(t)

foo = notify(dcalerts_settings)(foo)
foo()
```

### Utils
---

The following utility functions are available in `dcalerts.utils`. They return text in a format that Discord interprets in a special way. Most of them use `make_message` to make it simpler to use them:

- `create_timer(seconds_from_now)` : Returns a string which Discord reads as a timer to a given second.
- `code_block(text, language="")` : Wraps text in a code block.
- `inline_code(text)` : Wraps text in inline code.
- `bold(text)` : Makes text bold.
- `italic(text)` : Makes text italic.
- `underline(text)` : Underlines text.
- `strikethrough(text)` : Strikes through text.
- `spoiler(text)` : Makes text a spoiler.
- `quote(text)` : Quotes text.
- `block_quote(text)` : Quotes text in a block.
- `link(text, url)` : Creates a hyperlink.
- `mention(user_id)` : Mentions a user.
- `channel_mention(channel_id)` : Mentions a channel.
- `role_mention(role_id)` : Mentions a role.
- `emoji(emoji_id)` : Adds an emoji.
- `header(text, level=1)` : Creates a header.