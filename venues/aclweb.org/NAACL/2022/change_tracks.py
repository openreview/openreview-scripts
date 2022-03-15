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
print('Load SAC groups')
track_SAC_profiles = {}
track_groups = { group.id: group for group in client.get_groups('aclweb.org/NAACL/2022/Conference/.*/Senior_Area_Chairs')}
profile_ids = []
for track_name, group_abbreviation in sac_name_dictionary.items():
    #print(track_name)
    group = track_groups[f'aclweb.org/NAACL/2022/Conference/{group_abbreviation}/Senior_Area_Chairs']
    profile_ids = profile_ids + group.members

print(f'Load SAC {len(list(set(profile_ids)))} profiles')
SAC_profiles = { p.id: p for p in openreview.tools.get_profiles(client, list(set(profile_ids)), with_publications = True)}
    # profiles = openreview.tools.get_profiles(client, group.members, with_publications = True)
    # track_SAC_profiles[track_name] = profiles

papers_to_move = {679:'Machine Learning for NLP: Language Modeling', 253:'Machine Learning for NLP: Language Modeling', 306:'Information Extraction', 6: 'Sentiment Analysis', 789: 'Dialogue and Interactive systems', 143: 'Machine Translation', 178: 'Question Answering', 847: 'Summarization', 993: 'Machine Learning for NLP: Language Modeling', 81: 'Machine Learning for NLP: Language Modeling', 289: 'Information retrieval', 762: 'Syntax'}
for paper in papers_to_move: 
    # compute conflicts between paper and new track SACs and add them to paper conflicts 
    # Change review and metareview readers to include correct track 
    # If paper readers isn't everyone, change paper readers to include correct track
    for SAC in track_groups[f"aclweb.org/NAACL/2022/Conference/{sac_name_dictionary[acl_submission.content['track']]}/Senior_Area_Chairs"].members:
        #print(SAC)
        conflicts = openreview.tools.get_conflicts(author_group, SAC_profiles[SAC], policy = 'neurips', n_years=5)
        if conflicts:
            conflict_members.append(SAC)