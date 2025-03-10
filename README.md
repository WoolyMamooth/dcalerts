# dcalerts

Provides different utilities, decorators and classes that let the user send Discord messages from code.

## Installation

You can install directly from GitHub:
```
pip install git+https://github.com/WoolyMamooth/dcalerts
```
Or the latest stable release from PyPI:
```
pip install dcalerts
```

## Quickstart
```python
from dcalerts import DcalertsSettings, Notifier

dcalerts_settings=DcalertsSettings(
    webhook = webhook_url,
    before = "Starting code.",
    after = "Code finished.",
    send_error = True
)

with Notifier(dcalerts_settings) as notifier:
    print("Doing stuff")
```
# Usage

### Settings
---
`dcalerts` uses a special `dict` class called `DcalertsSettings` to track what messages you want to send and where. In the code it is uniformly referred to as `dcalerts_settings`. It can have the following items:
 - `webhook` : Can be either a `str` or a `MessageHandler` object. It should be the link you get from your Discord channel. You can learn how to make one [HERE](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks). This is where your messages will be sent to.
 - `before` : Optional. This is the message that is sent before your given code starts execution. Used by *decorators* and *context managers*.
 - `after` : Optional. This is the message that is sent after your given code finishes. Used by *decorators* and *context managers*.
 - `separator` : Optional. Used to separate the multiple items in messages. (more on this below)
 - `send_error` : Optional. If it is set to `True` any errors that stop the program will be sent to the `webhook` as well. `False` by default.
 - `error_message` : Optional. This will be the message sent together with the error text if an error is encountered. Default is `"ERROR:"`.

Messages can be *strings*, *lists*, *lists of lists*, or *functions*. Your message will always pass through the `make_message()` function. This will execute all functions in the message, cast everything to string and fuse together all items of the list in order putting the `separator` string between them. For example this is a valid message you could put in `after`:
```python
def result_function():
    return ["Something something", 42]

dcalerts_settings["after"] = ["Your code is done. Results:", result_function]
```
### Simple messaging
---
For this you don't even need your `dcalerts_settings` (but you can use it if you have one). You can simply use a webhook url to send a message.
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

# OR

message_handler = MessageHandler(dcalerts_settings)

message_handler.send("This is a message.")
```

These also use `make_message`, so you can complicate messages as much as you like

```python
send_message(webhook_url, ["This is a message.", [42, result_function]])
```

### Context manager
---
The package offers a context manager class called `Notifier`. You can use this to send messages before, during and after code execution. For example:
```python
from dcalerts import Notifier, DcalertsSettings
from dcalerts.utils import code_block

class Testclass:
    def __init__(self, num):
        self.num = num

    def get_num(self):
        return self.num

testobj = Testclass(42)

dcalerts_settings=DcalertsSettings(
    webhook = webhook_url,
    before = "Starting code.",
    after = ["Code finished. Result:", code_block(testobj.get_num)],
)

with Notifier(dcalerts_settings) as notifier:
    # dcalerts_settings["before"] is sent here. The message will be: "Starting code."
    print("Doing stuff.")
    # we change testobj.num here
    testobj.num = 43
    notifier.send(["Partial result:",testobj.get_num]) # The message will be: "Partial result: 43"
    print("Doing more stuff.")
    # we change testobj.num again
    testobj.num = 44
    # dcalerts_settings["after"] is sent here. The message will be: "Code finished. Result: 44"
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

## Misc
---
To check the default value of any of the settings, you can use the `DEFAULTS` dictionary.

```python
from dcalerts import DEFAULTS

print(DEFAULTS)
```

There is a `Specialsep` class used internally that changes the `separator` character mid-message. This is mainly used by the `utils` functions, because their output has to be formatted in a special way. (for example Discord understands emojis if you write their name like this: `:emoji:`, so we can't have a whitespace after the `:` character). If you want to, you can use it like this:
```python
from dcalerts.messages import Specialsep

send_message(webhook, ["This is a message", [Specialsep("\n"),"Everything in", "this list", "is a new line"], "but not this."], list_item_sep=" ")
```