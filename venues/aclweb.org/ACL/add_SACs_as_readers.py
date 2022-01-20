import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv

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

# Creating SAC groups from Track Name 
sac_name_dictionary = {
    'Ethics in NLP': 'Ethics_NLP', 
    'Linguistic theories, Cognitive Modeling and Psycholinguistics': 'LCMP', 
    'Linguistic Theories, Cognitive Modeling and Psycholinguistics': 'LCMP',
    'Machine Learning for NLP': 'Machine_Learning_NLP', 
    'Phonology, Morphology and Word Segmentation': 'Phonology_Morphology_Word_Segmentation', 
    'Resources and Evaluation': 'Resources_Evaluation', 
    'Semantics: Lexical': 'Semantics_Lexical', 
    'Semantics: Sentence level, Textual Inference and Other areas': 'Semantics_STO', 
    'Syntax: Tagging, Chunking and Parsing': 'Syntax_TCP', 
    'Information Extraction': 'Information_Extraction', 
    'Computational Social Science and Cultural Analytics': 'CSSCA', 
    'Information Retrieval and Text Mining': 'Info_Retrieval_Text_Mining', 
    'Interpretability and Analysis of Models for NLP': 'IAM_for_NLP', 
    'Machine Translation and Multilinguality': 'Machine_Translation_Multilinguality', 
    'NLP Applications': 'NLP_Applications', 
    'Question Answering': 'Question_Answering', 
    'Dialogue and Interactive Systems': 'Dialogue_and_Interactive_Systems', 
    'Discourse and Pragmatics': 'Discourse_and_Pragmatics', 
    'Generation': 'Generation', 
    'Language Grounding to Vision, Robotics, and Beyond': 'LGVRB', 
    'Sentiment Analysis, Stylistic Analysis, and Argument Mining': 'SASAAM', 
    'Speech and Multimodality': 'Speech_and_Multimodality', 
    'Summarization': 'Summarization', 
    'Special Theme on Language Diversity: From Low Resource to Endangered Languages': 'Special_Theme'
    }

acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))
acl_meta_reviews = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Meta_Review'))
acl_reviews = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Official_Review'))
reviews_by_forum = {}
for metareview in acl_meta_reviews:
    if metareview.forum in reviews_by_forum: 
        reviews_by_forum[metareview.forum].append(metareview)
    else:
        reviews_by_forum[metareview.forum] = [metareview]
for review in acl_reviews:
    if review.forum in reviews_by_forum: 
        reviews_by_forum[review.forum].append(review)
    else:
        reviews_by_forum[review.forum] = [review]

# For each blind submission, set the readers to the SAC track group 
for acl_blind_submission in acl_blind_submissions:
    acl_submission = client.get_note(acl_blind_submission.original)
    acl_blind_submission.readers.append(f'aclweb.org/ACL/2022/Conference/{sac_name_dictionary[acl_submission.content["track"]]}/Senior_Area_Chairs')
    acl_blind_submission.content = {
        'authors': ['Anonymous'],
        'authorids': [f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors']
    }
    client.post_note(acl_blind_submission)
    reviews = reviews_by_forum[acl_blind_submission.forum]
    for review in reviews: 
        review.readers.append(f'aclweb.org/ACL/2022/Conference/{sac_name_dictionary[acl_submission.content["track"]]}/Senior_Area_Chairs')
        client.post_note(review)