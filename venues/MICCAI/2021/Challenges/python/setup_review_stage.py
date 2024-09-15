import argparse
import re
import csv
import openreview
from tqdm import tqdm
from openreview import tools
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('assignments_file', help='csv file')
parser.add_argument('--baseurl', help='base url')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

conference = openreview.helpers.get_conference(client, '6tlp9iYQvsy')

#set official reviews
review_stage = conference.set_review_stage(openreview.ReviewStage(due_date = datetime.datetime(2021, 1, 16, 11, 59),release_to_authors=True, 
additional_fields = {
    "summary": {
        "order": 2,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Please provide a summary of this work (max 200000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "soundness": {
        "order": 3,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Is the challenge design concise and sound? (max 5000 characters) Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "quality": {
        "order": 4,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Is the document in sufficient quality for being uploaded? (max 5000 characters) Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "revisions": {
        "order": 5,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Provide any revisions essential for the acceptance of the challenge. (max 5000 characters) Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "comments": {
        "order": 6,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Provide any further comments. (max 5000 characters) Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "rating": {
        "order": 7,
        "value-dropdown": [
            "10: Top 5% of accepted challenges, seminal challenge",
            "9: Top 15% of accepted challenges, strong challenge",
            "8: Top 50% of accepted challenges, clear accept",
            "7: Good challenge, accept",
            "6: Marginally above acceptance threshold",
            "5: Marginally below acceptance threshold",
            "4: Ok but not good enough - rejection",
            "3: Clear rejection",
            "2: Strong rejection",
            "1: Trivial or wrong"
        ],
        "required": True
    },
    "confidence": {
        "order": 8,
        "value-radio": [
            "5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature",
            "4: The reviewer is confident but not absolutely certain that the evaluation is correct",
            "3: The reviewer is fairly confident that the evaluation is correct",
            "2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper",
            "1: The reviewer's evaluation is an educated guess"
        ],
        "required": True
    }
},
remove_fields = ['review']))

#Set clinical reviews
clinical_revs = conference.set_review_stage(openreview.ReviewStage(name='Clinical_Review', due_date = datetime.datetime(2021, 1, 16, 11, 59), 
release_to_authors=True, 
additional_fields = {
    "summary": {
        "order": 2,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Please provide a summary of this work (max 200000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "challenge_goals": {
        "order": 3,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Is the challenge goal clinically relevant? (max 5000 characters) Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "metrics": {
        "order": 4,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Are the metrics clinically relevant? (max 5000 characters) Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "comments": {
        "order": 5,
        "value-regex": "[\\S\\s]{1,200000}",
        "description": "Provide any further comments. (max 5000 characters) Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "required": True,
        "markdown": True
    },
    "rating": {
        "order": 6,
        "value-dropdown": [
            "10: Top 5% of accepted challenges, seminal challenge",
            "9: Top 15% of accepted challenges, strong challenge",
            "8: Top 50% of accepted challenges, clear accept",
            "7: Good challenge, accept",
            "6: Marginally above acceptance threshold",
            "5: Marginally below acceptance threshold",
            "4: Ok but not good enough - rejection",
            "3: Clear rejection",
            "2: Strong rejection",
            "1: Trivial or wrong"
        ],
        "required": True
    },
    "confidence": {
        "order": 7,
        "value-radio": [
            "5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature",
            "4: The reviewer is confident but not absolutely certain that the evaluation is correct",
            "3: The reviewer is fairly confident that the evaluation is correct",
            "2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper",
            "1: The reviewer's evaluation is an educated guess"
        ],
        "required": True
    }
}, 
remove_fields = ['review']))