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


# Posting submission invitation 
submission_invitation = openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/-/Submission",
    signatures = ["aclweb.org/ACL/2022/Conference"],
    readers = ["everyone"],
    invitees=["aclweb.org/ACL/2022/Conference"],
    reply={
        "readers":{"values":["aclweb.org/ACL/2022/Conference"]},
        "writers":{"values":["aclweb.org/ACL/2022/Conference"]},
        "signatures":{"values":["aclweb.org/ACL/2022/Conference"]},
        "content":{
            "paper_link": {
                "description": "Provide the link to your previous ACL submission",
                "value-regex": "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                "required": True,
                "order": 10
                },
            "paper_type": {
                "description": "Select if your paper is short or long",
                "value-radio": [
                "short",
                "long"
                ],
                "required": True,
                "order": 11
                },
            "track": {
                "description": "Select the track that best fits your submission.",
                "values-checkbox": [
                "Ethics and NLP",
                "Linguistic theories, Cognitive Modeling and Psycholinguistics",
                "Machine Learning for NLP",
                "Phonology, Morphology and Word Segmentation",
                "Resources and Evaluation",
                "Semantics: Lexical",
                "Semantics: Sentence-level Semantics, Textual Inference and Other areas",
                "Syntax: Tagging, Chunking and Parsing",
                "Information Extraction",
                "Computational Social Science and Cultural Analytics",
                "Information Retrieval and Text Mining",
                "Interpretability and Analysis of Models for NLP",
                "Machine Translation and Multilinguality",
                "NLP Applications",
                "Question Answering",
                "Dialogue and Interactive Systems",
                "Discourse and Pragmatics",
                "Generation",
                "Language Grounding to Vision, Robotics and Beyond",
                "Sentiment Analysis, Stylistic Analysis, and Argument Mining",
                "Speech and Multimodality",
                "Summarization",
                "Special Theme"
                ],
                "required": True,
                "order": 12
                },
            "comment": {
                "description": "Comment to Senior Area Chairs (500 words)",
                "order": 13,
                "value-regex": "[\\S\\s]{0,500}",
                "required": False
                },
            "title": {
                "description": "Title of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 10,
                "value-regex": ".{1,250}",
                "required": True
            },
            "authors": {
                "description": "Comma separated list of author names.",
                "order": 11,
                "values-regex": "[^;,\\n]+(,[^,\\n]+)*",
                "required": True,
                "hidden": True
            },
            "authorids": {
                "description": "Search author profile by first, middle and last name or email address. If the profile is not found, you can add the author by completing first, middle, and last names as well as author email address.",
                "order": 12,
                "values-regex": "~.*|([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,},){0,}([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,})",
                "required": True
            },
            "abstract": {
                "description": "Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 14,
                "value-regex": "[\\S\\s]{1,5000}",
                "required": True
            },
            "pdf": {
                "description": "Upload a single PDF containing the paper, references and any appendices",
                "order": 15,
                "value-file": {
                "fileTypes": [
                "pdf"
                ],
                "size": 80
                },
                "required": True
            },
        "software": {
                "description": "Each ARR submission can be accompanied by one .tgz or .zip archive containing software (max. 200MB).",
                "order": 21,
                "value-file": {
                "fileTypes": [
                "tgz",
                "zip"
                ],
                "size": 200
                },
                "required": False
                },
            "data": {
                "description": "Each ARR submission can be accompanied by one .tgz or .zip archive containing data (max. 200MB).",
                "order": 22,
                "value-file": {
                "fileTypes": [
                "tgz",
                "zip"
                ],
                "size": 200
                },
                "required": False
                }        
        }
    }
)

client.post_invitation(submission_invitation)

# Posting Blind Submission Invitation 
blind = openreview.Invitation(
    id = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission',
    readers = ['everyone'],
    writers = ['aclweb.org/ACL/2022/Conference'],
    invitees = ['aclweb.org/ACL/2022/Conference'],
    signatures = ['aclweb.org/ACL/2022/Conference'],
    reply ={
        "readers" : {"values-regex":".*"},
        "nonreaders" : {"values-regex":".*"},
        "writers" : {"values-regex":".*"},
        "signatures" : {"values":['aclweb.org/ACL/2022/Conference']},
        "content" : {
                    "authorids" : ".*",
                    "authors":".*"
                }
    }
)

client.post_invitation(blind)

commitment = openreview.Invitation(
    id = 'aclweb.org/ACL/2022/Conference/-/Commitment_Submission',
    signatures = ["aclweb.org/ACL/2022/Conference"],
    readers = ["everyone"],
    invitees=["everyone"],
    reply={
        "readers":{"values-copied":["aclweb.org/ACL/2022/Conference/Program_Chairs","aclweb.org/ACL/2022/Conference"]},
        "signatures":{"values-copied":["aclweb.org/ACL/2022/Conference"]},
        "content":{
            "paper_link": {
                "description": "Provide the link to your previous ACL submission",
                "value-regex": "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                "required": True,
                "order": 10
                },
            "paper_type": {
                "description": "Select if your paper is short or long",
                "value-radio": [
                "short",
                "long"
                ],
                "required": True,
                "order": 11
                },
            "track": {
                "description": "Select the track that best fits your submission.",
                "values-checkbox": [
                "Ethics and NLP",
                "Linguistic theories, Cognitive Modeling and Psycholinguistics",
                "Machine Learning for NLP",
                "Phonology, Morphology and Word Segmentation",
                "Resources and Evaluation",
                "Semantics: Lexical",
                "Semantics: Sentence-level Semantics, Textual Inference and Other areas",
                "Syntax: Tagging, Chunking and Parsing",
                "Information Extraction",
                "Computational Social Science and Cultural Analytics",
                "Information Retrieval and Text Mining",
                "Interpretability and Analysis of Models for NLP",
                "Machine Translation and Multilinguality",
                "NLP Applications",
                "Question Answering",
                "Dialogue and Interactive Systems",
                "Discourse and Pragmatics",
                "Generation",
                "Language Grounding to Vision, Robotics and Beyond",
                "Sentiment Analysis, Stylistic Analysis, and Argument Mining",
                "Speech and Multimodality",
                "Summarization",
                "Special Theme"
                ],
                "required": True,
                "order": 12
                },
            "comment": {
                "description": "Comment to Senior Area Chairs (500 words)",
                "order": 13,
                "value-regex": "[\\S\\s]{0,500}",
                "required": False
                }
        }
    }
)
client.post_invitation(commitment)

# Creating SAC groups from Track Name 
f = open('SAC_groups.csv')
SAC_name_dictionary = {}

file = csv.reader(f)
header = []
rows = []
header = next(file)
for row in file:
    rows.append(row)
f.close()
for row in rows:
    SAC_name_dictionary[row[1]] = row[0]



# Retrieve all commitment submissions, ACL submissions, and ACL blind submissions  
notes = openreview.tools.iterget_notes(client,invitation='aclweb.org/ACL/2022/Conference/-/Commitment_Submission')
submissions = openreview.tools.iterget_notes(client,invitation='aclweb.org/ACL/2022/Conference/-/Submission')
blind_submissions = {note.forum: note for note in list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))}

# Save all submissions in a dictionary by paper_link
submission_dict = {submission.content['paper_link'].split('=')[1]:submission for submission in submissions}


# Iterate through all commitment submissions  
for note in tqdm(notes):
    # For each, retrieve old paper from link
    forum = note.content['paper_link'].split('=')[1]
    if forum not in submission_dict:
        original_arr_sub_id = client.get_note(forum).original
        original_arr_sub = client.get_note(original_arr_sub_id)
        if original_arr_sub:
            # Create new note to submit to ACL 
            acl_sub = openreview.Note(
                invitation="aclweb.org/ACL/2022/Conference/-/Submission",
                readers = ["aclweb.org/ACL/2022/Conference/Program_Chairs","aclweb.org/ACL/2022/Conference"], # Should SAC be in readers? 
                writers = ["aclweb.org/ACL/2022/Conference"],
                signatures = ["aclweb.org/ACL/2022/Conference"],
                content = {
                    "paper_link": note.content["paper_link"],
                    "paper_type":note.content["paper_type"],
                    "track":note.content["track"],
                    "comment":note.content.get("comment"),
                    "authorids":original_arr_sub.content["authorids"],
                    "authors": original_arr_sub.content["authors"],
                    "title":original_arr_sub.content["title"],
                    "abstract":original_arr_sub.content["abstract"],
                    "data":original_arr_sub.content.get("data"),
                    "software":original_arr_sub.content.get("software"),
                    "pdf":original_arr_sub.content.get("pdf")
                }  
            )
            acl_sub = client.post_note(acl_sub)
            submission_dict[acl_sub.content['paper_link'].split('=')[1]]=acl_sub

# Iterate through submission dictionary, check if each has a blind submission, and create blind submission if not 
for forum in submission_dict.keys():
    acl_submission = submission_dict[forum]
    if acl_submission.forum not in blind_submissions:
        # Post blind note with original = forum of ACL submission
        blinded_note = openreview.Note(
            invitation = "aclweb.org/ACL/2022/Conference/-/Blind_Submission",
            original = acl_submission.id,
            readers = ["aclweb.org/ACL/2022/Conference/Program_Chairs","aclweb.org/ACL/2022/Conference", "aclweb.org/ACL/2022/Conference/Paper{number}/Senior_Area_Chairs".format(number = acl_submission.number)],
            nonreaders = ["aclweb.org/ACL/2022/Conference/Paper{number}/Conflicts".format(number = acl_submission.number)],
            writers = ["aclweb.org/ACL/2022/Conference"],
            signatures = ["aclweb.org/ACL/2022/Conference"],
            content = {
                "authorids" : "",
                "authors":""
            }
        )
        
        blinded_note = client.post_note(blinded_note)
        print(blinded_note.forum)
        blind_submissions[blinded_note.forum] = blinded_note 
        
        # Post requisite groups 

        number = blinded_note.number
        # Create paperX/Authors -- do I need to check if the group already exists? 
        authors = openreview.Group(
            id = 'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number), 
            signatures = ['aclweb.org/ACL/2022/Conference'],
            signatories = ['aclweb.org/ACL/2022/Conference', 'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)],
            readers = ['aclweb.org/ACL/2022/Conference', 'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)],
            writers = ['aclweb.org/ACL/2022/Conference'],
            members = acl_submission.content['authorids']
        )
        
        client.post_group(authors)
        
        # Create paperX/Conflicts
        arr_submission = client.get_note(forum)
        conf_id = arr_submission.invitation.rsplit('/', 2)[0]
        arr_number = arr_submission.number
        conflicts = openreview.Group(
            id = 'aclweb.org/ACL/2022/Conference/Paper{number}/Conflicts'.format(number = number),
            signatures = ['aclweb.org/ACL/2022/Conference'],
            signatories = ['aclweb.org/ACL/2022/Conference'],
            readers = ['aclweb.org/ACL/2022/Conference'],
            writers = ['aclweb.org/ACL/2022/Conference'],
            members = ['{confid}/Paper{number}/Reviewers'.format(confid = conf_id, number = arr_number),
                       '{confid}/Paper{number}/Area_Chairs'.format(confid = conf_id, number = arr_number),
                      'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
                      ]
        )
        client.post_group(conflicts)
        
        # Create paperX/SAC groups 
        members = []
        for track in acl_submission.content['track']:
            members.append("aclweb.org/ACL/2022/Conference/{SAC_group}/Senior_Area_Chairs".format(SAC_group = SAC_name_dictionary[track]))
        SAC = openreview.Group(
            id = 'aclweb.org/ACL/2022/Conference/Paper{number}/Senior_Area_Chairs'.format(number = number),
            signatures = ['aclweb.org/ACL/2022/Conference'],
            signatories = ['aclweb.org/ACL/2022/Conference', 'aclweb.org/ACL/2022/Conference/Paper{number}/Senior_Area_Chairs'.format(number = number)],
            readers = ['aclweb.org/ACL/2022/Conference', 'aclweb.org/ACL/2022/Conference/Paper{number}/Senior_Area_Chairs'.format(number = number)],
            writers = ['aclweb.org/ACL/2022/Conference'],
            members = members
        )
        client.post_group(SAC)
    

    