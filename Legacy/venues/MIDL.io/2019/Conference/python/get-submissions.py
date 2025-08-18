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
import config

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output', help="The directory to save the output file")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connecting to "+client.baseurl)
conference = config.get_conference(client)

iterator = tools.iterget_notes(client, invitation=conference.get_submission_id())

notes = {}
for note in iterator:
    #print(note.number)
    notes[note.id]= {
        'submission': note,
        'reviews': [],
        'metareview':[],
    }

reviews = tools.iterget_notes(client, invitation=conference.get_id() + '/-/Paper.*/Official_Review')
for review in reviews:
    if review.forum in notes:
        notes[review.forum]['reviews'].extend([review.content['rating'][0],review.content['confidence'][0]])
    else:
        print("missing note for review "+review.forum)

metareviews = tools.iterget_notes(client, invitation=conference.get_id() + '/-/Paper.*/Meta_Review')
for meta in metareviews:
    if meta.forum in notes:
        notes[meta.forum]['metareview']=[meta.content['recommendation'],meta.content['confidence'][0]]
    else:
        print("missing meta "+meta.forum)

if args.output!=None:
    ext = args.output.split('.')[-1]
    if ext.lower()=='json':
        with open(args.output, 'w') as outfile:
            for n in notes:
                json.dump(n.to_json(), outfile, indent=4, sort_keys=True)

    elif ext.lower()=='csv':
        with open(args.output, 'w') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['id', 'number', 'title', 'R1 rate', 'R1 conf','R2 rate', 'R2 conf','R3 rate', 'R3 conf','AC rate', 'AC conf', 'Decision']
            csvwriter.writerow(fieldnames)

            for key in notes.keys():
                row = []
                row.append('%s/forum?id=%s' % (args.baseurl,notes[key]['submission'].forum))
                row.append(notes[key]['submission'].number)
                row.append(notes[key]['submission'].content['title'])
                row.extend(notes[key]['reviews'])
                row.extend(notes[key]['metareview'])
                csvwriter.writerow(row)

    else:
        print("Unrecognized file extension: "+ext)

else:
    for n in notes:
        print(json.dumps(n.to_json(), indent=4, sort_keys=True))
