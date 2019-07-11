#!/usr/bin/python

import openreview
import datetime

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('adai.ai/DAI/2019/Conference')
    builder.set_conference_name('Conference on Distributed Artificial Intelligence')
    builder.set_conference_short_name('DAI 2019')
    builder.set_homepage_header({
        'title': 'Conference on Distributed Artificial Intelligence',
        'subtitle': '',
        'deadline': 'Submission Deadline: 18th of June, 2019 (23:59 UTC-12)',
        'date': '13 - 15 Oct, 2019',
        'website': 'http://www.adai.ai',
        'location': 'Beijing China',
        'instructions': '''<p><strong>Important Notes about Submitting a Paper:</strong>
                <ul>
                    <li>The paper length is limited to 6 pages, with 1 additional page containing only bibliographic references.</li>
                    <li>All work must be original, i.e., it must not have appeared in a conference proceedings, book, or journal and may not be under review for another archival conference.</li>
                    <li>The DAI 2019 review process is double blind. Please make sure that the submission does not disclose the author's identities or affiliation.</li>
                    <li>Neither submissions nor the reviewing process will be public.</li>
                </ul></p>
                <p> <strong>Questions or Concerns:</strong> <br>
Please contact the DAI 2019 Program chairs at <a href="mailto:dai2019chairs@gmail.com">dai2019chairs@gmail.com</a>.<br>
Please contact the OpenReview support team at <a href="mailto:info@openreview.net">info@openreview.net</a> with any OpenReview related questions or concerns.</p>'''
    })

    #builder.set_submission_stage(double_blind = True, due_date = datetime.datetime(2019, 6, 19, 11, 59), remove_fields = ['TL;DR'])
    #builder.set_bid_stage(due_date=datetime.datetime(2019,7,5,11,59), request_count = 30)
    #builder.set_review_stage(start_date =datetime.datetime(2019,7,6,11,59), due_date = datetime.datetime(2019,7,27,11,59))
    #builder.set_decision_stage(start_date = datetime.datetime(2019,7,27,11,59))
    builder.set_authorpage_header({'schedule':
      '''<h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: 18th of June, 2019</strong></li>
          <li>Authors can revise their paper as many times as needed up to the paper submission deadline.</li>
          <li>Authors can submit an abstract without a paper through 12th of June. After that the pdf is required to create a submission.</li>
          <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>
      <br>
      <h4>Decisions</h4>
        <p><ul>
          <li><strong>30th of July 2019 (23:59 UTC-12)</strong></li>
        </ul></p>'''})

    builder.set_reviewerpage_header({'schedule':
      '''<h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: June 18th, 2019</strong></li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>
      <br>
      <h4>Reviewing Period</h4>
        <p><ul>
          <li><strong>Due: 26th of July, 2019(23:59 UTC-12) </strong></li>
          <li>During the review period, authors will not be allowed to revise their paper. </li>
        </ul></p>'''})

    #builder.set_override_homepage(True)
    return builder.get_result()

