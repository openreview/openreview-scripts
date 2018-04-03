import openreview
import argparse
from openreview import invitations
from openreview import process
from openreview import tools
from openreview import webfield

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

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
    'REVIEWERS': 'ISMIR.net/2018/WoRMS/Reviewers',
    'SUBMISSION_INVITATION': 'ISMIR.net/2018/WoRMS/-/Submission',
    'INSTRUCTIONS': ''
}

# Aug 7, 2018 11:59 pm AoE = 8/8/18 11:59am GMT
DUE_DATE =  tools.timestamp_GMT(2018, 8, 8, 12)

groups = tools.build_groups(js_constants['CONFERENCE'])
for g in groups:
    print "posting group {0}".format(g.id)
    client.post_group(g)
'''
Create a submission invitation (a call for papers).
'''

submission_inv = invitations.Submission(
    name = 'Submission',
    conference_id = js_constants['CONFERENCE'],
    duedate = DUE_DATE,
    content_params = {
        # defaults to blind submission description
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

comment_inv = invitations.Comment(
    name = 'Comment',
    conference_id = js_constants['CONFERENCE'],
    process = '../process/commentProcess.js',
    invitation = js_constants['SUBMISSION_INVITATION'],
)
client.post_invitation(comment_inv)

print "posted invitation", comment_inv.id

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

pcs = openreview.Group(js_constants['PROGRAM_CHAIRS'],
    readers=[js_constants['CONFERENCE'], js_constants['PROGRAM_CHAIRS']],
    writers=[js_constants['CONFERENCE']],
    signatories= [js_constants['CONFERENCE'], js_constants['PROGRAM_CHAIRS']],
    signatures= [js_constants['CONFERENCE']]
    #'web': os.path.join(os.path.dirname(__file__), '../webfield/programchairWebfield.js'),
)
client.post_group(pcs)
print "posted group",pcs.id

reviewers = openreview.Group(js_constants['REVIEWERS'],
    readers=[js_constants['CONFERENCE']],
    writers=[js_constants['CONFERENCE']],
    signatories= [js_constants['CONFERENCE']],
    signatures= [js_constants['CONFERENCE']]
    #'web': os.path.join(os.path.dirname(__file__), '../webfield/programchairWebfield.js'),
)
client.post_group(reviewers)
print "posted group",reviewers.id
