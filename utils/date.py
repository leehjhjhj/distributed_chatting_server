from datetime import datetime

def current_time():
    now = datetime.now()
    formatted_now = now.strftime('%m/%d %H:%M')
    return formatted_now
