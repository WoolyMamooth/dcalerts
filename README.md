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

or you could just use **send_message**

```python
send_message("your webhook url here", "This is a message.")
```
or
```python
dcalerts_settings={
    "webhook" : "your webhook url here"
}

send_message(settings, "This is a message")
```

### notify decorator

This decorator lets you send messages both before and after the execution of the function you use it on. If you don't set one of the messages it will not be sent, so you could for example only send a message after the execution.
Put everything you want to send into a dictionary together with your webhook link. (NOTE: you can also pass a **MessageHandler** instead of a string in the place of the webhook url) Like so:
```python
settings={
    "webhook" : "your webhook url here",
    "before" : "Before running",
    "after" : "After running"
}
```
You can also put in lists, lists of lists, and even functions. If you put in a list for a message all of it's contents will be casted to string, then concatenated and sent as one message. You can set the separating character under the name *separator* (by default it's '**\\n**'). If you put in a function it will be executed after the decorated function and it's return value casted to string and added to the message. For example:
```python
result_func():
    return "some return value"

settings={
    "webhook" : "your webhook url here",
    "before" : ["This", ["is", "before"]],
    "after" : ["Results:", result_func()],
    "separator" : "\t"
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
You can also use **notify** like this:
```python
@notify(dcalerts_settings=settings)
def foo(t)
    sleep(t)

foo(10)
```
Or like this:
```python
def foo(t):
    sleep(t)

foo = notify(settings)(foo)
foo()
```

### Utils

The following utility functions are available in `dcalerts.utils`. They return text in a format that Discord interprets in a special way:

- **create_timer(seconds_from_now)**: Returns a string which Discord reads as a timer to a given second.
- **code_block(text, language="")**: Wraps text in a code block.
- **inline_code(text)**: Wraps text in inline code.
- **bold(text)**: Makes text bold.
- **italic(text)**: Makes text italic.
- **underline(text)**: Underlines text.
- **strikethrough(text)**: Strikes through text.
- **spoiler(text)**: Makes text a spoiler.
- **quote(text)**: Quotes text.
- **block_quote(text)**: Quotes text in a block.
- **link(text, url)**: Creates a hyperlink.
- **mention(user_id)**: Mentions a user.
- **channel_mention(channel_id)**: Mentions a channel.
- **role_mention(role_id)**: Mentions a role.
- **emoji(emoji_id)**: Adds an emoji.
- **header(text, level=1)**: Creates a header.