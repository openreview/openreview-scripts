import argparse
from openreview import *
import sys, os
import time

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


def update_reviewers(members):
    """
    Update the members of the group
    :param members:
    :return:
    """
    reviewers = openreview.get_group(CONFERENCE_REVIEWERS)
    reviewers.members = members
    openreview.post_group(reviewers)


def create_reviewer_metadata_note(reviewer_sample_meta):
    """
    Create a new invitation and supporting note for the reviewer meta data
    :param reviewer_sample_meta:
    :return:
    """
    reviewers = openreview.get_group(CONFERENCE_REVIEWERS)
    members = reviewers.members
    reviewer_meta_invitation = Invitation(CONFERENCE_REVIEWERS,
                                          'metadata', signatures=[CONFERENCE_REVIEWERS], readers=['everyone'],
                                          writers=['everyone'], reply=INVITATION_REPLY)
    openreview.post_invitation(reviewer_meta_invitation)
    for member in members:
        note = Note(invitation=reviewer_meta_invitation.id, cdate=int(time.time()) * 1000, readers=['everyone'],
                    writers=['everyone'], content=reviewer_sample_meta, signatures=reviewer_meta_invitation.signatures)
        openreview.post_note(note)


def get_reviewer_metadata_notes():
    """
    Get all the reviewer meta data notes
    :return:
    """
    notes = openreview.get_notes(invitation=CONFERENCE_REVIEWERS + "/-/metadata")
    return notes


if __name__ == '__main__':
    if openreview.user['id'].lower() == 'openreview.net':
        samples_reviewer_meta_data= ReviewerMeta.create_samples(3)
        for reviewer_meta_data in samples_reviewer_meta_data:
            create_reviewer_metadata_note(reviewer_sample_meta=reviewer_meta_data.to_dict())
        notes = get_reviewer_metadata_notes()
        for note in notes:
            print json.dumps(note.content)
    else:
        print "Aborted. User must be Super User."
