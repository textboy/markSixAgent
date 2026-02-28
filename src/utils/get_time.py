from datetime import datetime

def getTimeStamp():
    current_time = datetime.now().time()
    return current_time.strftime("%H:%M:%S")