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
    'TITLE': "IEEE ITSC 2018",
    'SUBTITLE': "Workshop on Reinforcement Learning for Transportation",
    'LOCATION': "Maui, Hawaii, USA",
    'DATE': "November 4-7, 2018",
    'WEBSITE': "https://sites.google.com/view/itsc18-rl",
    'DEADLINE': "Submission Deadline: April 15, 2018, 11:59 pm (AoE)",
    'CONFERENCE': 'IEEE.org/2018/ITSC',
    'PROGRAM_CHAIRS': 'IEEE.org/2018/ITSC/Program_Chairs',
    'REVIEWERS': 'IEEE.org/2018/ITSC/Reviewers',
    'SUBMISSION_INVITATION': 'IEEE.org/2018/ITSC/-/Submission',
    'BLIND_INVITATION': 'IEEE.org/2018/ITSC/-/Blind_Submission'
}

# April 15, 2018, 11:59 pm (AoE) = 4/16/18 11:59am GMT
DUE_DATE =  1523879999000

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
    reply_params={
        'readers': {'values-copied': [
            js_constants['CONFERENCE'], '{content.authorids}', '{signatures}']},
        'signatures': {'values-regex': '~.*|'+js_constants['CONFERENCE']},
        'writers': {'values-regex': '~.*|'+js_constants['CONFERENCE']}
    }
)

blind_inv = invitations.Submission(
    name = 'Blind_Submission',
    conference_id = js_constants['CONFERENCE'],
    duedate = DUE_DATE,
    mask = {
        'authors': {'values': ['Anonymous']},
        'authorids': {'values-regex': '.*'}
    },
    reply_params = {
        'signatures': {'values': [js_constants['CONFERENCE']]},
        'readers': {'values': ['everyone']}
    }
)

submission_process = process.MaskSubmissionProcess(
    '../process/submissionProcess.js', js_constants, mask = blind_inv)

submission_inv.add_process(submission_process)

# post both the submissions
submission_inv = client.post_invitation(submission_inv)
blind_inv = client.post_invitation(blind_inv)
print "posted invitation", submission_inv.id
print "posted invitation", blind_inv.id

'''
Create the homepage and add it to the conference group.
'''
instructions = ' '.join([
    '<p><strong>Important Information about Anonymity:</strong><br>',
    'When you post a submission to Intelligent Transportation Systems 2018,',
    'please provide the real names and email addresses of authors',
    'in the submission form below (but NOT in the manuscript).',
    'The <em>original</em> record of your submission will be private,',
    'and will contain your real name(s).',
    'Originals can be found in the "My Submitted Papers" tab below.',
    'Discussion forum pages for the anonymous versions of your paper can be found in the "My Papers Under Review" tab.',
    'You can also access the original record of your paper',
    'by clicking the "Modifiable Original" link in the discussion forum page of your paper.',
    'The PDF in your submission should not contain the names of the authors. </p>',
    '',
    '<p><strong>Conflict of Interest:</strong><br>',
    'Please make sure that your current and previous affiliations listed on your',
    'OpenReview <a href="/profile">profile page</a> is up-to-date to avoid conflict of interest.</p>',
    '',
    '<p><strong>Questions or Concerns:</strong><br>',
    'Please contact the OpenReview support team at',
    '<a href="mailto:info@openreview.net">info@openreview.net</a>',
    'with any questions or concerns. </p>'
    ])

js_constants['INSTRUCTIONS'] = instructions

homepage = webfield.Webfield(
    '../webfield/homepage.js',
    group_id = js_constants['CONFERENCE'],
    js_constants = js_constants,
)

this_conference = client.get_group(js_constants['CONFERENCE'])
this_conference.web = homepage.render()
this_conference = client.post_group(this_conference)
print "adding webfield to", this_conference.id