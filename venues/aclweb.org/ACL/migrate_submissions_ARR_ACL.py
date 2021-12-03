import argparse
import openreview
from tqdm import tqdm

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

# Iterate through all commitment submissions 
notes = openreview.tools.iterget_notes(client,invitation='aclweb.org/ACL/2022/Conference/-/Commitment')
for note in notes:
    # For each, retrieve old paper from link
    link = note.content['paper_link']
    forum = link.split('=')[1]
    old_note = client.get_note(client.get_note(forum).original)
# Create JSON for new note with readers
    JSON = {
        "invitation": "aclweb.org/ACL/2022/Conference/-/Submission",
        "readers": ["aclweb.org/ACL/2022/Program_Chairs","aclweb.org/ACL/2022"],
        "writers": ["aclweb.org/ACL/2022/Conference"],
        "signatures":["aclweb.org/ACL/2022/Conference"],
        "content":{
            "paper_link": note.content["paper_link"],
            "paper_type":note.content["paper_type"],
            "track":note.content["track"],
            "comment":note.content["comment"],
            "authorids":old_note.content["authorids"],
            "authors": old_note.content["authors"],
            "title":old_note.content["title"],
            "abstract":old_note.content["abstract"],
            "data":old_note.content.get("data"),
            "software":old_note.content.get("software"),
            "pdf":old_note.content.get("pdf")
        }  
    }
    # Create note from JSON and post to ACL Submission invitation
    acl_sub = openreview.Note.from_json(JSON)
    print(acl_sub)
    client.post_note(acl_sub)