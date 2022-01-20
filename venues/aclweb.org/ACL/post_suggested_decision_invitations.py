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
    'Special Theme on Language Diversity: From Low Resource to Endangered Languages': 'Special_Theme'
}

suggested_decision_super = openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/-/Suggested_Decision",
    readers = ["everyone"], 
    writers = ["aclweb.org/ACL/2022/Conference"],
    signatures = ["aclweb.org/ACL/2022/Conference"],
    reply = {
        "readers":{
            "values-copied": [
                "aclweb.org/ACL/2022/Conference",
                "aclweb.org/ACL/2022/Conference/Senior_Area_Chairs"
                "{signatures}"
            ]
        },
        "writers":{
            "values-copied":[
                "aclweb.org/ACL/2022/Conference",
                "{signatures}"
            ]
        },
        "signatures":{
            "values-regex":"~.*"
        },
        "content": {
            "suggested_decision": {
                "order": 1,
                "value-radio": [
                    "1 - definite accept",
                    "2 - possible accept to main conference", 
                    "3 - possible accept to findings", 
                    "4 - reject"
                ],
                "description": "Please select your suggested decision",
                "required": True
                },
            "Justification": {
                "order": 3,
                "value-regex": "[\\S\\s]{1,200000}",
                "description": "Provide justification for your suggested decision. Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq.",
                "required": True,
                "markdown": True
                },
            "Ranking":{
                "order":2, 
                "value-regex": "^(5|\d)(\.\d{1,2})?$",
                "description": "If you selected options 2 or 3, provide a numerical score for the paper. It should be a number between 1 and 5 with up to 2 decimal places.",
                "required": False
            },
            "best_paper":{
                "order":4, 
                "values-checkbox": [
                    "Best Paper",
                    "Outstanding Paper"
                ],
                "description": "Do you consider this paper either the best or an outstanding paper?",
                "required": False
            }
            }
    }
    
)
client.post_invitation(suggested_decision_super)

acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))

for acl_blind_submission in acl_blind_submissions:
    acl_submission = client.get_note(acl_blind_submission.original)
    suggested_decision = client.post_invitation(openreview.Invitation(
    id = f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/-/Suggested_Decision",
    super = "aclweb.org/ACL/2022/Conference/-/Suggested_Decision",
    invitees = [f'aclweb.org/ACL/2022/Conference/{sac_name_dictionary[acl_submission.content["track"]]}/Senior_Area_Chairs', 'aclweb.org/ACL/2022/Conference/Program_Chairs'],
    signatures = ["aclweb.org/ACL/2022/Conference"],
    reply = {
        "forum": acl_blind_submission.forum,
        "replyto": acl_blind_submission.forum,
        "signatures": {
            "values-regex": f'aclweb.org/ACL/2022/Conference/{sac_name_dictionary[acl_submission.content["track"]]}/Senior_Area_Chairs',
            "description": "How your identity will be displayed."},
            "readers": {
                "values": [f'aclweb.org/ACL/2022/Conference/{sac_name_dictionary[acl_submission.content["track"]]}/Senior_Area_Chairs', 'aclweb.org/ACL/2022/Conference/Program_Chairs']
            },
            "writers": {
                "values": [f'aclweb.org/ACL/2022/Conference/{sac_name_dictionary[acl_submission.content["track"]]}/Senior_Area_Chairs', 'aclweb.org/ACL/2022/Conference/Program_Chairs']
            }

    }
))