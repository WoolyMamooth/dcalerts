import time
from .messages import make_message

def create_timer(seconds_from_now):
    """
    Returns a string which Discord reads as a timer to a given second. You can include this in the settings dict of @notify:\n
    settings={\n
        \tmessage_before="Time until completion: "+create_timer(42)\n
    }
    """
    return "<t:"+str(int(time.time()+seconds_from_now))+":R>"

def code_block(text:str, language:str=""):
    """
    Wraps text in a code block.
    """
    if type(text)is not str:
        text=make_message(text)
    return "```"+language+"\n"+text+"```"

def inline_code(text:str):
    """
    Wraps text in inline code.
    """
    if type(text)is not str:
        text=make_message(text)
    return "`"+text+"`"

def bold(text:str):
    """
    Makes text bold.
    """
    if type(text)is not str:
        text=make_message(text)
    return "**"+text+"**"

def italic(text:str):
    """
    Makes text italic.
    """
    if type(text)is not str:
        text=make_message(text)
    return "*"+text+"*"

def underline(text:str):
    """
    Underlines text.
    """
    if type(text)is not str:
        text=make_message(text)
    return "__"+text+"__"

def strikethrough(text:str):
    """
    Strikes through text.
    """
    if type(text)is not str:
        text=make_message(text)
    return "~~"+text+"~~"

def spoiler(text:str):
    """
    Makes text a spoiler.
    """
    if type(text)is not str:
        text=make_message(text)
    return "||"+text+"||"

def quote(text:str):
    """
    Quotes text.
    """
    if type(text)is not str:
        text=make_message(text)
    return "> "+text

def block_quote(text:str):
    """
    Quotes text in a block.
    """
    if type(text)is not str:
        text=make_message(text)
    return ">>> "+text

def link(text:str, url:str):
    """
    Creates a hyperlink.
    """
    if type(text)is not str:
        text=make_message(text)
    return "["+text+"]("+url+")"

def mention(user_id:str):
    """
    Mentions a user.
    """
    return "@"+user_id

def channel_mention(channel_id:str):
    """
    Mentions a channel.
    """
    return "#"+channel_id

def role_mention(role_id:str):
    """
    Mentions a role.
    """
    return "@"+role_id

def emoji(emoji_id:str):
    """
    Adds an emoji.
    """
    return ":"+emoji_id+":"

def header(text:str, level:int=1):
    """
    Creates a header.
    """
    if type(text)is not str:
        text=make_message(text)
    return "#"*level+" "+text