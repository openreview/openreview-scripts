import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv
import tracks

"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password

"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
confid = 'aclweb.org/NAACL/2022/Conference'
sac_name_dictionary = tracks.sac_name_dictionary
blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission'))
original_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/Submission'))
commitment_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/Commitment_Submission'))
commitment_by_forum = {commit.forum:commit for commit in commitment_submissions}
original_by_forum = {original.id: original for original in original_submissions}
comment_super = openreview.Invitation(
    id = "aclweb.org/NAACL/2022/Conference/-/Comment_by_Authors",
    readers = ["everyone"],
    writers = ["aclweb.org/NAACL/2022/Conference"],
    signatures = ["aclweb.org/NAACL/2022/Conference"],
    reply = {
    "content": {
        "title": {
            "order": 0,
            "value-regex": ".{1,500}",
            "description": "Brief summary of your comment.",
            "required": True
        },
        "comment": {
            "order": 1,
            "value-regex": "[\\S\\s]{1,5000}",
            "description": "Your comment or reply (max 5000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
            "required": True,
            "markdown": True
        }
    }
}

)
client.post_invitation(comment_super)


for blind_submission in tqdm(blind_submissions):
    original_submission = original_by_forum[blind_submission.original] 
    sac_id = f'aclweb.org/NAACL/2022/Conference/{sac_name_dictionary[original_submission.content["track"]]}/Senior_Area_Chairs'
    pc_id = 'aclweb.org/NAACL/2022/Conference/Program_Chairs'
    author_id = f'aclweb.org/NAACL/2022/Conference/Commitment{blind_submission.number}/Authors'
    commitment_forum = original_submission.content['commitment_note'].split('=')[1]
    commitment_note = commitment_by_forum[commitment_forum]
    if commitment_note.content.get('optional_comments'):
        comment = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/NAACL/2022/Conference/Commitment{blind_submission.number}/-/Comment_by_Authors",
        super = "aclweb.org/NAACL/2022/Conference/-/Comment_by_Authors",
        invitees = [confid], # Is this right? 
        signatures = ["aclweb.org/NAACL/2022/Conference"],
        reply = {
            "forum": blind_submission.forum,
            "replyto": blind_submission.forum,
            "readers": {
                "values": [pc_id, sac_id]
            },
            "signatures": {
                "values": [author_id]
            },
            "writers": {
                "values": [confid]
            },
            "nonreaders": {
                "values": blind_submission.nonreaders
            }
        }
    ))
        client.post_note(openreview.Note(
            invitation = f'aclweb.org/NAACL/2022/Conference/Commitment{blind_submission.number}/-/Comment_by_Authors',
            readers = [
                sac_id, 
                pc_id
            ],
            writers = [confid],
            signatures = [ 
                author_id
            ],
            forum = blind_submission.forum,
            nonreaders=blind_submission.nonreaders,
            content = {
                'title': 'Comment to the Senior Area Chairs by Paper Authors',
                'comment': commitment_note.content['optional_comments']
            }
        ))