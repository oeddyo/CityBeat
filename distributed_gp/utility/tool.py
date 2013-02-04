import calendar
from datetime import datetime

def getCurrentStampUTC():
    cur_utc_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
    return cur_utc_timestamp


def processAsPeopleCount():
    # process the data and delete those that are "floodingly" upload photos
    # eliminate photos that are within a time window

    pass


if __name__ == "__main__":
    print getCurrentStampUTC()
