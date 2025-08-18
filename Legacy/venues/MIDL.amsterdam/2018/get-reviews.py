#!/usr/bin/python

###############################################################################
# Print csv file with basic review information (to help with acceptance decision
###############################################################################

## Import statements
import argparse
import csv
import sys
import openreview

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('track', help= "Abstract or Conference")
parser.add_argument('-o','--output', help="The output file")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

sys.path.append(args.track+'/python')
import config

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print "connected to "+client.baseurl

# review_info[paper_num][reviewer_id] = review
reviews = client.get_notes(invitation=config.CONFERENCE_ID+'/-/Paper.*/Official/Review')
review_info = {}
for review in reviews:
    paper_number = int(review.invitation.split('Paper')[-1].split('/')[0])
    if paper_number not in review_info:
        review_info[paper_number]={}
    review_info[paper_number][review.signatures[0]] = review

reviewer_by_anon = {}
anon_groups = client.get_groups(id=config.CONFERENCE_ID+'/Paper.*/AnonReviewer.*')
for anon_group in anon_groups:
    if len(anon_group.members) > 0:
        reviewer_by_anon[anon_group.id] = anon_group.members[0]

notes = client.get_notes(invitation=config.SUBMISSION)
if args.output!=None:
    ext = args.output.split('.')[-1]
    if ext.lower()=='json':
        with open(args.output, 'w') as outfile:
            for n in reviews:
                json.dump(n.to_json(), outfile, indent=4, sort_keys=True)

    elif ext.lower()=='csv':
        with open(args.output, 'wb') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['id', 'number', 'title', 'reviewer','score','review', 'confidence']
            csvwriter.writerow(fieldnames)

            for count, note in enumerate(notes):
                if note.number in review_info.keys():
                    for reviewer in review_info[note.number].keys():
                        row = []
                        row.append('%s/forum?id=%s' % (client.baseurl,note.id))
                        row.append(note.number)
                        row.append(note.content['title'].encode('UTF-8'))
                        row.append(reviewer_by_anon[reviewer].encode('UTF-8'))
                        row.append(review_info[note.number][reviewer].content['rating'].encode('UTF-8'))
                        row.append(review_info[note.number][reviewer].content['review'].encode('UTF-8'))
                        row.append(review_info[note.number][reviewer].content['confidence'].encode('UTF-8'))
                        csvwriter.writerow(row)

    else:
        print "Unrecognized file extension: "+ext

else:
    for n in reviews:
        print json.dumps(n.to_json(), indent=4, sort_keys=True)
