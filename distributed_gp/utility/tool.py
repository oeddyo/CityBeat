import calendar
from datetime import datetime

def getCurrentStampUTC():
    cur_utc_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
    return cur_utc_timestamp



if __name__ == "__main__":
    print getCurrentStampUTC()
