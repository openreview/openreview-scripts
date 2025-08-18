import sys, os
import argparse
import openreview
import config
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-a','--add',help="username or email address to add")
parser.add_argument('-r','--remove',help="username or email address to remove")
parser.add_argument('-n','--number',help="the paper number")
parser.add_argument('-f','--file', help="a csv file with rows formatted as follows: <forum, reviewer1, reviewer2, reviewer3>. There must be three reviewers per line.")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

def assign_reviewer(number, add, remove):
    anonreviewer = client.get_group(config.CONF + '/Paper%s/AnonReviewer' % number)
    reviewers = client.get_group(config.CONF + '/Paper%s/Reviewers' % number)
    if add:
        client.add_members_to_group(anonreviewer, add)
        client.add_members_to_group(reviewers, add)
        print "%s added to Paper%s" % (add, number)
    if remove:
        client.remove_members_from_group(anonreviewer, remove)
        client.remove_members_from_group(reviewers, remove)
        print "%s removed from Paper%s" % (remove, number)

if not args.file:
    assign_reviewer(args.number, args.add, args.remove)
else:
    with open(args.file, 'r') as assignments:
        reader = csv.reader(assignments)
        for row in reader:
            print row
            forum = row[0]
            r1 = row[1]
            r2 = row[2]
            r3 = row[3]

            note = client.get_note(forum)

            assign_reviewer(note.number, r1, None)
            assign_reviewer(note.number, r2, None)
            assign_reviewer(note.number, r3, None)

