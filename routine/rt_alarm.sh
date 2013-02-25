#!/bin/sh
date
source /grad/users/kx19/.bash_profile
(cd /grad/users/kx19/CityBeat/distributed_gp && nohup python /grad/users/kx19/CityBeat/distributed_gp/run_online_alarm.py >> /.freespace/alarm_db_report.txt & )
