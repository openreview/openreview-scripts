#!/usr/bin/python

###############################################################################
# Print csv file with basic paper info to help match w/ reviewers
# ex. python get-submissions.py --cpath MyConf.org/2017
# #                         --baseurl http://localhost:3000 --output submissions.csv
###############################################################################

## Import statements
import argparse
import csv
import sys
from openreview import *

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--cpath', required=True, help="conference path ex. MyConf.org/2017")
parser.add_argument('-o','--output', help="The directory to save the output file")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

## check conference directory exists
base_path = "../../venues/"+args.cpath
config_path = base_path+"/python/"
if os.path.isfile(config_path+"config.py") is False:
    print "Cannot locate config.py in:"+config_path
    sys.exit()
## load conference specific data
sys.path.insert(0, config_path)
import config

if args.baseurl == None:
    try:
        args.baseurl = os.environ['OPENREVIEW_BASEURL']
    except KeyError:
        print('OPENREVIEW_BASEURL not found. Please provide a base URL: ')

notes = openreview.get_notes(invitation=config.SUBMISSION)
if args.output!=None:
    ext = args.output.split('.')[-1]
    if ext.lower()=='json':
        with open(args.output, 'w') as outfile:
            for n in notes:
                json.dump(n.to_json(), outfile, indent=4, sort_keys=True)

    if ext.lower()=='csv':
        with open(args.output, 'wb') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['id', 'number', 'date', 'title', 'TL;DR', 'abstract','keywords','authors','authorids']
            csvwriter.writerow(fieldnames)

            for count, note in enumerate(notes):
                row = []
                row.append('%s/forum?id=%s' % (args.baseurl,note.id))
                row.append(note.number)
                row.append(note.tcdate)
                row.append(note.content['title'].encode('UTF-8'))
                row.append(note.content['TL;DR'].encode('UTF-8'))
                row.append(note.content['abstract'].encode('UTF-8'))
                row.append(', '.join(note.content['keywords']).encode('UTF-8'))
                row.append(', '.join(note.content['authors']).encode('UTF-8'))
                row.append(', '.join(note.content['authorids']).encode('UTF-8'))
                csvwriter.writerow(row)
else:
    for n in notes:
        print json.dumps(n.to_json(), indent=4, sort_keys=True)
