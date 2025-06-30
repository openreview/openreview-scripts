#!/usr/bin/python

###############################################################################
# ex. python freeze-submissions.py --cpath MyConf.org/2017 --baseurl http://localhost:3000
#       --username admin --password admin_pw
# Prevents submissions from being edited or deleted.
# Change the submission invitation so reply writers of invitations can be set to []
# For each paper: change writers to []
###############################################################################

## Import statements
import argparse
import sys
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--cpath', required=True, help="conference path ex. MyConf.org/2017")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

## check conference directory exists
base_path = "../../venues/"+args.cpath
config_path = base_path+"/python/"
if os.path.isfile(config_path+"config.py") is False:
    print "Cannot locate config.py in:"+config_path
    sys.exit()
## load conference specific data
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
