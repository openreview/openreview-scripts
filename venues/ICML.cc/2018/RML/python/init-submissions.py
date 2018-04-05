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
    'TITLE': "ICML 2018 - RML Workshop",
    'SUBTITLE': "Reproducibility in Machine Learning",
    'LOCATION': "Stockholm, Sweden",
    'DATE': "July 15, 2018",
    'WEBSITE': "https://mltrain.cc/events/enabling-reproducibility-in-machine-learning-mltrainrml-icml-2018/",
    'DEADLINE': "Submission Deadline: May 15th, 10am EST",
    'CONFERENCE': 'ICML.cc/2018/RML',
    'PROGRAM_CHAIRS': 'ICML.cc/2018/RML/Program_Chairs',
    'REVIEWERS': 'ICML.cc/2018/RML/Reviewers',
    'SUBMISSION_INVITATION': 'ICML.cc/2018/RML/-/Submission',
    'INSTRUCTIONS': "<a href =\"https://sites.google.com/view/icml-reproducibility-workshop/home\">https://sites.google.com/view/icml-reproducibility-workshop/home</a>"
}

# May 15th, 10am EST = 5/15/18 2pm GMT
DUE_DATE =  tools.timestamp_GMT(2018, 5, 15, 14)

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

# post the submission
submission_inv = client.post_invitation(submission_inv)
print "posted invitation", submission_inv.id

# create and post the comment invitation
comment_inv = invitations.Comment(
    name = 'Comment',
    conference_id = js_constants['CONFERENCE'],
    invitation = js_constants['SUBMISSION_INVITATION'],
)
comment_process = process.MaskSubmissionProcess('../process/commentProcess.js', js_constants, None)
comment_inv.add_process(comment_process)
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
