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

groups = build_groups('swsa.semanticweb.org/ISWC/2018/DeSemWeb')
for g in sorted([g for g in groups]):
    print "posting group {0}".format(g)
    client.post_group(groups[g])

'''
Set the variable names that will be used in various pieces of executable javascript.
'''
js_constants = {
    'TITLE': "DeSemWeb 2018",
    'SUBTITLE': "ISWC2018 workshop on Decentralizing the Semantic Web",
    'LOCATION': "Monterey, California, USA",
    'DATE': "October 8-12, 2018",
    'WEBSITE': "http://iswc2018.desemweb.org/",
    'DEADLINE': "Submission Deadline: May 15th, 2018, 11:59 pm SST (Samoa Standard Time)",
    'CONFERENCE': 'swsa.semanticweb.org/ISWC/2018/DeSemWeb',
    'PROGRAM_CHAIRS': 'swsa.semanticweb.org/ISWC/2018/DeSemWeb/Program_Chairs',
    'SUBMISSION_INVITATION': 'swsa.semanticweb.org/ISWC/2018/DeSemWeb/-/Submission',
    'INSTRUCTIONS': ''
}

SUBJECT_AREAS = ['Research Article','Intelligent Client Challenge / Demo', 'Vision Statement']
# 5/15/18 11:59 pm SST (Samoa Standard Time) = 5/16/18 5:59 here
DUE_DATE =  1526464799000

'''
Create a submission invitation (a call for papers).
'''

submission_inv = invitations.Submission(
    name = 'Submission',
    conference_id = js_constants['CONFERENCE'],
    duedate = DUE_DATE,
    content_params = {
        "submission category": {
            "required": True,
            "order": 4,
            "description": "Select a submission category",
            "value-radio": [
                "Research Article",
                "Intelligent Client Challenge / Demo",
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