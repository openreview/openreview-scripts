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


papers = client.get_notes(invitation='auai.org/UAI/2018/-/Blind_Submission')

recommendations_by_forum = {}

for p in papers:
    recs = client.get_tags(invitation='auai.org/UAI/2018/-/Paper{}/Recommend_Reviewer'.format(p.number))
    recommendations_by_forum[p.id] = sorted(recs, key=lambda x: x.cdate)

metadata_notes = client.get_notes(invitation='auai.org/UAI/2018/-/Paper_Metadata')

def update_recommendation_score(metadata_note):

    user_scores = metadata_note.content['groups']['auai.org/UAI/2018/Program_Committee']
    recommendations = [e.tag for e in recommendations_by_forum.get(metadata_note.forum, [])]

    rank_score_map = [ 50.0 for i in range(len(recommendations)) ]
    '''
    rank_score_map

    this is a linear mapping between the recommended reviewer's position in the recommendation
    list (its "rank") and a "recommendation score" for the reviewer and that paper.
    '''
    for metadata_entry in user_scores:
        metadata_entry['scores'].pop('recommendation_score', None)
    
    for rank, userid in enumerate(recommendations):
        for metadata_entry in user_scores:
            if metadata_entry['userId'] in recommendations:
                metadata_entry['scores']['recommendation_score'] = float(rank_score_map[rank])
            else:
                metadata_entry['scores'].pop('recommendation_score', None)

    return metadata_note

for m in metadata_notes:
    m = update_recommendation_score(m)
    client.post_note(m)

print 'Done.'
