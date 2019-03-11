#!/usr/bin/python

import openreview

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
    'instructions': 'Extended abstracts are up to 3 pages (excluding references and acknowledgements) and can, for example, focus on preliminary novel methodological ideas without extensive validation. We also specifically accept extended abstracts of recently published or submitted journal contributions to give authors the opportunity to present their work and obtain feedback from the community. Selection of abstracts is performed via a lightweight single-blind review process via OpenReview. All accepted abstracts will be presented as posters at the conference.</p>'
    })
    builder.set_conference_submission_name('Submission')
    builder.set_submission_public(True)
    return builder.get_result()


