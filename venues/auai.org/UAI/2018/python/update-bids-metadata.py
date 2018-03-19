import openreview
import random
import argparse
import requests
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)


tags = client.get_tags(invitation='auai.org/UAI/2018/-/Add_Bid')

bid_score_map = {
    'I want to review': 1.0,
    'I can review': 0.75,
    'I can probably review but am not an expert': 0.5,
    'I cannot review': -20,
    'No bid': 0.0
}

bids = {}
for a in tags:
    if a.forum not in bids:
        bids[a.forum] = {}
    bids[a.forum][a.signatures[0]] = bid_score_map.get(a.tag, 0)


metadata_notes = client.get_notes(invitation='auai.org/UAI/2018/-/Paper_Metadata')


def update_bid_score(user_scores):
    for s in user_scores:
        bid_score = bids[m.forum].get(s['userId'], 0)
        if bid_score:
            s['scores']['bid_score'] = bid_score
        else:
            s['scores'].pop('bid_score', None)
    return user_scores

for m in metadata_notes:
    #Area chairs
    ac_scores = m.content['groups']['auai.org/UAI/2018/Senior_Program_Committee']
    m.content['groups']['auai.org/UAI/2018/Senior_Program_Committee'] = update_bid_score(ac_scores)


    #Reviewers
    r_scores = m.content['groups']['auai.org/UAI/2018/Program_Committee']
    m.content['groups']['auai.org/UAI/2018/Program_Committee'] = update_bid_score(r_scores)

    client.post_note(m)

print 'Done.'
