#!/bin/bash

set -o errexit
id=${1:? need proper id } 
counters=${2:-`cat $id`}
master=${3:-`hostname -s`}
date=`date +%s`
curl -XPOST  localhost:9200/rids/clients/$id -d '{ "@timestamp":'$date', "ridscounters" : "'$counters'", "lastupdate_master" : "'$master'"  }'
#vim set ts=3 tw=3 sw=3
