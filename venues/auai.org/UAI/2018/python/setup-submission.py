import openreview
import argparse
from openreview import conference
from openreview import process
from openreview import webfield

client = openreview.Client()
print 'connecting to {0}'.format(client.baseurl)

'''
Set the variable names that will be used in various pieces of executable javascript.

'''

js_constants = {
    'TITLE': "UAI 2018",
    'SUBTITLE': "Conference on Uncertainty in Artificial Intelligence",
    'LOCATION': "TBD",
    'DATE': "TBD",
    'WEBSITE': "http://auai.org/uai2018/index.php",
    'DEADLINE': "Submission Deadline: TBD",
    'CONFERENCE': 'auai.org/UAI/2018',
    'PROGRAM_CHAIRS': 'auai.org/UAI/2018/Program_Chairs',
    'REVIEWERS': 'auai.org/UAI/2018/Program_Committee',
    'AREA_CHAIRS': 'auai.org/UAI/2018/Senior_Program_Committee',
    'SUBMISSION_INVITATION': 'auai.org/UAI/2018/-/Submission',
    'BLIND_INVITATION': 'auai.org/UAI/2018/-/Blind_Submission',
    'RECRUIT_REVIEWERS': 'auai.org/UAI/2018/-/PC_Invitation',
}

'''
Create a submission invitation (a call for papers) and a blind submission
invitation.

The submission invitation is the form that users fill out to submit a paper.
An anonymous copy is created by the submission invitation's process function;
this copy is defined by the blind submission invitation.

'''

submission_inv = conference.Submission(
    name = 'Submission',
    conference_id = 'auai.org/UAI/2018',
    duedate = 1527757200000, # 17:00:00 EST on May 1, 2018
    reply_params = {
        'readers': {'values-copied': [
                'auai.org/UAI/2018', '{content.authorids}', '{signatures}']},
        'signatures': {'values-regex': '~.*|auai.org/UAI/2018'},
        'writers': {'values': ['auai.org/UAI/2018']}
    }
)

blind_inv = conference.Submission(
    name = 'Blind_Submission',
    conference_id = 'auai.org/UAI/2018',
    duedate = 1527757200000, # 17:00:00 EST on May 1, 2018
    mask = {
        'authors': {'values': ['Anonymous']},
        'authorids': {'values-regex': '.*'}
    },
    reply_params = {
        'signatures': {'values': ['auai.org/UAI/2018']}
    }

)

submission_process = process.MaskSubmissionProcess(js_constants, mask = blind_inv)

submission_inv.add_process(submission_process)

submission_inv = client.post_invitation(submission_inv)
blind_inv = client.post_invitation(blind_inv)


'''
Create the homepage and add it to the conference group.

'''
instructions = ' '.join([
    '<p><strong>Important Information about Anonymity:</strong><br>',
    'When you post a submission to this anonymous preprint server,',
    'please provide the real names and email addresses of authors',
    'in the submission form below.',
    'An anonymous record of your paper will appear in the list below,',
    'and will be visible to the public.',
    'The <em>original</em> record of your submission will be private,',
    'and will contain your real name(s).',
    'Originals can be found in your OpenReview <a href="/tasks">Tasks page</a>.',
    'You can also access the original record of your paper',
    'by clicking the "Modifiable Original" link in the discussion forum page of your paper.',
    'The PDF in your submission should not contain the names of the authors. </p>',
    '',
    '<p><strong>Posting Revisions to Submissions:</strong><br>',
    'To post a revision to your paper, navigate to the original version,'
    'and click on the "Add Revision" button.',
    'Revisions on originals propagate all changes to anonymous copies,',
    'while maintaining anonymity.</p>',
    '',
    '<p><strong>Questions or Concerns:</strong><br>',
    'Please contact the OpenReview support team at',
    '<a href="mailto:info@openreview.net">info@openreview.net</a>',
    'with any questions or concerns. </p>'
    ])

js_constants['INSTRUCTIONS'] = instructions

homepage = webfield.TabbedHomepage(
    group_id = 'auai.org/UAI/2018',
    js_constants = js_constants
)

uai2018_conference = client.get_group('auai.org/UAI/2018')
uai2018_conference.web = homepage.render()
uai2018_conference = client.post_group(uai2018_conference)
