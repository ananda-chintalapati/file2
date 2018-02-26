#!/usr/bin/env bash
useradd -m -d /home/tomcat/ -s /bin/bash tomcat
usermod -aG sudo tomcat
chown tomcat:tomcat -R /home/tomcat
sed -i '/#includedir/i tomcat ALL=(ALL) NOPASSWD: ALL' /etc/sudoers
