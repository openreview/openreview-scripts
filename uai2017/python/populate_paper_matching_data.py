import argparse
from openreview import *
import sys, os
import time
import utils
sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
print sys.path
from note_content import *
from constants import *

import random
"""
Parse the arguments for user authentication
"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()
if args.username != None and args.password != None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

def create_sample_paper_metadata_note(notes):
    """
    Create a new invitation and supporting note for the paper meta data
    :param notes:
    :return:
    """
    papers = utils.get_paper_numbers(notes)
    reviewers = utils.get_all_reviewers(openreview,CONFERENCE_REVIEWERS)
    for i in range(len(notes)):
        inviter = CONFERENCE + "/-/matching"
        note = Note(invitation=inviter, cdate=int(time.time()) * 1000,
                    readers=[CONFERENCE_PCS, CONFERENCE_ACS],
                    forum=notes[i].id,
                    writers=['everyone'], content=PaperMetaData.create_samples(papers,reviewers,1)[0].to_dict(),
                    signatures=[CONFERENCE])
        openreview.post_note(note)

