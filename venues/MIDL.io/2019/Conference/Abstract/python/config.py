#!/usr/bin/python

import openreview
import datetime

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('MIDL.io/2019/Conference/Abstract')
    builder.set_conference_name('Medical Imaging with Deep Learning')
    builder.set_conference_short_name('MIDL 2019')
    builder.set_homepage_header({
    'title': 'Medical Imaging with Deep Learning',
    'subtitle': 'MIDL 2019 Conference',
    'deadline': 'Abstract Submission Deadline: 12th of April, 2019, 17:00 UTC',
    'date': '8-10 July 2019',
    'website': 'http://2019.midl.io',
    'location': 'London',
    'instructions': '<p>Extended abstracts are up to 3 pages (excluding references and acknowledgements) and can, for example, focus on preliminary novel methodological ideas without extensive validation. We also specifically accept extended abstracts of recently published or submitted journal contributions to give authors the opportunity to present their work and obtain feedback from the community. Selection of abstracts is performed via a lightweight single-blind review process via OpenReview. All accepted abstracts will be presented as posters at the conference. We note that not all dual submissions are allowed. For further information on the dual submission policy, please read <a href="http://2019.midl.io/submissions/" target="_blank">http://2019.midl.io/submissions/</a>.</p>'
    })
    builder.use_legacy_invitation_id(True)
    builder.set_submission_stage(double_blind = False, public = True, due_date=datetime.datetime(2019, 4, 12, 17, 00), additional_fields={
        "code of conduct": {
            "order": 11,
            "description": "As a professional scientific community, we are committed to providing an atmosphere that encourages the free expression and exchange of ideas. Consistent with this commitment, it is the policy of the MIDL conference series that all participants in all activities will enjoy a welcoming environment free from unlawful discrimination, harassment and retaliation. All participants in activities of the MIDL conference series also agree to comply with all rules and conditions of the activities, which are subject to change without notice. This policy applies to all participants — attendees, organizers, reviewers, speakers, sponsors, guests, staff, contractors, exhibitors, and volunteers at our conference sessions and conference-related social events — who are required to agree with this code of conduct both during the event and on official communication channels, including social media.\n\nAll individuals must behave responsibly in MIDL activities in which they participate, at the MIDL conference, related events and social activities at on-site and off-site locations, and in related online communities and social media. Threatening physical or verbal actions and disorderly or disruptive conduct will not be tolerated. Harassment, including verbal comments relating to gender, sexual orientation, disability, race, ethnicity, religion, age, national origin, gender identity or expression, veteran status or other protected status, or sexual images in public spaces, deliberate intimidation, stalking, unauthorized or inappropriate photography or recording, inappropriate physical contact, and unwelcome sexual attention, will not be tolerated. All individuals participating in activities of the MIDL conference series must comply with these standards of behavior.\n\nViolations should be reported in a timely fashion to the MIDL ombudsperson via ombudsperson@midl.io. The ombudsperson may refuse to deal with a dispute. This decision is at the sole discretion of the ombudsperson.\n\nUnacceptable behavior may cause removal or denial of access to meeting facilities or activities, and other penalties, without refund of any applicable registration fees or costs. In addition, violations may be reported to the individual’s employer. Offenders may be banned from future activities of the MIDL conference series.",
            "value-checkbox": "I have read and accept the code of conduct.",
            "required": True
        },
        "remove if rejected": {
            "order": 12,
            "description": "Optional",
            "value-checkbox": "Remove submission from public view if paper is rejected.",
            "required": False
        },
        "link": {
            "description": "If submitted elsewhere, provide link to the article.",
            "value-regex": ".{1,500}",
            "required": False
        }

    })

    # builder.set_override_homepage(True)
    return builder.get_result()


