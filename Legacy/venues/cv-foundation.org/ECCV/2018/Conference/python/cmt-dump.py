#!/usr/bin/python

import argparse
import openreview
import csv
import datetime
import xml.etree.cElementTree as ET

now = datetime.date.today()
datestring = '{:0>4}-{:0>2}-{:0>2}'.format(now.year, now.month, now.day)

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--label', required=True)
parser.add_argument('-o','--outfile', default = '../data/{}-cmt-dump.xml'.format(datestring))
parser.add_argument('-i','--infile', default='../data/areachairs.csv')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

print "collecting data from {}".format(client.baseurl)
papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
all_assignments = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Assignment')
assignments = [a for a in all_assignments if a.content['label'] == args.label]
assignment_by_forum = {n.forum: n for n in assignments}

print "reading emails from {}".format(args.infile)
emails_by_id = {}
with open(args.infile) as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        email = row[3].lower()
        profile = client.get_profiles([email]).values()[0]
        emails_by_id[profile.id] = email

root = ET.Element("assignments")

for paper in papers:
    assignment = assignment_by_forum[paper.id]
    paperid = paper.content['paperId']
    assignment_entries = assignment.content['assignedGroups']

    doc = ET.SubElement(root, "submission", submissionId = paperid)
    for entry in assignment_entries:
        ET.SubElement(doc, "user", email=emails_by_id[entry['userId']])


indent(root)
tree = ET.ElementTree(root)
print "writing {}".format(args.outfile)

with open(args.outfile, 'w') as f:
    f.write('<?xml version="1.0"?>\n')
    f.write(ET.tostring(root))

#tree.write(args.outfile)

