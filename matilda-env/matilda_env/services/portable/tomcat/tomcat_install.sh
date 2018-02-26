#!/usr/bin/env bash

tar xzf /tmp/jdk-8u162-linux-x64.tar.gz -C /home/tomcat
tar xzf /tmp/apache-tomcat-7.0.85.tar.gz -C /home/tomcat
echo "export JAVA_HOME=/home/tomcat/jdk1.8.0_162" >> /home/tomcat/.bash_profile
echo "export CATALINA_HOME=/home/tomcat/apache-tomcat-7.0.85" >> /home/tomcat/.bash_profile
source /home/tomcat/.bash_profile
$CATALINA_HOME/bin/startup.sh