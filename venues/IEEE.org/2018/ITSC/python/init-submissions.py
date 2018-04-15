import openreview
import argparse
import os
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
    'DEADLINE': "Submission Deadline: May 1, 2018, 11:59 pm (AoE)",
    'CONFERENCE': 'IEEE.org/2018/ITSC',
    'PROGRAM_CHAIRS': 'IEEE.org/2018/ITSC/Program_Chairs',
    'REVIEWERS': 'IEEE.org/2018/ITSC/Reviewers',
    'SUBMISSION_INVITATION': 'IEEE.org/2018/ITSC/-/Submission',
    'BLIND_INVITATION': 'IEEE.org/2018/ITSC/-/Blind_Submission',
    'COMMENT_INVITATION': 'IEEE.org/2018/ITSC/-/Comments'
}

# May 1, 2018, 11:59 pm (AoE) = 5/2/18 noon GMT
DUE_DATE =  tools.timestamp_GMT(2018,5,2,12)

groups = tools.build_groups(js_constants['CONFERENCE'])
for g in groups:
    print "posting group {0}".format(g.id)
    client.post_group(g)



pc_params = {
    'readers': [js_constants['CONFERENCE'], js_constants['PROGRAM_CHAIRS']],
    'writers': [js_constants['CONFERENCE']],
    'signatures': [u'~Super_User1'],
    'signatories': [js_constants['CONFERENCE'], js_constants['PROGRAM_CHAIRS']],
    'members': []
}
client.post_group(openreview.Group(js_constants['PROGRAM_CHAIRS'], **pc_params))

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


comment_inv = invitations.Comment(
    name = 'Comment',
    conference_id = js_constants['CONFERENCE'],
    process = os.path.join(os.path.dirname(__file__),'../process/commentProcess.js'),
    invitation = js_constants['BLIND_INVITATION'],
)
client.post_invitation(comment_inv)

print "posted invitation", comment_inv.id
'''
Create the homepage and add it to the conference group.
'''
instructions = ' '.join([

    '<p>When you post your submission, the pdf should <strong>not</strong> contain the names of the authors. ',
    'Please provide real names and email addresses of authors in the form.',
    'An anonymous record of your paper will be visible to the public.<br>',
    'The <em>original</em> record of your submission will be private,',
    'and will contain your real name(s).',
    'Originals can be found in your OpenReview Tasks page or through the "Original" link',
    'in the discussion forum page of your paper.<br></p>',
    '<p><strong>To Edit Submissions:</strong><br>',
    'To edit your paper, navigate to the original version, and click on the edit button if available. ',
    'Edits are not allowed during the formal review process.',
    'Edits to the originals propagate all changes to anonymous copies, while maintaining anonymity.</p>',
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