
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
    'auai.org/UAI/2018/Program_Committee',
    'auai.org/UAI/2018/Senior_Program_Committee'
]

papers = client.get_notes(invitation = 'auai.org/UAI/2018/-/Blind_Submission')
groups = [client.get_group(g) for g in group_ids]

metadata_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Paper_Metadata',
    'readers': [
        'auai.org/UAI/2018',
        'auai.org/UAI/2018/Program_Chairs',
        'auai.org/UAI/2018/Program_Committee',
        'auai.org/UAI/2018/Senior_Program_Committee'
    ],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'auai.org/UAI/2018/-/Blind_Submission',
        'readers': {'values': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Program_Committee',
            'auai.org/UAI/2018/Senior_Program_Committee'
            ]},
        'writers': {'values': ['auai.org/UAI/2018']},
        'signatures': {'values': ['auai.org/UAI/2018']},
        'content': {}
    }
}))

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
                'groups': {}
            }
    })
    for g in groups:
        metadata_note.content['groups'][g.id] = {}
        for user_id in g.members:
            scores = {'affinity_score': random.random()*10}
            if random.random() > 0.9:
                scores['conflict_score'] = '-inf'

            metadata_note.content['groups'][g.id][user_id] = scores

    return metadata_note

existing_notes_by_forum = {n.forum: n for n in client.get_notes(invitation = 'auai.org/UAI/2018/-/Paper_Metadata')}

print "posting paper metadata..."
for p in papers:
    if p.forum in existing_notes_by_forum:
        metadata_note = existing_notes_by_forum[p.forum]
    else:
        metadata_note = metadata(p.forum, groups)
    client.post_note(metadata_note)

print "posting assignment invitation..."
assignment_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Paper_Assignment',
    'readers': [
        'auai.org/UAI/2018',
        'auai.org/UAI/2018/Program_Chairs',
        'auai.org/UAI/2018/Program_Committee',
        'auai.org/UAI/2018/Senior_Program_Committee'
    ],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'auai.org/UAI/2018/-/Blind_Submission',
        'readers': {'values': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Program_Committee',
            'auai.org/UAI/2018/Senior_Program_Committee']
        },
        'writers': {'values': ['auai.org/UAI/2018']},
        'signatures': {'values': ['auai.org/UAI/2018']},
        'content': {
            # assignment
            # label
        }
    }
}))


print "posting configuration invitation..."
config_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Assignment_Configuration',
    'readers': [
        'auai.org/UAI/2018',
        'auai.org/UAI/2018/Program_Chairs'
    ],
    'writers': [
        'auai.org/UAI/2018'
    ],
    'signatures': ['auai.org/UAI/2018'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': None,
        'readers': {'values': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs'
        ]},
        'writers': {'values': ['auai.org/UAI/2018']},
        'signatures': {'values': ['auai.org/UAI/2018']},
        'content': {
            # label = label
            # configuration = configuration
            # paper_invitation = 'auai.org/UAI/2018/-/Blind_Submission'
            # metadata_invitation = 'auai.org/UAI/2018/-/Paper_Metadata'
            # assignment_invitation = 'auai.org/UAI/2018/-/Paper_Assignment'
            # match_group = 'auai.org/UAI/2018/Program_Committee'
            # statistics = {fill in later}
        }
    }

}))

