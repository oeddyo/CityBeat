#!/bin/sh
date
source /grad/users/kx19/.bash_profile
(cd /grad/users/kx19/CityBeat && nohup python /grad/users/kx19/CityBeat/run_distributed_crawl.py 200 tmp_citybeat > /.freespace/rt_update.log & )
