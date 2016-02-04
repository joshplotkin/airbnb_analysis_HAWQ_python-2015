#!/bin/bash

sudo -u hdfs hadoop fs -mkdir /airbnb
sudo -u hdfs hadoop fs -put listings.csv /airbnb

sudo -u gpadmin -i psql -f DDL.sql
