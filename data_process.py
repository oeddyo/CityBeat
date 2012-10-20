from lib.mysql_connect import connect_to_mysql

cursor = connect_to_mysql()
sql = "select * from herenow_region where time > '2012-10-08 6:00:00' and time < '2012-10-08 6:15:00';"
cursor.execute(sql)

print 'data:['
for r in cursor.fetchall():
    print '{'+'lat: '+str(r['mid_lat']) + ', lng:'+str(r['mid_lng']) + ', count: '+str(r['herenow']) + '},',
print ']'
