#!/usr/bin/env bash

tar xzf /tmp/mysql-5.7.21-el7-x86_64.tar.gz -C /usr/local
ln -s mysql-5.7.21-el7-x86_64 mysql
mkdir /usr/local/mysql/mysql-files
chmod 755 /usr/local/mysql/mysql-files
/usr/local/mysql/bin/mysqld --initialize
/usr/local/mysql/bin/mysqld_safe &