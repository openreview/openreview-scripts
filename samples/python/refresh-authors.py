#!/usr/bin/python

###############################################################################
# ex. python refresh-authors.py --conf MyConf.org/2017 --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# To be run to refresh author groups in case of revisions and/or withdrawals
# Expects config to define BLIND_SUBMISSION, SUBMISSION and AUTHORS as well
# as an Authors group for each SUBMISSION paper
###############################################################################

## Import statements
import argparse
import sys
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-c','--conf', required=True, help = "the full path of the conference group ex. MyConf.org/2017")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

## check conference directory exists
base_path = "../../venues/"+args.conf
config_path = base_path+"/python/"
if os.path.isfile(config_path+"config.py") is False:
    print "Cannot locate config.py in:"+config_path
    sys.exit()
## load conference specific data
sys.path.insert(0, config_path)
import config

### update authors lists
all_authors = []
submissions_by_forum = {n.forum: n for n in client.get_notes(invitation=config.SUBMISSION)}
blinded = client.get_notes(invitation=config.BLIND_SUBMISSION)

for blind_note in blinded:
    #find associated note in Submissions to get true authors
    parent_forum = blind_note.original
    num_str = str(blind_note.number)
    note_authors = []
    found_profile = False
    note = submissions_by_forum[blind_note.original]

    # convert email ids to twiddle ids where possible
    for email in note.content['authorids']:
        email = email.lower()
        try:
            profile = client.get_profile(email)
            note_authors.append(profile.id)
            found_profile = True
            #print "found profile "+email
        except openreview.OpenReviewException as e:
            if e[0][0] == 'Profile not found':
                # no ~id, use the email
                note_authors.append(email)
            else:
                print "OpenReviewException: {0}".format(e)

    # if we don't have any profiles for the authorids,
    # add the ID of the person who submitted the paper.
    if found_profile == False:
        note_authors.append(note.signatures[0])

    # update paper author group
    author_group = client.get_group(config.CONF+"/Paper"+num_str+"/Authors")
    author_group.members = note_authors
    client.post_group(author_group)

    ## check for withdrawal
    if "withdrawal" not in blind_note.content or blind_note.content['withdrawal'] != "Confirmed":
        # Not withdrawn, therefore add to all_authors
        all_authors.extend(note_authors)



# remove duplicates
all_authors = list(set(all_authors))
print all_authors
# update conference authors group
all_authors_group = client.get_group(config.AUTHORS)
all_authors_group.members = all_authors
client.post_group(all_authors_group)