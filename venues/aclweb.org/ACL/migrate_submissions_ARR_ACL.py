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

# Iterate through all submissions submitted through commitment invitation 
notes = openreview.tools.iterget_notes(client,invitation='aclweb.org/ACL/2022/Conference/-/Commitment')
for note in tqdm(notes):
    # Retrieve forum from link
    link = note.content['link']
    forum = link.split('=')[1]
    old_note = client.get_note(client.get_note(forum).original)
    new_fields = {
        'link':note.content['link'],
        'length':note.content['length'],
        'track':note.content['track'],
        'comment':note.content['comment']
    }
    
    old_note.content.update(new_fields)
    old_note.invitation = 'aclweb.org/ACL/2022/Conference/-/Submission'
    old_note.readers = 'aclweb.org/ACL/2022/Conference/Program_Chairs'
    old_note.writers = old_note.content['authorids'] + ['aclweb.org/ACL/2022/Conference']
    old_note.replyto = old_note.id
    client.post_note(old_note)