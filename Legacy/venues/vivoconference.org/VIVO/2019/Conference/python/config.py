#!/usr/bin/python

import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('vivoconference.org/VIVO/2019/Conference')
    builder.set_conference_name('VIVO 2019 Conference')
    builder.set_conference_short_name('VIVO 2019 Conference')
    builder.set_homepage_header({
    'title': 'VIVO 2019 Conference',
    'deadline': 'Submission Deadline: 14th of April, 2019',
    'date': 'September 4-6, 2019',
    'website': 'http://vivoconference.org',
    'location': 'Podgorica, Montenegro',
    'instructions': '<p><strong>Questions or Concerns</strong></p><p>Please contact the OpenReview support team at <a href=\"mailto:info@openreview.net\">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>    Please contact the VIVO 2019 Program Chairs at <a href=\"mailto:conference@vivoweb.org\">conference@vivoweb.org</a> with any questions or concerns about conference administration or policy.</p><p>We are aware that some email providers inadequately filter emails coming from openreview.net as spam so please check your spam folder regularly.</p>'
    })
    builder.set_conference_submission_name('Submission')
    builder.set_submission_public(True)
    return builder.get_result()
