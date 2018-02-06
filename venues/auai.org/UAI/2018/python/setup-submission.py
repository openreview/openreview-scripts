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

subject_areas = [
    "Algorithms: Approximate Inference",
    "Algorithms: Belief Propagation",
    "Algorithms: Distributed and Parallel",
    "Algorithms: Exact Inference",
    "Algorithms: Graph Theory",
    "Algorithms: Heuristics",
    "Algorithms: Lifted Inference",
    "Algorithms: MCMC methods",
    "Algorithms: Optimization",
    "Algorithms: Other",
    "Algorithms: Software and Tools",
    "Applications: Biology",
    "Applications: Databases",
    "Applications: Decision Support",
    "Applications: Diagnosis and Reliability",
    "Applications: Economics",
    "Applications: Education",
    "Applications: General",
    "Applications: Medicine",
    "Applications: Planning and Control",
    "Applications: Privacy and Security",
    "Applications: Robotics",
    "Applications: Sensor Data",
    "Applications: Social Network Analysis",
    "Applications: Speech",
    "Applications: Sustainability and Climate",
    "Applications: Text and Web Data",
    "Applications: User Models",
    "Applications: Vision",
    "Data: Big Data",
    "Data: Multivariate",
    "Data: Other",
    "Data: Relational",
    "Data: Spatial",
    "Data: Temporal or Sequential",
    "Learning: Active Learning",
    "Learning: Classification",
    "Learning: Clustering",
    "Learning: Deep Learning",
    "Learning: General",
    "Learning: Nonparametric Bayes",
    "Learning: Online and Anytime Learning",
    "Learning: Other",
    "Learning: Parameter Estimation",
    "Learning: Probabilistic Generative Models",
    "Learning: Ranking",
    "Learning: Recommender Systems",
    "Learning: Regression",
    "Learning: Reinforcement Learning",
    "Learning: Relational Learning",
    "Learning: Relational Models",
    "Learning: Scalability",
    "Learning: Semi-Supervised Learning",
    "Learning: Structure Learning",
    "Learning: Structured Prediction",
    "Learning: Theory",
    "Learning: Unsupervised",
    "Methodology: Bayesian Methods",
    "Methodology: Calibration",
    "Methodology: Elicitation",
    "Methodology: Evaluation",
    "Methodology: Human Expertise and Judgement",
    "Methodology: Other",
    "Methodology: Probabilistic Programming",
    "Models: Bayesian Networks",
    "Models: Directed Graphical Models",
    "Models: Dynamic Bayesian Networks",
    "Models: Markov Decision Processes",
    "Models: Mixed Graphical Models",
    "Models: Other",
    "Models: Relational Models",
    "Models: Topic Models",
    "Models: Undirected Graphical Models",
    "None of the above",
    "Principles: Causality",
    "Principles: Cognitive Models",
    "Principles: Decision Theory",
    "Principles: Game Theory",
    "Principles: Information Theory",
    "Principles: Other",
    "Principles: Probability Theory",
    "Principles: Statistical Theory",
    "Representation: Constraints",
    "Representation: Dempster-Shafer",
    "Representation: Fuzzy Logic",
    "Representation: Influence Diagrams",
    "Representation: Non-Probabilistic Frameworks",
    "Representation: Probabilistic"
]

'''
Set the variable names that will be used in various pieces of executable javascript.

'''

js_constants = {
    'TITLE': "UAI 2018",
    'SUBTITLE': "Conference on Uncertainty in Artificial Intelligence",
    'LOCATION': "Monterey, California, USA",
    'DATE': "August 6 - 10, 2018",
    'WEBSITE': "http://auai.org/uai2018/index.php",
    'DEADLINE': "Submission Deadline: March 9th, 2018, 11:59 pm SST (Samoa Standard Time)",
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

submission_inv = invitations.Submission(
    name = 'Submission',
    conference_id = 'auai.org/UAI/2018',
    duedate = 1520589599000, #  (GMT): Friday, 9 March 2018 09:59:59
    reply_params = {
        'readers': {'values-copied': [
                'auai.org/UAI/2018', '{content.authorids}', '{signatures}']},
        'signatures': {'values-regex': '~.*|auai.org/UAI/2018'},
        'writers': {'values': ['auai.org/UAI/2018']}
    },
    content_params = {
        'subject areas': {'required': True, 'values-dropdown': subject_areas}
    }
)

blind_inv = invitations.Submission(
    name = 'Blind_Submission',
    conference_id = 'auai.org/UAI/2018',
    duedate = 1520589599000, #  (GMT): Friday, 9 March 2018 09:59:59
    mask = {
        'authors': {'values': ['Anonymous']},
        'authorids': {'values-regex': '.*'}
    },
    reply_params = {
        'signatures': {'values': ['auai.org/UAI/2018']},
        'readers': {'values-regex': 'auai.org/UAI/2018.*'}
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
Create a bid invitation.
'''

bid_invitation = invitations.AddBid(
    name = 'Add_Bid',
    conference_id = 'auai.org/UAI/2018',
    duedate = 1527757200000, # 17:00:00 EST on May 1, 2018
    completion_count = 50,
    inv_params = {
        'readers': ['auai.org/UAI/2018','auai.org/UAI/2018/Program_Chairs'],
        'invitees': ['auai.org/UAI/2018/Program_Chairs']}
        #'readers': ['auai.org/UAI/2018','auai.org/UAI/2018/Program_Committee'],
        #'invitees': ['auai.org/UAI/2018/Program_Committee']}
    )

bid_webfield = webfield.Webfield(
    '../webfield/bidWebfield.js',
    group_id = 'auai.org/UAI/2018',
    js_constants = js_constants,
    subject_areas = subject_areas
    )

bid_invitation.web = bid_webfield.render()

bid_invitation = client.post_invitation(bid_invitation)
print "posted invitation", bid_invitation.id
'''
Create the homepage and add it to the conference group.

'''
instructions = ' '.join([
    '<p><strong>Important Information about Anonymity:</strong><br>',
    'When you post a submission to this anonymous preprint server,',
    'please provide the real names and email addresses of authors',
    'in the submission form below (but NOT in the manuscript).',
    'The <em>original</em> record of your submission will be private,',
    'and will contain your real name(s).',
    'Originals can be found in your OpenReview <a href="/tasks">Tasks page</a>.',
    'You can also access the original record of your paper',
    'by clicking the "Modifiable Original" link in the discussion forum page of your paper.',
    'The PDF in your submission should not contain the names of the authors. </p>',
    '',
    '<p><strong>Conflict of Interest:</strong><br>',
    'Please make sure that your current and previous affiliations listed on your',
    'OpenReview <a href="/profile">profile page</a> is up-to-date to avoid conflict of interest.</p>',
    '',
    #'<p><strong>Posting Revisions to Submissions:</strong><br>',
    #'To post a revision to your paper, navigate to the original version,'
    #'and click on the "Add Revision" button.',
    #'Revisions on originals propagate all changes to anonymous copies,',
    #'while maintaining anonymity.',
    #'Adding revision will not be possible after the submission deadline.</p>',
    #''
    '<p><strong>Bidding on Papers (for reviewers)</strong><br>',
    'If you are serving as a member of the Program Committee (as a reviewer), you can',
    'bid on papers in the list below. You can also use the ',
    '<a href="invitation?id=auai.org/UAI/2018/-/Add_Bid">Bidding Console</a> for better',
    'navigational features.',
    'These features will be made available once the bidding period starts. </p>',
    '',
    '<p><strong>Questions or Concerns:</strong><br>',
    'Please contact the OpenReview support team at',
    '<a href="mailto:info@openreview.net">info@openreview.net</a>',
    'with any questions or concerns. </p>'
    ])

js_constants['INSTRUCTIONS'] = instructions

homepage = webfield.Webfield(
    '../webfield/homepage.js',
    group_id = 'auai.org/UAI/2018',
    js_constants = js_constants,
    subject_areas = subject_areas
)

uai2018_conference = client.get_group('auai.org/UAI/2018')
uai2018_conference.web = homepage.render()
uai2018_conference = client.post_group(uai2018_conference)
print "adding webfield to", uai2018_conference.id
