This folder is for testing MQTT Client and MongoDB.
These program capture data from MQTT broker that Anko IPC transfer data to MQTT broker.
And then these can store raw data to MySQL and create json data and store it to MongoDB.

//------------------------------------------------------------------

install MQTT
https://swf.com.tw/?p=1007

install: brew install mosquitto
conf file: /opt/homebrew/etc/mosquitto/mosquitto.conf
To start mosquitto now and restart at login:
  brew services start mosquitto
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf

  ==> mosquitto
mosquitto has been installed with a default configuration file.
You can make changes to the configuration by editing:
    /opt/homebrew/etc/mosquitto/mosquitto.conf

To start mosquitto now and restart at login:
  brew services start mosquitto
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf
==> mysql
We've installed your MySQL database without a root password. To secure it run:
    mysql_secure_installation

MySQL is configured to only allow connections from localhost by default

To connect run:
    mysql -u root

To restart mysql after an upgrade:
  brew services restart mysql
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/mysql/bin/mysqld_safe --datadir\=/opt/homebrew/var/mysql

modify listener
https://stackoverflow.com/questions/45260068/setting-up-mosquitto-on-home-server
https://swf.com.tw/?p=1473#google_vignette


MQTT Client
https://mqttx.app/

//------------------------------------------------------------------

install MongoDB
https://treehouse.github.io/installation-guides/mac/mongo-mac.html
https://make9.tw/wp-shorthand/other/%E5%9C%A8-mac-%E6%9C%AC%E6%A9%9F%E5%AE%89%E8%A3%9D-mongodb-%E7%9A%84%E6%AD%A5%E9%A9%9F/


#brew install mongodb
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
brew services start mongodb/brew/mongodb-community


