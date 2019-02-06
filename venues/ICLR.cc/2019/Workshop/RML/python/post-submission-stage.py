import openreview
import config
import argparse

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
conference.create_blind_submissions(public = True)
