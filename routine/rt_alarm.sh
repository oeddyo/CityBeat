#!/bin/sh
date
source /grad/users/kx19/.bash_profile
(cd /grad/users/kx19/CityBeat/distributed_gp && nohup python /grad/users/kx19/CityBeat/distributed_gp/alarm2.py >> /.freespace/alarm_db_report.txt & )
