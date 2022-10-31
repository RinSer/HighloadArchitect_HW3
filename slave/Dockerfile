# Galera Cluster Dockerfile
FROM ubuntu:18.04

ARG cnf

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y  software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv BC19DDBA
RUN add-apt-repository 'deb https://releases.galeracluster.com/galera-3/ubuntu bionic main'
RUN add-apt-repository 'deb https://releases.galeracluster.com/mysql-wsrep-5.7/ubuntu bionic main'

RUN apt-get update
RUN apt-get install -y galera-3 galera-arbitrator-3 mysql-wsrep-5.7 rsync

COPY $cnf /etc/mysql/my.cnf
RUN mkdir /var/run/mysqld
RUN chown -R mysql /var/run/mysqld
RUN mkdir /usr/local/mysql
RUN chown -R mysql /usr/local/mysql
USER mysql
RUN mysqld --initialize-insecure --explicit_defaults_for_timestamp
ENTRYPOINT ["mysqld"]