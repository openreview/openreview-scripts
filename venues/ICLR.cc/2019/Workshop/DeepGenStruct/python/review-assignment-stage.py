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

print ("Set global committee members")
conference.set_authors()
conference.set_program_chairs(['pc@mail.com'])
conference.set_reviewers(['pmandler@cs.umass.edu'])

print ("Create some assignments")
conference.set_assignment('mandler@cs.umass.edu', 1, is_area_chair = False)
