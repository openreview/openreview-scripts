import argparse
from openreview import *
import sys, os
import time
import utils

sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
print sys.path
from note_content import *
from constants import *

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


def create_reviewer_data_notes(samples_reviewer_data):
    """
    Create a new invitation and supporting note for the reviewer data
    :param samples_reviewer_data:
    :return:
    """
    reviewer_invitation = Invitation(CONFERENCE,
                                          'reviewer', signatures=[CONFERENCE], readers=['everyone'],
                                          writers=['everyone'], reply=INVITATION_REPLY)
    openreview.post_invitation(reviewer_invitation)
    for reviewer_data in samples_reviewer_data:
        note = Note(invitation=reviewer_invitation.id, cdate=int(time.time()) * 1000, readers=['everyone',reviewer_data.name],
                    writers=['everyone',reviewer_data.name], content=reviewer_data.to_dict(), signatures=reviewer_invitation.signatures)
        openreview.post_note(note)



if __name__ == '__main__':
    if openreview.user['id'].lower() == 'openreview.net':
        #Manually updating the reviewers data
        members=utils.get_all_member_ids(openreview)
        utils.update_reviewers(openreview,CONFERENCE_REVIEWERS,members)
        papers = utils.get_paper_numbers(utils.get_notes_submitted_papers(openreview,CONFERENCE_SUBMISSION))
        samples_reviewer_data = ReviewerData.create_samples(papers,members,3)
        #Creating reviewer note for each reviewer
        create_reviewer_data_notes(samples_reviewer_data)
        notes = utils.get_reviewer_data_notes(openreview,CONFERENCE)
        for note in notes:
            print json.dumps(note.content)
    else:
        print "Aborted. User must be Super User."
