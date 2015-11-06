#!/bin/bash

set -o errexit
master=`hostname -s`
id=${1:? need proper id } 
counters=`cat $id`
date=`date +%s`
curl -XPOST  localhost:9200/rids/$id -d '{ "@timestamp":'$date', "ridscounters" : "'$counters'", "lastupdate_master" : "'$master'"  }'
#vim set ts=3 tw=3 sw=3
