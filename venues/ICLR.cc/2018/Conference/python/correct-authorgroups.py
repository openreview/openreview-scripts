import openreview
import config
import csv
import argparse
from collections import defaultdict

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print client.baseurl

# get all the authorgroups.
# where does 1176 come from?
# 1176 is the value on the counter for ICLR.cc/2018/Conference/-/Submission
authorgroups = []
print "finding valid authorgroups ..."
for i in range(1, 1176):
    groupid = 'ICLR.cc/2018/Conference/Paper{0}/Authors'.format(i)
    try:
        authorgroup = client.get_group(groupid)
        authorgroups.append(authorgroup)
    except:
        pass


# strip all the author groups of their members
print "remove all members from all authorgroups ..."
for authorgroup in authorgroups:
    client.remove_members_from_group(authorgroup, authorgroup.members)


# iterate through all the blind submissions and set the authorids to the right number authorgroup
print "iterating through blind submissions, updating them ..."
blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
for n in blind_submissions:
    n.content['authorids'] = ['ICLR.cc/2018/Conference/Paper{0}/Authors'.format(n.number)]
    client.post_note(n)

# collect all the official comments by replyforum
# official comments are the only ones that should be made by authors
print "collecting comments ..."
official_comment_invs = client.get_invitations(regex = config.CONF + '/-/Paper.*/' + "Official_Comment")
official_comments_by_replyforum = defaultdict(list)
for i in official_comment_invs:
    notes = client.get_notes(invitation=i.id)
    if notes != []:
        official_comments_by_replyforum[i.reply['forum']]+= notes

# iterate through all the official comments,
# check that they're written by authors,
# and if they are replace the author with the right writer/signature
print "correcting comments ..."
official_comments_by_replyforum
for forum, comments in official_comments_by_replyforum.iteritems():
    for c in comments:
        if 'Authors' in c.signatures[0]:
            try:
                blind_note = client.get_note(forum)
                c.writers = ['ICLR.cc/2018/Conference/Paper{0}/Authors'.format(blind_note.number)]
                c.signatures = c.writers
                client.post_note(c)
            except:
                print "note not found", forum
                c.ddate = 1509637852000
                client.post_note(c)
        else:
            print c.signatures

# loop through original submissions and repopulate the groups
authorgroup_by_id = {a.id: a for a in authorgroups}

submissions = client.get_notes(invitation=config.SUBMISSION)
for n in submissions:
    authorgroup = authorgroup_by_id['ICLR.cc/2018/Conference/Paper{0}/Authors'.format(n.number)]
    client.add_members_to_group(authorgroup, n.content['authorids'])
