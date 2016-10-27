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


def get_notes_submitted_papers():
    """
    Get all the submitted papers
    :return:
    """
    notes = openreview.get_notes(invitation=CONFERENCE_SUBMISSION)
    return notes


def get_paper_names(notes):
    """
    Getting paper name using the following logic: If note.number is NONE then use 0 as default else 'Paper' followed by its number
    :param notes:
    :return:
    """
    list_paper_name = []
    for note in notes:
        if (note.number is None):
            list_paper_name.append("Paper0")
        else:
            list_paper_name.append("Paper" + str(note.number))
    return list_paper_name


def create_paper_groups(notes):
    """
    Creating a group for each paper name
    :param notes:
    :return:
    """
    paper_names = get_paper_names(notes)
    for paper_name in paper_names:
        group_id = CONFERENCE + "/" + paper_name
        g = Group(group_id, readers=['everyone'],
                  writers=[CONFERENCE, CONFERENCE_PCS],
                  signatures=[CONFERENCE],
                  signatories=[CONFERENCE_REVIEWERS])
        print "Posting group: ", g.id
        openreview.post_group(g)


def create_paper_metadata_note(notes):
    """
    Create a new invitation and supporting note for the paper meta data
    :param paper_sample_meta:
    :return:
    """
    paper_names = get_paper_names(notes)
    for i in range(len(notes)):
        inviter = CONFERENCE + "/" + paper_names[i]
        paper_meta_invitation = Invitation(inviter, 'matching', signatures=[CONFERENCE_PCS],
                                           readers=['everyone'],
                                           writers=['everyone'], reply=INVITATION_REPLY)
        openreview.post_invitation(paper_meta_invitation)
        note = Note(invitation=paper_meta_invitation.id, cdate=int(time.time()) * 1000,
                    readers=[CONFERENCE_PCS, CONFERENCE_ACS],
                    writers=['everyone'], content=PaperMetaData.create_samples(1)[0].to_dict(),
                    signatures=[CONFERENCE])
        openreview.post_note(note)


def get_paper_metadata_notes(paper_names):
    """
    Get all submitted paper meta data notes
    :return:
    """
    notes = [openreview.get_notes(invitation=CONFERENCE + "/" + paper_name + "/-/matching")[0] for paper_name in
             paper_names]
    return notes


if __name__ == '__main__':
    if openreview.user['id'].lower() == 'openreview.net':
        notes = get_notes_submitted_papers()
        paper_names = get_paper_names(notes)
        # Creating groups for all submitted papers
        create_paper_groups(notes)
        # Creating invitations and notes for all submitted papers
        create_paper_metadata_note(notes)
        # Printing all the paper meta data notes
        notes_meta = get_paper_metadata_notes(paper_names)
        for note in notes_meta:
            content = note.content
            print json.dumps(note.content)
    else:
        print "Aborted. User must be Super User."
