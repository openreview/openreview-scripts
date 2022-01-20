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
    'Special Theme on Language Diversity: From Low Resource to Endangered Languages': 'Special_Theme',
    'PC Track': 'PC_Track'
    }

desk_rejected_invitation = client.post_invitation(openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/-/Desk_Rejected_Submission", 
    writers = ['aclweb.org/ACL/2022/Conference'],
    readers = ['aclweb.org/ACL/2022/Conference'],
    signatures = ['aclweb.org/ACL/2022/Conference'],
    reply = {
        "readers": {
            "values-regex": ".*"
            },
        "writers": {
            "values": [
            'aclweb.org/ACL/2022/Conference'
            ]
        },
    "signatures": {
        "values": [
        'aclweb.org/ACL/2022/Conference'
        ]
    },
    "content": {
    "authorids": {
        "values-regex": ".*"
        },
    "authors": {
        "values": [
            "Anonymous"
        ]
    }
}
}
))



# Get all ACL 2022 Conference blind submissions 
acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))
# For each blind submission, set the readers to the SAC track group 
for acl_blind_submission in acl_blind_submissions:
    acl_submission = client.get_note(acl_blind_submission.original)
    desk_reject = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/-/Desk_Reject",
        invitees = ["aclweb.org/ACL/2022/Conference/Program_Chairs","OpenReview.net/Support"],
        readers = ["everyone"],
        writers = ["aclweb.org/ACL/2022/Conference"],
        signatures = ["~Super_User1"],
        reply = {
            "forum": acl_blind_submission.forum,
            "replyto": acl_blind_submission.forum,
            "readers": {
                "values": [
                    "aclweb.org/ACL/2022/Conference"
                ]
                },
            "writers": {
                "values-copied": [
                    "aclweb.org/ACL/2022/Conference",
                    "{signatures}"
                ]
            },
            "signatures": {
                "values": [
                    "aclweb.org/ACL/2022/Conference/Program_Chairs"
                ],
                "description": "How your identity will be displayed."
                },
            "content": {
                "title": {
                    "value": "Submission Desk Rejected by Program Chairs",
                    "order": 1
                },
                "desk_reject_comments": {
                    "description": "Brief summary of reasons for marking this submission as desk rejected",
                    "value-regex": "[\\S\\s]{1,10000}",
                    "order": 2,
                    "required": True
                }
            }},
            process = './desk-reject-ACL-process.py'
                ))
   