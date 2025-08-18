#!/usr/bin/python

###############################################################################
# Print csv file with basic paper info to help match w/ reviewers
# ex. python get-submissions.py --cpath MyConf.org/2017
# #                         --baseurl http://localhost:3000 --output submissions.csv
###############################################################################

## Import statements
import argparse
import csv
import openreview
import config

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output', help="The directory to save the output file")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print('connecting to {0}'.format(client.baseurl))

conference = config.get_conference(client)

notes = client.get_notes(invitation=conference.get_id()+'/-/Submission')
if args.output!=None:
    ext = args.output.split('.')[-1]
    if ext.lower()=='csv':
        with open(args.output, 'w') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['id', 'number', 'date', 'title', 'abstract','keywords','authors','authorids']
            csvwriter.writerow(fieldnames)

            for note in notes:
                row = []
                row.append('%s/forum?id=%s' % (client.baseurl,note.id))
                row.append(note.number)
                row.append(note.tcdate)
                row.append(note.content['title'])
                row.append(note.content['abstract'])
                row.append(', '.join(note.content['keywords']))
                row.append(', '.join(note.content['authors']))
                row.append(', '.join(note.content['authorids']))
                csvwriter.writerow(row)

    else:
        print("Unrecognized file extension: "+ext)
