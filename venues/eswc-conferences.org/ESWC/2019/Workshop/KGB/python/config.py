#!/usr/bin/python

import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('eswc-conferences.org/ESWC/2019/Workshop/KGB')
    builder.set_conference_name('Knowledge Graph Building Workshop')
    builder.set_conference_short_name('KGB 2019')
    builder.set_homepage_header({
    'title': 'Knowledge Graph Building Workshop',
    'subtitle': 'Co-located with the Extended Semantic Web Conference 2019',
    'deadline': 'Submission Deadline: 1st of March, 2019, 23:59 Hawaii time',
    'date': '3 June 2019',
    'website': 'http://kgb-workshop.org/',
    'location': 'Portorož, Slovenia',
    'instructions': ' '
    })
    builder.set_conference_submission_name('Submission')
    builder.set_submissions_public(True)
    return builder.get_result()


