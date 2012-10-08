"""This script contains all the mysql fetching and saving functions so that this could be independent of main logics

"""

import mysql_connect
import datetime
import json
import datetime

def save_region(region):
    """Save region data for a single venue into mysql (table venue_meta)
See table 'region_foursquare' for details of fields
Keyword arguments
venue - Venue object """
    curtime = datetime.datetime.now()
    mid_lat = region[0]
    mid_lng = region[1]
    lat_length = region[2]
    lng_length = region[3]
    herenow = region[4]
    cursor = mysql_connect.connect_to_mysql()
    cursor.execute("INSERT INTO herenow_region(mid_lat, mid_lng, lat_length, lng_length, time, herenow) values (%s" + ",%s"*5 + ")",(mid_lat, mid_lng, lat_length, lng_length, curtime, herenow) ) 

def save_herenow(venue):
    """Save hereNow data for a single venue into mysql (table venue_meta)
See table 'hereNow_foursquare' for details of fields
Keyword arguments
venue - Venue object """
    curtime = datetime.datetime.now()
    cursor = mysql_connect.connect_to_mysql()
    venue_dic = venue
    venue_id = venue_dic['id']
    name = venue_dic['name']
    hereNow = venue_dic['hereNow']['count']
    lat = venue_dic['location']['lat']
    lng = venue_dic['location']['lng']
    cursor.execute("INSERT INTO hereNow(venue_id, hereNow, lat, lng, time, name) values (%s" + ",%s"*5 + ")",(venue_id, hereNow, lat, lng, curtime, name) ) 
    """
    venue_dic = venue['venue']
    id = venue_dic['id']
    name = venue_dic.get('name',None)
    lat = venue_dic['location']['lat']
    lng = venue_dic['location']['lng']
    postalCode = venue_dic['location'].get('postalCode',None)
    city = venue_dic['location'].get('city',None)
    state = venue_dic['location'].get('state',None)
    country = venue_dic['location'].get('country',None)
    if venue_dic['verified'] == True:
        verified = 1
    else:
        verified = 0
    checkinsCount = venue_dic['stats'].get('checkinsCount', None)
    usersCount = venue_dic['stats'].get('usersCount',None)
    tipCount = venue_dic['stats'].get('tipCount',None)
    url = venue_dic.get('url', None)
    likesCount = venue_dic['likes'].get('count',None)
    rating = venue_dic.get('rating',None)
    ratingSignals = venue_dic.get('ratingSignals',None)
    photoCount = venue_dic['photos'].get('count',None)
    tmp_list = [id, name, lat, lng, postalCode, city, state, country, verified, checkinsCount, usersCount, tipCount, url, likesCount, rating, ratingSignals, photoCount]
    cursor = mysql_connect.connect_to_mysql()
    cursor.execute("REPLACE INTO venue_meta (id, name, lat, lng, postalCode, city, state, country, verified, checkinsCount, usersCount, tipCount, url, likesCount, rating, ratingSignals, photoCount) values (%s" + ",%s"*16 + ")", (id, name, lat, lng, postalCode, city, state, country, verified, checkinsCount, usersCount, tipCount, url, likesCount, rating, ratingSignals, photoCount) )
    #cursor.execute(sql)
    """
def save_venue_photo_4sq(photo, venue_id):
    """Save photos from 4sq into table venue_photo_4sq
    See table 'venue_photo_4sq' for columns detail.
    Keyword arguments
    photo - photos from 4sq 
    venue_id - venue id for this venue. Used as a foreign key"""
    cursor = mysql_connect.connect_to_mysql()
    for pic in photo['photos']['items']:
        print pic
        print '\n\n'
        id = pic['id']
        createdAt = pic.get('createdAt',None)
        source_name = pic['source'].get('name', None)
        source_url = pic['source'].get('url', None)
        url = pic.get('url', None)
        user_id = pic['user'].get('id',None)
        user_firstName = pic['user'].get('firstName',None)
        user_lastName = pic['user'].get('lastName', None)
        user_photo = pic['user'].get('photo',None)
        user_gender = pic['user'].get('gender',None)
        user_homeCity = pic['user'].get('homeCity',None)
        user_tips = pic['user']['tips'].get('count',None)
        cursor.execute("REPLACE INTO venue_photo_4sq (venue_id, id, createdAt, source_name, source_url, url, user_id, user_firstName, user_lastName, user_photo, user_gender, user_homeCity, user_tips) values (%s" + ",%s"*12+")", (venue_id, id, createdAt, source_name, source_url, url ,user_id, user_firstName, user_lastName, user_photo, user_gender, user_homeCity, user_tips) )


def save_photo_instagram(photos, foursquare_venue_id, instagram_venue_id):
    """Save photos from instagram into table venue_photo_instagram
    See table venue_photo_instagram for columns detail.
    Notice, this table structure is different from venue_photo_4sq.
    Keyword arguments
    photos - photos from instagram
    venue_id venue id for this venue. This is used as a foreign key"""
    cursor = mysql_connect.connect_to_mysql()
    for photo in photos:
        _id = photo.id
        _filter = photo.filter
        _tags = []
        if 'tags' in dir(photo):
            for t in photo.tags:
                _tags.append(t.name)
            #_tags = photo.tags
        if len(_tags)==0:
            _tags = None
        else:
            _tags = json.dumps(_tags)
        _comments = []
        for c in photo.comments:
            _comments.append( (c.user.username, c.text) )
        if len(_comments)==0:
            _comments = None
        else:
            _comments = json.dumps(_comments)
            #print _comments
        if len(photo.likes)==0:
            _likes_count = 0
        else:
            _likes_count = len(photo.likes)
        _link = photo.link
        _username = photo.user.username
        _profile_picture = photo.user.profile_picture
        _standard_resolution = photo.images['standard_resolution']
        _created_time = photo.created_time
        #print _id, _filter, _tags, _comments, _likes_count, _link, _username, _profile_picture, _standard_resolution, _created_time
        cursor.execute("REPLACE INTO venue_photo_instagram (foursquare_venue_id, instagram_venue_id, id, filter, tags, comments, likes_count, link, username, profile_picture, standard_resolution, created_time) values(%s" + ",%s"*11 + ")",(foursquare_venue_id,instagram_venue_id, _id, _filter, _tags, _comments, _likes_count, _link, _username, _profile_picture, _standard_resolution, _created_time) )


def save_venue_stats(venue_dic, foursquare_id):
    venue_dic = venue_dic['venue']
    checkinsCount = venue_dic['stats'].get('checkinsCount', None)
    usersCount = venue_dic['stats'].get('usersCount',None)
    tipCount = venue_dic['stats'].get('tipCount',None)
    photoCount = venue_dic['photos'].get('count',None)
    now_date = datetime.datetime.now()
    print now_date
    cursor = mysql_connect.connect_to_mysql()
    cursor.execute("INSERT INTO venue_stats (id, checkinsCount, usersCount, tipCount, photoCount , time) values (%s, %s, %s, %s, %s, %s) ", (foursquare_id, checkinsCount, usersCount, tipCount, photoCount, now_date) )

def get_all_foursquare_ids():
    sql = """
    select name,id from venue_meta
    """
    cursor = mysql_connect.connect_to_mysql()
    cursor.execute(sql)
    venue_id_name_dic = {}
    for r in cursor.fetchall():
        venue_id_name_dic[r['id']] = r['name']
    return venue_id_name_dic

def get_all_stats():
    sql = """
    select * from venue_stats;
    """
    cursor = mysql_connect.connect_to_mysql()
    cursor.execute(sql)
    return cursor.fetchall()

def get_all_photo_fetched_venue_id_instagram():
    sql = """
    select distinct foursquare_venue_id from venue_photo_instagram;
    """
    cursor = mysql_connect.connect_to_mysql()
    cursor.execute(sql)
    ids = set()
    for r in cursor.fetchall():
        ids.add(r['foursquare_venue_id'])
    return ids

def save_venue_tip(tips, venue_id):
    """Save tips from 4sq into table venue_tips.
    See table 'venue_tips' for columns detail.
    Keyword arguments
    tips - tips from 4sq given a venue id
    venue_id - venue id for this venue. This is used as a foreign key so that we could fetch venue details from venue_meta table"""
    cursor = mysql_connect.connect_to_mysql()
    for tip in tips['tips'].get('items', None):
        id = tip['id']
        createdAt = tip.get('createdAt',None)
        text = tip.get('text', None)
        likesCount = tip['likes'].get('count', None)
        user_id = tip['user'].get('id',None)
        user_firstName = tip['user'].get('firstName',None)
        user_lastName = tip['user'].get('lastName', None)
        user_photo = tip['user'].get('photo',None)
        user_gender = tip['user'].get('gender',None)
        user_homeCity = tip['user'].get('homeCity',None)
        user_tips = tip['user']['tips'].get('count',None)
        cursor.execute("REPLACE INTO venue_tips (venue_id, id, createdAt, text, likesCount, user_id, user_firstName, user_lastName, user_photo, user_gender, user_homeCity, user_tips) values (%s"+",%s"*11+")", (venue_id, id, createdAt, text, likesCount, user_id, user_firstName, user_lastName, user_photo, user_gender, user_homeCity, user_tips) )

