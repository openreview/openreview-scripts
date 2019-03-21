#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('icaps-conference.org/ICAPS/2019/Workshop/XAIP')
    builder.set_conference_name('Explainable Artificial Intelligence Planning')
    builder.set_conference_short_name('ICAPS XAIP 2019')
    builder.set_homepage_header({
    'title': 'Explainable Artificial Intelligence Planning',
    'subtitle': 'ICAPS 2019 Workshop on Explainable AI Planning (XAIP)',
    'deadline': 'Submission Deadline: March 31, 2019',
    'date': 'July 11-15, 2019',
    'website': 'https://icaps19.icaps-conference.org/workshops/XAIP/',
    'location': 'Berkeley, CA, USA'
    })
    builder.set_double_blind(True)
    builder.set_submission_public(True)
    builder.set_override_homepage(True)
    return builder.get_result()

