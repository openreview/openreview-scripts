#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('ICLR.cc/2019/Workshop/LLD')
    builder.set_conference_name('Learning from Limited Labeled Data')
    builder.set_conference_short_name('LLD 2019')
    builder.set_homepage_header({
        'title': 'Learning from Limited Labeled Data',
        'subtitle': 'ICLR 2019 Workshop',
        'deadline': 'Submission Deadline: March 15, 2019',
        'date': 'May 6 - May 9, 2019',
        'website': 'https://lld-workshop.github.io/',
        'location': 'New Orleans, Louisiana, United States',
        'instructions': ' '})
    return builder.get_result()


BLIND_SUBMISSION = 'ICLR.cc/2019/Workshop/LLD/-/Blind_Submission'