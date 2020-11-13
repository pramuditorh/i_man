#!/bin/sh
# RUN db CONTAINER
docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
-e MYSQL_DATABASE=i_man -e MYSQL_USER=i_man \
-e MYSQL_PASSWORD=database \
mysql/mysql-server:5.7

sleep 35

# RUN i_man APP CONTAINER
docker run --name i_man -d -p 8000:5000 --rm -e SECRET_KEY=8bcd55ec519bc9f7 \
--link mysql:dbserver \
-e DATABASE_URL=mysql+pymysql://i_man:database@dbserver/i_man \
i_man:latest

sleep 3

docker container ls -a