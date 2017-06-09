import sys, os
import argparse
import openreview
import config

parser = argparse.ArgumentParser()
parser.add_argument('-a','--add',help="username or email address to add")
parser.add_argument('-r','--remove',help="username or email address to remove")
parser.add_argument('-n','--number',help="the paper number", required=True)
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

anonreviewer = client.get_group(config.CONF + '/Paper%s/AnonReviewer' % args.number)
reviewers = client.get_group(config.CONF + '/Paper%s/Reviewers' % args.number)
if args.add:
	client.add_members_to_group(anonreviewer, args.add)
	client.add_members_to_group(reviewers, args.add)
	print "%s added to Paper%s" % (args.add, args.number)
if args.remove:
	client.remove_members_from_group(anonreviewer, args.remove)
	client.remove_members_from_group(reviewers, args.remove)
	print "%s removed from Paper%s" % (args.remove, args.number)
