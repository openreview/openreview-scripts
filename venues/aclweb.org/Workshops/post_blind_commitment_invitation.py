import argparse
from calendar import c
from re import sub
import openreview
from tqdm import tqdm
import csv


"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password
    confid - the user's conference 

"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--confid')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

confid = args.confid
blind = openreview.Invitation(
    id = f'{confid}/-/Blind_Commitment_Submission',
    readers = [
        'everyone'
        ],
    writers = [
        confid
        ],
    invitees = [
        confid
        ],
    signatures = [
        confid
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
                confid
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
    )

client.post_invitation(blind)