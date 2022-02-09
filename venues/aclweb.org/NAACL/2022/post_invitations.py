import argparse
from re import sub
from sys import set_asyncgen_hooks
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

sac_name_dictionary = tracks.sac_name_dictionary
track_names = list(sac_name_dictionary.keys())
print(track_names)
# Post commitment invitation 
preprocess = None
with open('./commitmentPreProcess.py') as f:
    preprocess = f.read()

commitment = client.post_invitation(openreview.Invitation(
    id = 'aclweb.org/NAACL/2022/Conference/-/Commitment_Submission',
    signatures = [
        "aclweb.org/NAACL/2022/Conference"
        ],
    readers = [
        "everyone"
        ],
    invitees=[
        "~",
        "OpenReview.net/Support"
        ],
    process= './commitmentProcess.js',
    preprocess=preprocess,
    reply={
        "readers":{
            "values-copied":[
                "aclweb.org/NAACL/2022/Conference",
                "{content.authorids}",
                "{signatures}"
            ]
        },
        "writers": {
            "values-copied": [
                "aclweb.org/NAACL/2022/Conference",
                "{content.authorids}",
                "{signatures}"
            ]
        },
        "signatures": { "values-regex": "~.*" },
        "content":{
            "title": {
                "description": "Enter the title of the ARR submission that you want to commit to NAACL 2022",
                "value-regex": ".{1,250}",
                "required": True,
                "order": 10
            },
            "authors": {
                "description": "The author information entered in this field is only for communication purposes. Please remember that the list of authors and their order cannot be changed and should be the same as what was submitted to ARR. Comma separated list of author names.",
                "order": 11,
                "values-regex": "[^;,\\n]+(,[^,\\n]+)*",
                "required": True,
                "hidden": True
            },
            "authorids": {
                "description": "The author information entered in this field is only for communication purposes. Please remember that the list of authors and their order cannot be changed and should be the same as what was submitted to ARR. Search author profile by first, middle and last name or email address. If the profile is not found, you can add the author by completing first, middle, and last names as well as author email address.",
                "order": 12,
                "values-regex": "~.*|([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,},){0,}([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,})",
                "required": True
            },
            "paper_link": {
                "description": "The link to the paper on ARR (including id). You need to put a link to the page that shows the reviews and the meta-review (it should end with forum= a random string of letters, like https://openreview.net/forum?id=abCD-EFgHI). Please, do NOT put a link to the PDF or to the list of your papers.",
                "value-regex": "https://openreview.net/forum\\?id=.*",
                "required": True,
                "markdown": False,
                "order": 13
            },
            "paper_type": {
                "description": "Indicate whether this is a short (a small, focused contribution; a negative result; an opinion piece; or an interesting application nugget) or a long paper.",
                "value-radio": [
                    "Long paper (up to eight pages of content + unlimited references and appendices)",
                    "Short paper (up to four pages of content + unlimited references and appendices)"
                    ],
                "required": True,
                "order": 14
            },
            "track": {
                "description": "Please enter the subject area under which the submission should be considered. ",
                "value-radio": track_names,
                "required": True,
                "order": 15
            },
            "naacl_preprint": {
                "description": "Would the authors like to have a public anonymous pre-print of the submission? This includes PDF, abstract and all supplemental material.",
                "value-radio": [
                    "yes",
                    "no"
                    ],
                "required": True,
                "order": 16
            },
            "existing_preprints": {
                "values-regex": ".{1,500}",
                "description": "If there are any publicly available non-anonymous preprints of this paper, please list them here (provide the URLs please).",
                "required": False,
                "order": 17
            },
            "authorship": {
                "values-checkbox": [
                    "I confirm that I am one of the authors of this paper"
                    ],
                "required": True,
                "order": 19
            },
            "paper_version": {
                "values-checkbox": [
                    "I confirm that this link is for the latest version of the paper in ARR that has reviews and a meta-review"
                    ],
                "required": True,
                "order": 20
            },
            "anonymity_period": {
                "values-checkbox": [
                    "I confirm that this submission complies with the anonymity period"
                    ],
                "required": True,
                "order": 21
            }
        }
    }
)
)

# Posting submission invitation 
submission_invitation = client.post_invitation(openreview.Invitation(
    id = "aclweb.org/NAACL/2022/Conference/-/Submission",
    signatures = ["aclweb.org/NAACL/2022/Conference"],
    readers = ["everyone"],
    invitees=["aclweb.org/NAACL/2022/Conference"],
    reply={
        "readers":{
            "values":[
                "aclweb.org/NAACL/2022/Conference"
            ]
            },
        "writers":{
            "values":[
                "aclweb.org/NAACL/2022/Conference"
                ]
            },
        "signatures":{
            "values":[
                "aclweb.org/NAACL/2022/Conference"
                ]
            },
        "content":{
            "title": {
                "description": "Title of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 1,
                "value-regex": ".{1,250}",
                "required": True
            },
            "authors": {
                "description": "Comma separated list of author names.",
                "order": 2,
                "values-regex": "[^;,\\n]+(,[^,\\n]+)*",
                "required": True,
                "hidden": True
            },
            "authorids": {
                "description": "Search author profile by first, middle and last name or email address. If the profile is not found, you can add the author by completing first, middle, and last names as well as author email address.",
                "order": 3,
                "values-regex": "~.*|([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,},){0,}([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,})",
                "required": True
            },
            "abstract": {
                "description": "Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 4,
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
                },
            "paper_link": {
                "description": "Provide the link to your previous ACL submission",
                "value-regex": "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                "required": True,
                "order": 10
                },
            "paper_type": {
                "description": "Select if your paper is short or long",
                "value-radio": [
                    "Short paper (up to four pages of content + unlimited references and appendices)",
                    "Long paper (up to eight pages of content + unlimited references and appendices)"
                ],
                "required": True,
                "order": 11
                },
            "track": {
                "description": "Select the track that best fits your submission.",
                "value-radio": track_names,
                "required": True,
                "order": 12
                },
            "comments_to_the_senior_area_chairs": {
                "description": "Comment to Senior Area Chairs (500 words)",
                "order": 50,
                "value-regex": "[\\S\\s]{0,3000}",
                "required": False
                },
            "authorship": {
                "values-checkbox": [
                    "I confirm that I am one of the authors of this paper"
                ],
                "required": True,
                "order": 19
            },
            "paper_version": {
                "values-checkbox": [
                    "I confirm that this link is for the latest version of the paper in ARR that has reviews and a meta-review"
                ],
                "required": True,
                "order": 20
            },
            "anonymity_period": {
                "values-checkbox": [
                "I confirm that this submission complies with the anonymity period"
                ],
                "required": True,
                "order": 21
            },
            "commitment_note":{
                "value-regex":".*",
                "required": True,
                "order": 30
            },
            "naacl_preprint": {
            "description": "Would the authors like to have a public anonymous pre-print of the submission? This includes PDF, abstract and all supplemental material.",
            "value-radio": [
                "yes",
                "no"
            ],
            "required": False,
            "order": 16
            },
            "preprint": {
            "description": "Would the authors like to have a public anonymous pre-print of the submission? This includes PDF, abstract and all supplemental material.",
            "value-radio": [
                "yes",
                "no"
            ],
            "required": False,
            "order":31
            },
            "existing_preprints": {
            "values-regex": ".{1,500}",
            "description": "If there are any publicly available non-anonymous preprints of this paper, please list them here (provide the URLs please).",
            "required": False,
            "order": 17
            },
            "previous_URL": {
            "description": "Provide the URL of your previous submission to ACL Rolling Review if this is a resubmission",
            "order": 16,
            "value-regex": ".{0,500}",
            "required": False
            },
            "TL;DR": {
            "description": "\"Too Long; Didn't Read\": a short sentence describing your paper",
            "order": 13,
            "value-regex": "[^\\n]{0,250}",
            "required": False
        }
        }
    }  
))

# Posting Blind Submission Invitation 
blind = client.post_invitation(openreview.Invitation(
    id = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission',
    readers = [
        'everyone'
        ],
    writers = [
        'aclweb.org/NAACL/2022/Conference'
        ],
    invitees = [
        'aclweb.org/NAACL/2022/Conference'
        ],
    signatures = [
        'aclweb.org/NAACL/2022/Conference'
        ],
    reply ={
        "readers" : {
            "values-regex":".*"
            },
        "nonreaders" : {
            "values-regex":".*"
            },
        "writers" : {
            "values-regex":".*"
            },
        "signatures" : {
            "values":[
                'aclweb.org/NAACL/2022/Conference'
                ]
            },
        "content" : {
            "authorids" : { 
                "values-regex": ".*" 
                },
            "authors": {
                "values-regex": ".*" 
                }
            }   
        }
    ))

