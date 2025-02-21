import time

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
    return "```"+language+"\n"+text+"```"

def inline_code(text:str):
    """
    Wraps text in inline code.
    """
    return "`"+text+"`"

def bold(text:str):
    """
    Makes text bold.
    """
    return "**"+text+"**"

def italic(text:str):
    """
    Makes text italic.
    """
    return "*"+text+"*"

def underline(text:str):
    """
    Underlines text.
    """
    return "__"+text+"__"

def strikethrough(text:str):
    """
    Strikes through text.
    """
    return "~~"+text+"~~"

def spoiler(text:str):
    """
    Makes text a spoiler.
    """
    return "||"+text+"||"

def quote(text:str):
    """
    Quotes text.
    """
    return "> "+text

def block_quote(text:str):
    """
    Quotes text in a block.
    """
    return ">>> "+text

def link(text:str, url:str):
    """
    Creates a hyperlink.
    """
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
    return "#"*level+" "+text