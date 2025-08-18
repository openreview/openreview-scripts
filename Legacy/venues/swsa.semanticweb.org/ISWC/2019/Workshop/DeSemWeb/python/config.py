#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('swsa.semanticweb.org/ISWC/2019/Workshop/DeSemWeb')
    builder.set_conference_name('Decentralizing the Semantic Web')
    builder.set_conference_short_name('DeSemWeb 2019')
    builder.set_homepage_header({
    'title': 'Decentralizing the Semantic Web',
    'subtitle': 'ISWC2019 workshop',
    'deadline': 'Submission Deadline: 2019/7/24 11:59pm GMT',
    'date': '26 Oct 2019',
    'website': 'https://iswc2019.desemweb.org/',
    'location': 'The University of Auckland, New Zealand'
    })
    builder.set_double_blind(False)
    builder.set_submission_public(True)
    #builder.set_override_homepage(True)
    return builder.get_result()
