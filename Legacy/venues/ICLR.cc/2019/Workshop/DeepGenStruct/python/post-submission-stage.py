import openreview
import config
import argparse
import datetime

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference = config.get_conference(client)

print ("Closing submissions")
conference.close_submissions()

print ("Create blind submissions")
conference.create_blind_submissions()

conference.set_authors()

print('replacing members with IDs')
reviewers_group = client.get_group(conference.get_reviewers_id())
openreview.tools.replace_members_with_ids(client, reviewers_group)

# March 31st 11:59 pm EST
conference.open_bids(due_date = datetime.datetime(2019, 4, 1, 4, 59))