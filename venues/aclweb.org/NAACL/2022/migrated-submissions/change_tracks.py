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
    


papers_to_move = {679:'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models', 253:'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models', 306:'Information Extraction', 6: 'Sentiment Analysis and Stylistic Analysis', 789: 'Dialogue and Interactive systems', 143: 'Machine Translation', 178: 'Question Answering', 847: 'Summarization', 993: 'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models', 81: 'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models', 289: 'Information Retrieval and Text Mining', 762: 'Syntax: Tagging, Chunking, and Parsing'}
for number, track in papers_to_move.items():
    authors = client.get_group(f'aclweb.org/NAACL/2022/Conference/Commitment{number}/Authors')
    author_group = openreview.tools.get_profiles(client, ids_or_emails = authors.members, with_publications=True)
    blind_submission = client.get_notes(invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission', number = number)[0]
    
    conflict_group = client.get_group(f'aclweb.org/NAACL/2022/Conference/Commitment{number}/Conflicts')
    # compute conflicts between paper and new track SACs and add them to paper conflicts 
    # Change review and metareview readers to include correct track 
    # If paper readers isn't everyone, change paper readers to include correct track
    conflict_members = []
    for SAC in track_groups[f"aclweb.org/NAACL/2022/Conference/{sac_name_dictionary[track]}/Senior_Area_Chairs"].members:
        #print(SAC)
        conflicts = openreview.tools.get_conflicts(author_group, SAC_profiles[SAC], policy = 'neurips', n_years=5)
        if conflicts:
            conflict_members.append(SAC)
    if conflict_members: 
        conflict_group.members = conflict_group.members + conflict_members
        client.post_group(conflict_group)
    
    if len(blind_submission.readers) > 1: 
        blind_submission.readers = [confid, 
        f'{confid}/Program_Chairs',
        f'{confid}/{sac_name_dictionary[track]}/Senior_Area_Chairs'
        ]
        client.post_note(blind_submission)

    # fix review/metareview track readers 
    reviews = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/ARR_Official_Review', forum = blind_submission.forum))
    reviews = reviews + (list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/ARR_Meta_Review', forum = blind_submission.forum)))
    for review in reviews: 
        review.readers = [
            f'{confid}/Program_Chairs',
            f'{confid}/{sac_name_dictionary[track]}/Senior_Area_Chairs'
        ]
        client.post_note(review)
    
    # fix comment readers 
    try:
        comment = (client.get_notes(invitation=f"aclweb.org/NAACL/2022/Conference/Commitment{number}/-/Comment_by_Authors"))[0]
        comment_invitation = client.get_invitation(f"aclweb.org/NAACL/2022/Conference/Commitment{number}/-/Comment_by_Authors")
        comment_invitation.reply['readers']['values'] = [f'{confid}/Program_Chairs',
            f'{confid}/{sac_name_dictionary[track]}/Senior_Area_Chairs']
        client.post_invitation(comment_invitation)
        comment.readers = [ 
            f'{confid}/Program_Chairs',
            f'{confid}/{sac_name_dictionary[track]}/Senior_Area_Chairs'
        ]
        client.post_note(comment)
    except: 
        print(f'no comment by authors found for {number} forum {blind_submission.forum}')
    