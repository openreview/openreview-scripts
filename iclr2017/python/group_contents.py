###############################################################################
# Group dump python script will simply print the contents of any given group.  
# PCs can run this as they wish to inspect the system.
###############################################################################

import sys
import requests
sys.path.append('../..')
from client import *

## Import statements and argument handling
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
parser.add_argument('group', help="the group to examine")
parser.add_argument('--output', help="the directory to save the output csv")
args = parser.parse_args()


## Initialize the client library with username and password
or3 = Client(args.username, args.password)

group = or3.get_group({'id':args.group})

print or3.pretty_json(group)