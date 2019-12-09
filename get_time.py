import datetime

def get_time():
    x = datetime.datetime.now()
    time = str(x.year) + "/" + str(x.month) + "/" + str(x.day) + " " + str(x.hour) + ":" + str(x.minute) + ":" + str(x.second)
    return time