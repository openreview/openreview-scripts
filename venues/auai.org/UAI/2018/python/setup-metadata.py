import openreview
import openreview_matcher
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

submissions = client.get_notes(invitation='auai.org/UAI/2018/-/Submission')

group_ids = [
    'auai.org/UAI/2018/Program_Committee/IDs',
    'auai.org/UAI/2018/Senior_Program_Committee/IDs'
]

papers = client.get_notes(invitation = 'auai.org/UAI/2018/-/Blind_Submission')
groups = [client.get_group(g) for g in group_ids]

'''
This is how metadata generation *would* work, if we had any of the backend data to support it.
'''

# # Define features
# print "building feature models..."
# paper_features = [
#     openreview_matcher.metadata.BasicAffinity(name='affinity', client, groups, papers)
# ]

# print "generating paper metadata..."
# def metadata(forum):
#     return openreview_matcher.metadata.generate_metadata_note(groups=groups, features=paper_features, note_params={
#         'forum': forum,
#         'invitation': config.METADATA,
#         'readers': [config.CONF],
#         'writers': [config.CONF],
#         'signatures': [config.CONF]
#     })
# metadata_notes = [metadata(note.forum) for note in papers]

'''
Instead, we'll use this workaround
'''

def metadata(forum, groups):
    metadata_note = openreview.Note(**{
        'forum': forum,
        'invitation': 'auai.org/UAI/2018/-/Paper_Metadata',
        'readers': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Program_Committee',
            'auai.org/UAI/2018/Senior_Program_Committee'
        ],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'content': {
                'groups': []
            }
    })
    for g in groups:
        group_entry = {'groupid': g.id, 'members': []}
        for user_id in g.members:
            user_entry = {'userid': user_id, 'scores': []}
            affinity_entry = {'type': 'affinity', 'score': random.random()*10}
            conflict_entry = {'type': 'conflict', 'score': '-inf'}

            user_entry['scores'].append(affinity_entry)
            if random.random() > 0.9:
                user_entry['scores'].append(conflict_entry)

            group_entry['members'].append(user_entry)

        metadata_note.content['groups'].append(group_entry)

    return metadata_note

existing_notes_by_forum = {n.forum: n for n in client.get_notes(invitation = 'auai.org/UAI/2018/-/Paper_Metadata')}

print "posting paper metadata..."
for p in papers:
    if p.forum in existing_notes_by_forum:
        metadata_note = existing_notes_by_forum[p.forum]
    else:
        metadata_note = metadata(p.forum, groups)
    client.post_note(metadata_note)
