import openreview
import argparse
from openreview import invitations
from openreview import process
from openreview import webfield

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

''' Build groups for conference '''
def build_groups(conference_group_id):
    # create list of subpaths (e.g. Test.com, Test.com/TestConference, Test.com/TestConference/2018)
    path_components = conference_group_id.split('/')
    paths = ['/'.join(path_components[0:index+1]) for index, path in enumerate(path_components)]

    empty_params = {
        'readers': ['everyone'],
        'writers': [],
        'signatures': [],
        'signatories': [],
        'members': []
    }

    groups = {p: openreview.Group(p, **empty_params) for p in paths}
    groups[conference_group_id].writers = groups[conference_group_id].signatories = [conference_group_id]

    admin_id = conference_group_id + '/Admin'
    groups[admin_id] = openreview.Group(admin_id, readers=[admin_id], signatories=[admin_id])

    return groups


'''
Set the variable names that will be used in various pieces of executable javascript.
'''
js_constants = {
    'TITLE': "WoRMS 2018",
    'SUBTITLE': "1st International Workshop on Reading Music Systems",
    'LOCATION': "Paris, France",
    'DATE': "20th September 2018",
    'WEBSITE': "https://sites.google.com/view/worms2018",
    'DEADLINE': "Submission Deadline: 7th of August, 2018, 11:59 pm (AoE)",
    'CONFERENCE': 'ISMIR.net/2018/WoRMS',
    'PROGRAM_CHAIRS': 'ISMIR.net/2018/WoRMS/Program_Chairs',
    'SUBMISSION_INVITATION': 'ISMIR.net/2018/WoRMS/-/Submission',
    'INSTRUCTIONS': ''
}

# Aug 7, 2018 11:59 pm AoE = 8/8/18 11:59am GMT
DUE_DATE =  1533729599000

groups = build_groups(js_constants['CONFERENCE'])
for g in sorted([g for g in groups]):
    print "posting group {0}".format(g)
    client.post_group(groups[g])

'''
Create a submission invitation (a call for papers).
'''

submission_inv = invitations.Submission(
    name = 'Submission',
    conference_id = js_constants['CONFERENCE'],
    duedate = DUE_DATE,
    content_params={
        'authors': {
            'description': 'Comma separated list of author names.',
            'order': 2,
            'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
            'required': True
        },
        'authorids': {
            'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile.',
            'order': 3,
            'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
            'required': True
        }
    }
)

submission_process = process.MaskSubmissionProcess('../process/submissionProcess.js', js_constants, None)
submission_inv.add_process(submission_process)

# post both the submissions
submission_inv = client.post_invitation(submission_inv)
print "posted invitation", submission_inv.id

'''
Create the homepage and add it to the conference group.
'''


homepage = webfield.Webfield(
    '../webfield/conferenceWebfield.js',
    group_id = js_constants['CONFERENCE'],
    js_constants = js_constants,
)

this_conference = client.get_group(js_constants['CONFERENCE'])
this_conference.web = homepage.render()
this_conference = client.post_group(this_conference)
print "adding webfield to", this_conference.id