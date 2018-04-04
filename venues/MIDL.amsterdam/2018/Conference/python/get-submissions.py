#!/usr/bin/python

###############################################################################
# Print csv file with basic paper info to help match w/ reviewers
# ex. python get-submissions.py --cpath MyConf.org/2017
# #                         --baseurl http://localhost:3000 --output submissions.csv
###############################################################################

## Import statements
import argparse
import csv
from openreview import *
import config

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output', help="The output file")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

notes = client.get_notes(invitation=config.SUBMISSION)
if args.output!=None:
    ext = args.output.split('.')[-1]
    if ext.lower()=='json':
        with open(args.output, 'w') as outfile:
            for n in notes:
                json.dump(n.to_json(), outfile, indent=4, sort_keys=True)

    elif ext.lower()=='csv':
        with open(args.output, 'wb') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['id', 'number', 'title', 'abstract','keywords','authors','authorids', 'author affiliations']
            csvwriter.writerow(fieldnames)

            for count, note in enumerate(notes):
                row = []
                row.append('%s/forum?id=%s' % (client.baseurl,note.id))
                row.append(note.number)
                row.append(note.content['title'].encode('UTF-8'))
                row.append(note.content['abstract'].encode('UTF-8'))
                row.append(', '.join(note.content['keywords']).encode('UTF-8'))
                row.append(', '.join(note.content['authors']).encode('UTF-8'))
                row.append(', '.join(note.content['authorids']).encode('UTF-8'))
                row.append(', '.join(note.content['author affiliation']).encode('UTF-8'))
                csvwriter.writerow(row)

    else:
        print "Unrecognized file extension: "+ext

else:
    for n in notes:
        print json.dumps(n.to_json(), indent=4, sort_keys=True)
