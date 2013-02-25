from utility.prediction_interface import PredictionInterface



if __name__=="__main__":
    pi = PredictionInterface()
    pi.setDB('citybeat')
    pi.setCollection('online_prediction')
    region ={
            "min_lat" : 40.79133132,
            "max_lng" : -73.93005052,
            "min_lng" : -73.9380568,
            "max_lat" : 40.7966366
            }
    condition = ({'region.min_lat':region['min_lat'],
        'region.min_lng':region['min_lng'],
        'region.max_lat':region['max_lat'],
        'region.max_lng':region['max_lng']})
    prediction = pi.getNearestPrediction(region, '1361801869') #1361772000
    print prediction

