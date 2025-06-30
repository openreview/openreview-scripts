
import argparse
import openreview

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)
print client.baseurl

# pull authors off of non-readers for reviews
groups = client.get_groups('auai.org/UAI/2018/Paper.*/Reviewers/Unsubmitted')
for group in groups:
    paper_num = group.id.split('Paper')[-1].split('/')[0]
    authors = 'auai.org/UAI/2018/Paper'+paper_num+'/Authors'
    client.remove_members_from_group(group, [authors])

# add authors, area chairs, reviewers to final decision
decisions = client.get_notes(invitation='auai.org/UAI/2018/-/Paper.*/Final_Decision')

for note in decisions:
    paper_num = note.invitation.split('Paper')[-1].split('/')[0]
    authors = 'auai.org/UAI/2018/Paper{0}/Authors'.format(paper_num)
    reviewers = 'auai.org/UAI/2018/Paper{0}/Reviewers'.format(paper_num)
    acs = 'auai.org/UAI/2018/Paper{0}/Area_Chairs'.format(paper_num)
    note.readers.extend([authors, reviewers, acs])
    client.post_note(note)