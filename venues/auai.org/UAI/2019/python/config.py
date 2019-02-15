#!/usr/bin/python

import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)
    builder.set_conference_id('auai.org/UAI/2019/Conference')
    builder.set_conference_name('Conference on Uncertainty in Artificial Intelligence')
    builder.set_conference_short_name('UAI 2019')
    builder.set_homepage_header({
    'title': 'UAI 2019',
    'subtitle': 'Conference on Uncertainty in Artificial Intelligence',
    'deadline': 'Abstract Submission Deadline: 11:59 pm Samoa Standard Time, March 4, 2019, Full Submission Deadline: 11:59 pm Samoa Standard Time, March 8, 2019',
    'date': 'June 22 - June 25, 2019',
    'website': 'http://auai.org/uai2019/',
    'location': 'Tel Aviv, Israel',
    'instructions': '''<p><strong>Important Information about Anonymity:</strong><br>
        When you post a submission to UAI 2019, please provide the real names and email addresses of authors in the submission form below (but NOT in the manuscript).
        The <em>original</em> record of your submission will be private, and will contain your real name(s).
        The PDF in your submission should not contain the names of the authors. </p>
        <p><strong>Conflict of Interest:</strong><br>
        Please make sure that your current and previous affiliations listed on your OpenReview <a href=\"/profile\">profile page</a> is up-to-date to avoid conflict of interest.</p>
        <p><strong>Questions or Concerns:</strong><br> Please contact the UAI 2019 Program chairs at <a href=\"mailto:chairs@uai2019.atlassian.net\">chairs@uai2019.atlassian.net</a>.
        <br>Please contact the OpenReview support team at <a href=\"mailto:info@openreview.net\">info@openreview.net</a> with any OpenReview related questions or concerns.
        </p>'''
    })
    print ('Homepage header set')
    builder.set_conference_area_chairs_name('Senior_Program_Committee')
    builder.set_conference_reviewers_name('Program_Committee')
    builder.set_double_blind(True)
    builder.set_override_homepage(True)
    return builder.get_result()

subject_areas = [
    "Algorithms: Approximate Inference",
    "Algorithms: Belief Propagation",
    "Algorithms: Distributed and Parallel",
    "Algorithms: Exact Inference",
    "Algorithms: Graph Theory",
    "Algorithms: Heuristics",
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
    "Applications: Other",
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
    "Representation: Probabilistic",
    "Representation: Other"
]

