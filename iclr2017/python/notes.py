###############################################################################
# Note dump python script will simply print the contents of papers/reviews/
# comments matching certain criteria. PCs can run this as they wish to inspect 
# the system.
###############################################################################

# This script depends on being able to search by prefix

import sys
import requests
sys.path.append('../..')
from client import *

## Import statements and argument handling
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
parser.add_argument('--id', help="Id of the note to examine")
parser.add_argument('--invitation','-inv', help="Notes that respond to this invitation")
parser.add_argument('--output', '-o',help="the directory to save the output csv")
args = parser.parse_args()


## Initialize the client library with username and password
or3 = Client(args.username, args.password)

data = {}

if args.id != None:
	data['id']=args.id
if args.invitation != None:
	data['invitation']=args.invitation

note = or3.get_note(data)

if args.output!=None:
	with open(args.output, 'w') as outfile:
		json.dump(json.loads(note.text), outfile, indent=4, sort_keys=True)
else:
	print json.dumps(json.loads(note.text), indent=4, sort_keys=True)
