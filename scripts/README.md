Convert standalone to replicaset: https://docs.mongodb.com/manual/tutorial/convert-standalone-to-replica-set/

1. sudo systemctl stop mongod
2. sudo mkdir -p /srv/mongodb/db0
3. sudo mongod --port 27017 --dbpath /srv/mongodb/db0 --replSet rs0 --bind_ip localhost
4. Install mongosh: https://docs.mongodb.com/mongodb-shell/install/#std-label-mdb-shell-install
    * wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
    * sudo apt-get install gnupg
    * wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
    * echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
    * sudo apt-get update
    * sudo apt-get install -y mongodb-mongosh
5. mongosh
6. rs.initiate()
7. If failed, try to add following command to /etc/mongod.conf
```
replication:
  replSetName: rs0
  oplogSizeMB: 100
```
