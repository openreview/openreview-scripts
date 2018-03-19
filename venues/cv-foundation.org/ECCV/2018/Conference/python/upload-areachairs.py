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


def search_institution(history, domain):
    for h in history:
        if domain == h['institution']['domain']:
            return True
    return False

with open(os.path.join(os.path.dirname(__file__),'../data/areachairs.csv')) as f:
    reader = csv.reader(f)
    reader.next()
    members = []
    for line in reader:
        first = line[0].strip()
        middle = line[1].strip()
        last = line[2].strip()
        email = line[3].lower().strip()
        conflicts = [c.strip() for c in line[5].lower().strip().split(';')]

        profiles = client.get_profiles([email])

        if profiles:
            profile_note = client.get_note(id = profiles[email].id)

            history = profile_note.content.get('history', [])

            for c in conflicts:
                exists = search_institution(history, c)
                if not exists:
                    history.append({
                        'end': None,
                        'start': None,
                        'position': None,
                        'institution': {
                            'name': c,
                            'domain': c
                        }
                    })
            profile_note.content['history'] = history

            saved_profile = client.update_profile(profile_note.id, profile_note.content)
            members.append(saved_profile.id)
        else:
            print 'Not Found', email

areachairs_group = client.post_group(openreview.Group(**{
    'id': 'cv-foundation.org/ECCV/2018/Conference/Area_Chairs',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['~Super_User1'],
    'signatories': [],
    'members': members
}))

print areachairs_group.members
