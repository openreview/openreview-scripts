import argparse
import os
import openreview
import csv
from openreview import tools
from tqdm import tqdm

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

desk_reject_invitations = list(tools.iterget_invitations(client, regex='NeurIPS.cc/2022/Conference/Paper.*/-/Desk_Reject'))
print('#',len(desk_reject_invitations), 'desk-reject invitations')

for invitation in tqdm(desk_reject_invitations):
    paper_group = invitation.id.split('/-/')[0]

    with open(os.path.join(os.path.dirname(__file__), './updated_desk_reject_process.py')) as f:
        
        file_content = f.read()
        file_content = file_content.replace('CONFERENCE_ID = \'\'','CONFERENCE_ID = \'NeurIPS.cc/2022/Conference\'')
        file_content = file_content.replace('CONFERENCE_SHORT_NAME = \'\'','CONFERENCE_SHORT_NAME = \'NeurIPS 2022\'')
        file_content = file_content.replace('CONFERENCE_NAME = \'\'','CONFERENCE_NAME = \'Thirty-Sixth Conference on Neural Information Processing Systems\'')
        file_content = file_content.replace('CONFERENCE_YEAR = \'\'','CONFERENCE_YEAR = \'2022\'')
        file_content = file_content.replace('PAPER_AUTHORS_ID = \'\'','PAPER_AUTHORS_ID = \'' + paper_group +'/Authors\'')
        file_content = file_content.replace('PAPER_REVIEWERS_ID = \'\'','PAPER_REVIEWERS_ID = \'' + paper_group +'/Reviewers\'')
        file_content = file_content.replace('PAPER_AREA_CHAIRS_ID = \'\'','PAPER_AREA_CHAIRS_ID = \'' + paper_group +'/Area_Chairs\'')
        file_content = file_content.replace('PAPER_SENIOR_AREA_CHAIRS_ID = \'\'','PAPER_SENIOR_AREA_CHAIRS_ID = \'' + paper_group +'/Senior_Area_Chairs\'')
        file_content = file_content.replace('PROGRAM_CHAIRS_ID = \'\'','PROGRAM_CHAIRS_ID = \'NeurIPS.cc/2022/Conference/Program_Chairs\'')
        file_content = file_content.replace('DESK_REJECTED_SUBMISSION_ID = \'\'','DESK_REJECTED_SUBMISSION_ID = \'NeurIPS.cc/2022/Conference/-/Desk_Rejected_Submission\'')
        file_content = file_content.replace('BLIND_SUBMISSION_ID = \'\'','BLIND_SUBMISSION_ID = \'NeurIPS.cc/2022/Conference/-/Blind_Submission\'')
        file_content = file_content.replace('SUBMISSION_READERS = []',str.format('SUBMISSION_READERS = {}', ['NeurIPS.cc/2022/Conference', paper_group + '/Authors']))

    invitation.process=file_content
    inv = client.post_invitation(invitation)
