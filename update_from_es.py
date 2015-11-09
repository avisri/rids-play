#!/usr/bin/env python



from datetime import datetime
import json
from elasticsearch import Elasticsearch
import glob
import socket
import os

rids_dir="../rids/"
rids_dir_files=rids_dir+"[0-9]*[0-9]"

hostname=socket.gethostname()

def write_data(data):
    print "writing data:"
    print 'json/'+ data['_id']+ '.json'
    with open('json/'+ data['_id']+'.json', 'w') as f:
        json.dump(data, f)

def write_rids(data,):
    print "writing rid file:"
    print rids_dir+ data['_id']
    with open(rids_dir+data['_id'], 'w') as f:
      print "writing " + data['_source']['ridscounters']
      f.write(data['_source']['ridscounters'])
      f.close()

def read_data(data):
    with open('json/'+ data['_id']+'.json', 'r') as f:
        return(json.load(f))

def update_rids(data):
   print "updating rids"
   write_rids(data)

es = Elasticsearch()
# create an index in elasticsearch, ignore status code 400 (index already exists)
#es.indices.create(index='my-index', ignore=400)
# datetimes will be serialized
#es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})
# but not deserialized

clients=glob.glob(rids_dir_files)
print clients

for id in clients:
    
    data=es.get(index="rids", doc_type="clients",id=os.path.basename(id))
    print data
    #check only if last update master is not this host
    if data['_source']['lastupdate_master'] != hostname :
        #check save version , if not there save it first
        #write if rids has been updated
        try:
            sdata = read_data(data)
            print "read sucess " 
            #print sdata
            if data['_version'] >  sdata ['_version']:
                update_rids(data)
            elif (data['_version'] == sdata ['_version'] and
            data['_source']['ridscounters'] != sdata['_source']
            ['ridscounters']):
                print "same version different values"
                update_rids(data)
            else:
                print "same version %s, not updating rids" %(data['_version'])

        except IOError: 
            write_data(data)
            sdata = data
            print "read failure "
            #print sdata
            #update the rids file with new counters
            update_rids(data)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
