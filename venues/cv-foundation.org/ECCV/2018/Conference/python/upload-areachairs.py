import openreview
import argparse
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


with open(os.path.join(os.path.dirname(__file__),'../data/areachairs.csv')) as f:
    reader = csv.reader(f)
    reader.next()
    members = []
    for line in reader:
        first = line[0]
        middle = line[1]
        last = line[2]
        email = line[3]
        try:
            profile = openreview.tools.create_profile(client, first = first, middle = middle, last = last, email = email)
            members.append(profile.id)
        except Exception as error:
            print('Error get profile', email, error)

areachairs_group = client.post_group(openreview.Group(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/Area_Chairs',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['~Super_User1'],
    'signatories': [],
    'members': members
}))

print areachairs_group.members
