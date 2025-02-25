#!/bin/bash

mongod -f /home/mongodb/mongod.conf &

sleep 6.9
/opt/one_time_script.sh

mongod -f /home/mongodb/mongod.conf
