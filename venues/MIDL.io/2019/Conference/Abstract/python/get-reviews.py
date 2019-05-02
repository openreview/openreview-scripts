#!/usr/bin/python

## Import statements
import argparse
import csv
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

def get_number(id_string):
    return id_string.split('/Paper')[1].split('/')[0]

with open(args.output, 'w') as outfile:
    csvwriter = csv.writer(outfile, delimiter=',')
    fieldnames = ['id', 'number', 'review title', 'review', 'rating', 'confidence', 'reviewer']
    csvwriter.writerow(fieldnames)

    notes = client.get_notes(invitation=conference.get_id() + '/-/Paper.*/Official_Review')
    for note in notes:
        row = []
        row.append('%s/forum?id=%s' % (client.baseurl, note.id))
        row.append(get_number(note.invitation))
        row.append(note.content['title'])
        row.append(note.content['review'])
        row.append(note.content['rating'].split(':')[0])
        row.append(note.content['confidence'].split(':')[0])
        row.append(note.tauthor)
        csvwriter.writerow(row)
