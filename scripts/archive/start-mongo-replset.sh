#!/bin/bash

# shell script to create a simple mongodb replica set (tested on osx)
set -e

red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
default=$(tput sgr0)

function finish {
    pids=(`cat ~/mongosvr/rs-*.pid`)
    for pid in "${pids[@]}"
    do
        kill $pid
        wait $pid
    done
}

trap finish EXIT


mkdir -p ~/mongosvr/rs-0
mkdir -p ~/mongosvr/rs-1
mkdir -p ~/mongosvr/rs-2

mongod --shardsvr --dbpath ~/mongosvr/rs-0 --replSet set --rest --port 27091 \
    --config . --pidfilepath ~/mongosvr/rs-0.pid 2>&1 | sed "s/.*/$red&$default/" &

mongod --shardsvr --dbpath ~/mongosvr/rs-1 --replSet set --rest --port 27092 \
    --config . --pidfilepath ~/mongosvr/rs-1.pid 2>&1 | sed "s/.*/$green&$default/" &

mongod --shardsvr --dbpath ~/mongosvr/rs-2 --replSet set --rest --port 27093 \
    --config . --pidfilepath ~/mongosvr/rs-2.pid 2>&1 | sed "s/.*/$yellow&$default/" &

# wait a bit for the first server to come up
sleep 5

# call rs.initiate({...})
cfg="{
    _id: 'set',
    members: [
        {_id: 1, host: 'localhost:27091'},
        {_id: 2, host: 'localhost:27092'},
        {_id: 3, host: 'localhost:27093'}
    ]
}"

mongo localhost:27091 --eval "JSON.stringify(db.adminCommand({'replSetInitiate' : $cfg}))"

# sleep forever
cat
