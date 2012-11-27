from lib.mysql_connect import connect_to_mysql
from pandas import Series

cursor = connect_to_mysql()
sql = 'select * from region_photos'

cursor.execute(sql)

dates = []
counts = []
for r in cursor.fetchall():
    counts.append(1)
    dates.append(r['created_time'])


ts = Series(counts, index = dates)
ts = ts.resample('h',how='mean')
ts.plot()
