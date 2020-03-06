import argparse
import openreview
import csv
from tqdm import tqdm
import os

def get_valid_profiles(client, group_id):
    group = client.get_group(group_id)
    if not all(['~' in member for member in group.members]):
        print('WARNING: not all members of {0} have been converted to profile IDs.'.format(group_id))
    valid_tildes = [r for r in group.members if r.startswith('~')]
    return client.search_profiles(ids = valid_tildes)


## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

iclr_reviewers = client.get_group('ICLR.cc/2020/Conference/Reviewers')
eccv_reviewers = client.get_group('thecvf.com/ECCV/2020/Conference/Reviewers/Invited')
eccv_acs = client.get_group('thecvf.com/ECCV/2020/Conference/Area_Chairs/Invited')

cv_venues = [
    'dblp.org/conf/ECCV',
    'dblp.org/conf/ICCV',
    'dblp.org/conf/CVPR',
    'dblp.org/journals/IJCV'
]
def is_cv_venue(note):
    venueid = note.content['venueid']
    for c in cv_venues:
        if venueid.startswith(c):
            return True
    return False

cv_reviewers = []
for reviewer in tqdm(iclr_reviewers.members):
    content = {
      'authorids': reviewer
    }
    publications = openreview.tools.iterget_notes(client, content=content, invitation='dblp.org/-/record')
    cv_publications = list(filter(is_cv_venue, publications))
    if cv_publications:
        cv_reviewers.append(reviewer)

print('Total reviewers', len(cv_reviewers))

cv_invite_reviewers = list(set(cv_reviewers) - set(eccv_reviewers.members + eccv_acs.members))

print('Reviewers to invite', len(cv_invite_reviewers))

for c in cv_invite_reviewers:
    print(c)