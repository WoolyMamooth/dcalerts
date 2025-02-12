import time

def create_timer(seconds_from_now):
    """
    Returns a string which Discord reads as a timer to a given second. You can include this in the settings dict of notify:\n
    settings={\n
        \tmessage_before="Time until completion: "+create_timer(42)\n
    }
    """
    return "<t:"+str(int(time.time()+seconds_from_now))+":R>"