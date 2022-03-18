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


papers_to_move = {679:'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models', 253:'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models', 306:'Information Extraction', 6: 'Sentiment Analysis and Stylistic Analysis', 789: 'Dialogue and Interactive systems', 143: 'Machine Translation', 178: 'Question Answering', 847: 'Summarization', 993: 'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models', 81: 'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models', 289: 'Information Retrieval and Text Mining', 762: 'Syntax: Tagging, Chunking, and Parsing'}
for number, track in papers_to_move.items():
    original_submission = client.get_notes(invitation = 'aclweb.org/NAACL/2022/Conference/-/Submission', number = number)[0]
    original_submission.content['track'] = track 
    client.post_note(original_submission)
    author_id = f"aclweb.org/NAACL/2022/Conference/Commitment{number}/Authors"
    blind_submission = client.get_notes(invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission', number = number)[0]
    if len(blind_submission.readers) > 1: 
        blind_submission.content = {
            'track': track,
            'authorids': [author_id],
            'authors': ['Anonymous']
        }
        client.post_note(blind_submission)