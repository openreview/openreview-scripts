import openreview
import argparse
from openreview import process
from openreview import conference
from openreview import webfield

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

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
    '<p><strong>Withdrawing Submissions:</strong><br>',
    'To withdraw your paper, navigate to the anonymous record of your submission',
    'and click on the "Withdraw" button. You will be asked to confirm your withdrawal.',
    'Withdrawn submissions will be removed from the system entirely.</p>',
    '',
    '<p><strong>Disclaimer:</strong><br>',
    'Although this preprint service is not officially affiliated',
    'with the Association for Computational Linguistics,',
    'submission of anonymous preprints on OpenReview is allowed under',
    '<a href="https://www.aclweb.org/adminwiki/index.php?title=ACL_Policies_for_Submission,_Review_and_Citation">the new ACL submission guidelines</a>.',
    'See also <a href="http://naacl2018.org/invited%20post/2017/11/27/acl-submission-policies.html">this blog post by Joakim Nivre</a>, ',
    'president of the ACL.',
    '',
    '<p><strong>Questions or Concerns:</strong><br>',
    'Please contact the OpenReview support team at',
    '<a href="mailto:info@openreview.net">info@openreview.net</a>',
    'with any questions or concerns. </p>'
    ])



naacl_preprint_server = conference.Conference(
    'aclweb.org/NAACL/2018/Preprint', short_phrase = 'NAACL Preprint Server')

submission_process = process.SubmissionProcess(mask = 'Blind_Submission')

naacl_preprint_server.add_submission('Submission',
    duedate = 1527757200000, # 17:00:00 EST on May 1, 2018
    process = submission_process
)

homepage = webfield.BasicHomepage(user_constants = {
    'TITLE': "NAACL 2018 Preprint Server (Unofficial)",
    'SUBTITLE': "Anonymous Preprint Server for the 16th Annual Conference of the North American Chapter of the Association for Computational Linguistics",
    'LOCATION': "New Orleans, Louisiana, USA",
    'DATE': "June 1 to June 6, 2018",
    'WEBSITE': "http://naacl2018.org/",
    'DEADLINE': "Submission Deadline: 5:00pm Eastern Standard Time, May 1, 2018",
    'INSTRUCTIONS': instructions
    })

naacl_preprint_server.add_homepage(homepage)

results = client.post_conference(naacl_preprint_server, overwrite=True)

for response_type in ['groups', 'invitations']:
    print response_type.upper(),':'
    for k, v in results[response_type].iteritems():
        print k
    print
