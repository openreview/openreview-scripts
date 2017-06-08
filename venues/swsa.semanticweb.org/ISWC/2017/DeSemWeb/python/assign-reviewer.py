import sys, os
import argparse
import openreview
import config

parser = argparse.ArgumentParser()
parser.add_argument('-a','--add',help="username or email address to add")
parser.add_argument('-r','--remove',help="username or email address to remove")
parser.add_argument('-t','--target',help="the paper number and anonreviewer number to assign. E.g. Paper2/AnonReviewer3", required=True)
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

anonreviewer = client.get_group(config.CONF + '/' + args.target)

if args.add:
	client.add_members_to_group(anonreviewer, args.add)
	print "%s added to group %s" % (args.add, args.target)
if args.remove:
	client.remove_members_from_group(anonreviewer, args.remove)
	print "%s removed from group %s" % (args.remove, args.target)
