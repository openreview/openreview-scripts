#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('icaps-conference.org/ICAPS/2019/Workshop/XIAP')
    builder.set_conference_name('Explainable Artificial Intelligence Planning')
    builder.set_conference_short_name('ICAPS XIAP 2019')
    builder.set_homepage_header({
    'title': 'Explainable Artificial Intelligence Planning',
    'subtitle': 'ICAPS 2019 Workshop',
    'deadline': 'Submission Deadline: March 22, 2019',
    'date': 'July 11-15, 2019',
    'website': 'https://icaps19.icaps-conference.org/workshops/XIAP/index.html',
    'location': 'Berkeley, CA, USA'
    })
    builder.set_double_blind(True)

    return builder.get_result()

