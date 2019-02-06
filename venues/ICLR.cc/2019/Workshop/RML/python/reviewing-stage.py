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

print("Open Comments")
conference.open_comments(name = 'Official_Comment', public = False, anonymous = True)
conference.open_comments(name = 'Public_Comment', public = True, anonymous = True)

print("Open Reviews")
conference.open_reviews(name = 'Official_Review', due_date = datetime.datetime(2019, 3, 16, 0, 0), public = False)
