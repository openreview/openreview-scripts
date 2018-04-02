import os
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
    'TITLE': "DeSemWeb 2018",
    'SUBTITLE': "ISWC2018 workshop on Decentralizing the Semantic Web",
    'LOCATION': "Monterey, California, USA",
    'DATE': "October 8-12, 2018",
    'WEBSITE': "http://iswc2018.desemweb.org/",
    'DEADLINE': "Submission Deadline: May 15th, 2018, 11:59 pm (Hawaii)",
    'CONFERENCE': 'swsa.semanticweb.org/ISWC/2018/DeSemWeb',
    'PROGRAM_CHAIRS': 'swsa.semanticweb.org/ISWC/2018/DeSemWeb/Program_Chairs',
    'REVIEWERS': 'swsa.semanticweb.org/ISWC/2018/DeSemWeb/Reviewers',
    'SUBMISSION_INVITATION': 'swsa.semanticweb.org/ISWC/2018/DeSemWeb/-/Submission',
    'INSTRUCTIONS': ''
}

SUBJECT_AREAS = ['Research Article','Intelligent Client Challenge / Demo', 'Vision Statement']
# 5/15/18 11:59 pm Hawaii time = 5/16/18 9:59am GMT
DUE_DATE =  tools.timestamp_GMT(2018,5, 16,10)

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
        },
        "submission category": {
            "required": True,
            "order": 4,
            "description": "Select a submission category",
            "value-radio": [
                "Research Article",
                "Decentralized Application",
                "Vision Statement"
            ]
        },
        "pdf": {
            "required": False,
            "order": 9,
            "description": "Upload a PDF file or submit a PDF URL (PDF URLs must begin with \"http\" or \"https\" and end with \".pdf\"). Submit all other formats in the \"url\" field below.",
            "value-regex": "upload|http(s)?:\\/\\/.+\\.pdf"
        },
        "url": {
            "required": False,
            "order": 10,
            "description": "Submit a non-PDF URL (e.g. HTML submissions). URLs must begin with \"http\" or \"https\".",
            "value-regex": "http(s)?:\\/\\/.+"
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
    process = os.path.join(os.path.dirname(__file__),'../process/commentProcess.js'),
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
    subject_areas = SUBJECT_AREAS
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
