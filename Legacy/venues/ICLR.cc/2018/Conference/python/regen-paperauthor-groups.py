import openreview
import config
import csv
import argparse

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print client.baseurl

# repair author groups
submissions = client.get_notes(invitation=config.SUBMISSION)

for note in submissions:

    papergroup_id = 'ICLR.cc/2018/Conference/Paper{0}'.format(note.number)
    papergroup_params = {
        'signatures': [config.CONF],
        'writers': [config.CONF],
        'members': [],
        'readers': [config.CONF],
        'signatories': []
    }
    new_papergroup = client.post_group(openreview.Group(papergroup_id, **papergroup_params))

    authorgroup_id = 'ICLR.cc/2018/Conference/Paper{0}/Authors'.format(note.number)
    authorgroup_params = {
      'signatures': [config.CONF, '~Super_User1'],
      'writers': [config.CONF, '~Super_User1'],
      'members': note.content['authorids'] + note.signatures,
      'readers': [config.CONF, config.PROGRAM_CHAIRS, authorgroup_id],
      'signatories': [authorgroup_id]
    }
    new_group = client.post_group(openreview.Group(authorgroup_id, **authorgroup_params))
    print "posting new group ", new_group.id
