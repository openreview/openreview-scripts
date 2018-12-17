#!/usr/bin/python

import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('MIDL.io/2019/Conference')
    builder.set_conference_name('Medical Imaging with Deep Learning')
    builder.set_conference_short_name('MIDL 2019')
    builder.set_homepage_header({
    'title': 'Medical Imaging with Deep Learning',
    'subtitle': 'MIDL 2019 Conference',
    'deadline': 'Submission Deadline: 17th of December, 2018, 17:00 UTC',
    'date': '8-10 July 2019',
    'website': 'http://2019.midl.io',
    'location': 'London',
    'instructions': 'Full papers contain well-validated applications or methodological developments of deep learning algorithms in medical imaging. There is no strict limit on paper length. However, we strongly recommend keeping full papers at 8 pages (excluding references and acknowledgements). An appendix section can be added if needed with additional details but must be compiled into a single pdf. The appropriateness of using pages over the recommended page length will be judged by reviewers. All accepted papers will be presented as posters with a selection of these papers will also be invited for oral presentation.<br/><br/> <p><strong>Questions or Concerns</strong></p><p>Please contact the OpenReview support team at <a href=\"mailto:info@openreview.net\">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>    Please contact the MIDL 2019 Program Chairs at <a href=\"mailto:program-chairs@midl.io\">program-chairs@midl.io</a> with any questions or concerns about conference administration or policy.</p><p>We are aware that some email providers inadequately filter emails coming from openreview.net as spam so please check your spam folder regularly.</p>'
    })
    builder.set_conference_submission_name('Full_Submission')
    return builder.get_result()


