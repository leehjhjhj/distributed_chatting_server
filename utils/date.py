from datetime import datetime

def current_time():
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_now
