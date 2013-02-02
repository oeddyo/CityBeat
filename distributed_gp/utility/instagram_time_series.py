# Copyright [2013] Eddie Xie.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas

from pandas import Series

from datetime import datetime
from time_series import TimeSeries



class InstagramTimeSeries(TimeSeries):
    """For a single region specified by a box of
    [upper_left_lat, upper_left_lng, down_right_lat, down_right_lng]
    build a time series for that location 
    """

    def __init__(self, region, start_timestamp, end_timestamp, freq = '1h'):
        super(InstagramTimeSeries, self).__init__(region,
                start_timestamp, end_timestamp, freq)

    def buildTimeSeries(self, count_people = True, avoid_flooding = True):
        """Return a pandas Series object
        
        count_people = True menas we only want to count single user
        instead of # of photos for that region

        avoid_flooding = True means we want to avoid a single user
        flooding many photos into instagram in a short time. Now we
        set the time window as within 10 minutes only count as a single
        user
        
        """
        window_avoid_flooding = 600
        data  = []
        photo_cnt = 0
        for photo in self.cursor:
            p = {'user':photo['user'], 'created_time':photo['created_time']}
            data.append(p)
            photo_cnt += 1
            if photo_cnt%10000==0:
                print photo_cnt
        data= sorted(data, key = lambda x:x['created_time'])
        
        user_last_upload = {}   #for a single user, when is his last upload
        counts = []
        dates = []
        for photo_json in data:
            user = photo_json['user']['username']
            utc_date = datetime.utcfromtimestamp(float(photo_json['created_time']))
            if count_people:
                if user not in user_last_upload:
                    user_last_upload[user] = int(photo_json['created_time'])
                    dates.append(utc_date)
                    counts.append(1)
                else:
                    if float(photo_json['created_time']) - float(user_last_upload[user]) > window_avoid_flooding:
                        user_last_upload[user] = int(photo_json['created_time'])
                        dates.append(utc_date)
                        counts.append(1)
            else:
                dates.append(utc_date)
                counts.append(1)
        
        
        self.series = Series(counts, index = dates)
        try:
            self.series = self.series.resample(self.freq, how='sum', label='right')
        except Exception as e:  #not enough data
            pass
        return self.series

from region import Region
from config import InstagramConfig
import photo_interface


def test():
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
            ]
    huge_region = Region(coordinates)
    regions = huge_region.divideRegions(4, 4)
    for i in range(16):
        if i<14:
            continue
        test_region = regions[i]
        test_region.display()
        ts = InstagramTimeSeries(test_region, 1355765315-30*24*3600, 1355765315)
        print ts.buildTimeSeries()

test()

