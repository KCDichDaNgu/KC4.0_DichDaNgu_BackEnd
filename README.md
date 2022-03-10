# Cai dat moi truong

## Cài Cassandra
1. Cài Java-8
* sudo apt install openjdk-8-jdk

2. Cài Cassandra
* echo "deb http://www.apache.org/dist/cassandra/debian 40x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
* curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
* Nếu câu lệnh trên không chạy được: wget --no-check-certificate -qO - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
* sudo apt-get update
* sudo apt-get install cassandra

## Cài Kafka
1. Cài java-11
* sudo apt install openjdk-11-jre-headless

2. Cài Kafka
* sudo adduser kafka
* sudo adduser kafka sudo
* mkdir ~/Downloads
* curl "https://downloads.apache.org/kafka/2.6.2/kafka_2.13-2.6.2.tgz" -o ~/Downloads/kafka.tgz
* mkdir ~/kafka && cd ~/kafka
* tar -xvzf ~/Downloads/kafka.tgz --strip 1
* nano ~/kafka/config/server.properties
* Thêm delete.topic.enable = true
* sudo nano /etc/systemd/system/zookeeper.service
* Thêm nội dung dưới đây vào file

```
[Unit]
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
User=kafka
ExecStart=/home/kafka/kafka/bin/zookeeper-server-start.sh /home/kafka/kafka/config/zookeeper.properties
ExecStop=/home/kafka/kafka/bin/zookeeper-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

* sudo nano /etc/systemd/system/kafka.service
* Thêm nội dung dưới đây vào file

```
[Unit]
Requires=zookeeper.service
After=zookeeper.service

[Service]
Type=simple
User=kafka
ExecStart=/bin/sh -c '/home/kafka/kafka/bin/kafka-server-start.sh /home/kafka/kafka/config/server.properties > /home/kafka/kafka/kafka.log 2>&1'
ExecStop=/home/kafka/kafka/bin/kafka-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

* exit
* sudo deluser kafka sudo
* 
