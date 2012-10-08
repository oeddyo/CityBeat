import MySQLdb

def connect_to_mysql():
    sql_conn = MySQLdb.connect(host='localhost', user='root', passwd='sci', db='heatmap', charset='utf8', use_unicode = True)
    sql_conn.autocommit(True)
    sql_db = sql_conn.cursor(MySQLdb.cursors.DictCursor)
    return sql_db


def add_table_herenow_region():
    sql = """
    CREATE TABLE IF NOT EXISTS herenow_region(
    auto_id MEDIUMINT NOT NULL AUTO_INCREMENT,
    mid_lat DOUBLE,
    mid_lng DOUBLE,
    lat_length DOUBLE,
    lng_length DOUBLE,
    time DATETIME,
    herenow INT(10),
    PRIMARY KEY(auto_id)
    )ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)
def add_table_herenow():
    sql = """
    CREATE TABLE IF NOT EXISTS herenow(
    auto_id MEDIUMINT NOT NULL AUTO_INCREMENT,
    venue_id VARCHAR(50) NOT NULL,
    hereNow INT(10),
    lat DOUBLE,
    lng DOUBLE,
    time DATETIME,
    name VARCHAR(100),
    PRIMARY KEY(auto_id)
    )ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_hereNow_foursquare():
    sql = """
    CREATE TABLE IF NOT EXISTS hereNow(
    auto_id MEDIUMINT NOT NULL AUTO_INCREMENT,
    venue_id VARCHAR(50) NOT NULL,
    hereNow INT(10),
    lat DOUBLE,
    lng DOUBLE,
    time DATETIME,
    name VARCHAR(100),
    PRIMARY KEY(auto_id)
    )ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_region():
    sql  = """
    CREATE TABLE IF NOT EXISTS hereNow(
    auto_id MEDIUMINT NOT NULL AUTO_INCREMENT,
    hereNow INT(10),
    lat DOUBLE,
    lng DOUBLE,
    radius DOUBLE,
    time DATETIME,
    PRIMARY KEY(auto_id)
    ) ENGINE InnoDB DEFAULT CHARSET=utf8;
    """


def add_table_venue_meta():
    sql = """
    CREATE TABLE IF NOT EXISTS venue_meta(
    id VARCHAR(50) NOT NULL,
    name VARCHAR(200) ,
    lat DOUBLE ,
    lng DOUBLE ,
    postalCode VARCHAR(20) ,
    city VARCHAR(100) ,
    state VARCHAR(100),
    country VARCHAR(100),
    verified BOOL,
    checkinsCount INT(20),
    usersCount INT(20),
    tipCount INT(20),
    url VARCHAR(500),
    likesCount INT(20),
    rating  DOUBLE,
    ratingSignals   INT(20),
    photoCount  INT(20),
    PRIMARY KEY(id)
    )   ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_venue_photo_4sq():
    sql = """
    CREATE TABLE IF NOT EXISTS venue_photo_4sq(
    venue_id VARCHAR(50) NOT NULL,
    id VARCHAR(50) NOT NULL,
    createdAt INT(30),
    source_name VARCHAR(200),
    source_url VARCHAR(500), 
    url VARCHAR(500),
    user_id INT(20),
    user_firstName VARCHAR(100),
    user_lastName VARCHAR(100),
    user_photo VARCHAR(500),
    user_gender VARCHAR(20),
    user_homeCity VARCHAR(100),
    user_tips INT(20),
    
    PRIMARY KEY(id)
    ) ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_venue_tips():
    sql = """
    CREATE TABLE IF NOT EXISTS venue_tips(
    venue_id VARCHAR(50) NOT NULL,
    id VARCHAR(50) NOT NULL,
    createdAt INT(30),
    text TEXT, 
    likesCount INT(10),
    user_id INT(20),
    user_firstName VARCHAR(100),
    user_lastName VARCHAR(100),
    user_photo VARCHAR(500),
    user_gender VARCHAR(20),
    user_homeCity VARCHAR(100),
    user_tips INT(20),
    PRIMARY KEY(id)
    ) ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_venue_photo_instagram():
    sql = """
    CREATE TABLE IF NOT EXISTS venue_photo_instagram(
    foursquare_venue_id VARCHAR(50) NOT NULL,
    instagram_venue_id INT(20) NOT NULL,
    id VARCHAR(50) NOT NULL,
    filter VARCHAR(100),
    tags TEXT,
    comments TEXT,
    likes_count INT(10),
    link VARCHAR(500),
    username VARCHAR(100),
    profile_picture VARCHAR(500),
    standard_resolution VARCHAR(200),
    created_time DATETIME,
    PRIMARY KEY(id)
    ) ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)


def add_table_venue_stats():
    sql = """
    CREATE TABLE IF NOT EXISTS venue_stats(
    auto_id MEDIUMINT NOT NULL AUTO_INCREMENT,
    id VARCHAR(50) NOT NULL,
    time DATETIME NOT NULL,
    checkinsCount INT(12),
    usersCount INT(12),
    tipCount INT(12),
    photoCount INT(12),
    PRIMARY KEY (auto_id)
    )ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)


