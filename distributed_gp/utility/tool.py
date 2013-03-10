import calendar
from datetime import datetime

def getCurrentStampUTC():
    cur_utc_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
    return cur_utc_timestamp


def processAsPeopleCount(data):
    # process the data and delete those that are "floodingly" upload photos
    # eliminate photos that are within a time window
    user_last_upload = {}
    return_data = []
    window_size = 600
    for photo_json in data:
        user = photo_json['user']['username']
        if user not in user_last_upload:
            user_last_upload[user] = int(photo_json['created_time'])
            return_data.append(photo_json)
        else:
            if float(photo_json['created_time']) - float(user_last_upload[user]) > window_size: 
                user_last_upload[user] = int(photo_json['created_time'])
            else:
                return_data.append(photo_json)
    return return_data

if __name__ == "__main__":
    print getCurrentStampUTC()
