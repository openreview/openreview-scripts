import argparse
import openreview
from tqdm import tqdm
import csv
from openreview import tools
import re
from collections import defaultdict

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

def assign_reviewer_to_paper(reviewer_id_or_email, paper_forum):
    paper = client.get_note(paper_forum)
    print(paper)
    reviewer = client.get_profile(reviewer_id_or_email)
    client.post_edge(openreview.Edge(
        invitation = 'aclweb.org/ACL/2022/Conference/Ethics_Reviewers/-/Assignment', 
        head = paper,
        tail = reviewer,
        weight = 1,
        readers = [
            "aclweb.org/ACL/2022/Conference","aclweb.org/ACL/2022/Conference/Ethics_Chairs{tail}"
            ],
        nonreaders= ["aclweb.org/ACL/2022/Conference/Paper{head.number}/Authors"],
        writers= [
            "aclweb.org/ACL/2022/Conference/Ethics_Chairs"
            ],
        signatures=["aclweb.org/ACL/2022/Conference/Ethics_Chairs"]
    ))
assign_reviewer_to_paper('~Melisa_Bok1','Ofoi1kAeB5o')