#!/bin/sh
date
source /grad/users/kx19/.bash_profile
(cd /grad/users/kx19/CityBeat && nohup python /grad/users/kx19/CityBeat/merge_mongo.py &)
sleep 100
(cd /grad/users/kx19/CityBeat/distributed_gp && nohup python /grad/users/kx19/CityBeat/distributed_gp/run_distributed_gp.py  > /.freespace/dis_gp.log &)

