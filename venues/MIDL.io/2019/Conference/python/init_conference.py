#!/usr/bin/python

import sys, os
import argparse
import datetime
import openreview
import config

"""
OPTIONAL SCRIPT ARGUMENTS
	baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
 	username - the email address of the logging in user
	password - the user's password
"""

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print('connecting to {0}'.format(client.baseurl))

builder = openreview.conference.ConferenceBuilder(client)

builder.set_conference_id(config.CONFERENCE_ID)
builder.set_conference_name('Medical Imaging with Deep Learning')
builder.set_homepage_header({
'title': 'Medical Imaging with Deep Learning',
'subtitle': 'MIDL 2019 Conference',
'deadline': 'Submission Deadline: 13th of December, 2018',
'date': '8-10 July 2019',
'website': 'http://2019.midl.io',
'location': 'London',
'instructions': 'Full papers contain well-validated applications or methodological developments of deep learning algorithms in medical imaging. There is no strict limit on paper length. However, we strongly recommend keeping full papers at 8 pages (excluding references and acknowledgements). An appendix section can be added if needed with additional details but must be compiled into a single pdf. The appropriateness of using pages over the recommended page length will be judged by reviewers. All accepted papers will be presented as posters with a selection of these papers will also be invited for oral presentation.<br/><br/> <p><strong>Questions or Concerns</strong></p><p>Please contact the OpenReview support team at <a href=\"mailto:info@openreview.net\">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>    Please contact the MIDL 2019 Program Chairs at <a href=\"mailto:program-chairs@midl.io\">program-chairs@midl.io</a> with any questions or concerns about conference administration or policy.</p><p>We are aware that some email providers inadequately filter emails coming from openreview.net as spam so please check your spam folder regularly.</p>'
})
builder.set_conference_submission_name('Full_Submission')
conference = builder.get_result()

conference.open_submissions(due_date = datetime.datetime(2018, 12, 13, 18, 00), public = True, additional_fields = {
        "code of conduct": {
            "order": 11,
            "description": "As a professional scientific community, we are committed to providing an atmosphere that encourages the free expression and exchange of ideas. Consistent with this commitment, it is the policy of the MIDL conference series that all participants in all activities will enjoy a welcoming environment free from unlawful discrimination, harassment and retaliation. All participants in activities of the MIDL conference series also agree to comply with all rules and conditions of the activities, which are subject to change without notice. This policy applies to all participants — attendees, organizers, reviewers, speakers, sponsors, guests, staff, contractors, exhibitors, and volunteers at our conference sessions and conference-related social events — who are required to agree with this code of conduct both during the event and on official communication channels, including social media.\n\nAll individuals must behave responsibly in MIDL activities in which they participate, at the MIDL conference, related events and social activities at on-site and off-site locations, and in related online communities and social media. Threatening physical or verbal actions and disorderly or disruptive conduct will not be tolerated. Harassment, including verbal comments relating to gender, sexual orientation, disability, race, ethnicity, religion, age, national origin, gender identity or expression, veteran status or other protected status, or sexual images in public spaces, deliberate intimidation, stalking, unauthorized or inappropriate photography or recording, inappropriate physical contact, and unwelcome sexual attention, will not be tolerated. All individuals participating in activities of the MIDL conference series must comply with these standards of behavior.\n\nViolations should be reported in a timely fashion to the MIDL ombudsperson via ombudsperson@midl.io. The ombudsperson may refuse to deal with a dispute. This decision is at the sole discretion of the ombudsperson.\n\nUnacceptable behavior may cause removal or denial of access to meeting facilities or activities, and other penalties, without refund of any applicable registration fees or costs. In addition, violations may be reported to the individual’s employer. Offenders may be banned from future activities of the MIDL conference series.",
            "value-checkbox": "I have read and accept the code of conduct.",
            "required": True
        },
        "remove if rejected": {
            "order": 12,
            "value-checkbox": "Remove submission if paper is rejected.",
            "required": False
        }
    })
