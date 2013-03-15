instagram_client_id = '4d9231b411eb4ef69435b40eb83999d6'
instagram_client_secret = '204c565fa1244437b9034921e034bdd6'

instagram_API_pause = 0.1

#mongodb_address = 'grande'
mongodb_address = 'grande.rutgers.edu'
mongodb_port = 27017

class InstagramConfig:
    photo_db = 'citybeat'
    #notice. seperate online setting and experiment setting
    event_db = 'citybeat'

    #experiment setting as follow (uncomment them)
    #photo_collection = 'photos_no_duplicate'
    #event_collection = 'next_week_candidate_event_25by25'
    #online setting
    photo_collection = 'photos_no_duplicate'
    event_collection = 'online_candidate'
    prediction_db = 'citybeat'
    #prediction_collection = 'next_week_prediction_25by25'
    prediction_collection = 'online_prediction'
    # in seconds
    merge_time_interval = 1
    zscore = 3
    min_phots = 8
    # bottom left: 40.690531,-74.058151
    # bottom right: 40.823163,-73.857994
    photo_min_lat = 40.690531
    photo_max_lat = 40.823163
    photo_min_lng = -74.058151
    photo_max_lng = -73.857994
    # cut the region into region_N * region_M subregions
    # try 10*10, 15*15, 20*20, 25*25
    #region_N = 25
    #region_M = 25
    region_percentage = 0.3

instagram_client_id = '4d9231b411eb4ef69435b40eb83999d6'
instagram_client_secret = '204c565fa1244437b9034921e034bdd6'

instagram_API_pause = 0.1

#mongodb_address = 'grande'
mongodb_address = 'grande.rutgers.edu'
mongodb_port = 27017
