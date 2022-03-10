#!/bin/bash

# shell script to create a simple mongodb sharded cluster locally.
# Requires a replica set to be already running, you can run
# start-mongo-replset.sh first to start a replica set.
set -e

red=$(tput setaf 1)
green=$(tput setaf 2)
default=$(tput sgr0)

function finish {
    pid=`cat ~/mongosvr/shard-config-0.pid`
    kill $pid
    wait $pid
}
trap finish EXIT


mkdir -p ~/mongosvr/config-0

# start up the mongodb config server for the shards 
mongod --configsvr --dbpath ~/mongosvr/config-0 --port 27019 \
    --config . --pidfilepath ~/mongosvr/shard-config-0.pid 2>&1 | sed "s/.*/$red&$default/" &

sleep 3

mongos --configdb localhost:27019 | sed "s/.*/$green&$default/" &

sleep 3

# add the first replica set instance as a shard, the others will be discovered automatically by mongos
mongo --eval "JSON.stringify(sh._adminCommand( { addShard : 'set/localhost:27091' } , true ))"

# enable sharding on the test database
mongo --eval "JSON.stringify(sh._adminCommand( { enableSharding : 'test' } ))"

# sleep forever
cat
