#!/usr/bin/python

###############################################################################
# ex. python freeze-submissions.py --cid MyConf.org/2017 --baseurl http://localhost:3000
#       --username admin --password admin_pw
# run in same directory as config.py
# Prevents submissions from being edited or deleted.
# Change the submission invitation so reply writers of invitations can be set to []
# For each paper: change writers to []
###############################################################################

## Import statements
import argparse
import config
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--cid', required=True, help="conference id")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = Client(baseurl=args.baseurl)
baseurl = client.baseurl


## check conference directory exists
base_path = "../../venues/"+args.cid
config_path = base_path+"/python/"
if os.path.isfile(config_path+"config.py") is False:
    print "Cannot locate config.py in:"+config_path
    sys.exit()
sys.path.insert(0, config_path)
import config


###### update submission invite to allow setting writers set to []
# still allows new submissions that can't be edited
# the duedate determines whether or not new submissions can be added
invite = client.get_invitation(config.SUBMISSION)
invite.reply['writers']['values-regex'] = '(~.*)?'
client.post_invitation(invite)

submissions = client.get_notes(invitation=config.SUBMISSION)
for paper in submissions:
    paper.writers = []
    client.post_note(paper)
