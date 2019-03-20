#!/usr/bin/python

import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('adai.ai/DAI/2019/Conference')
    builder.set_conference_name('Conference on Distributed Artificial Intelligence')
    builder.set_conference_short_name('DAI 2019')
    builder.set_homepage_header({
    'title': 'Conference on Distributed Artificial Intelligence',
    'subtitle': '',
    'deadline': 'Submission Deadline: June 4, 2019 23:59 GMT',
    'date': '13 - 15 Oct, 2019',
    'website': 'http://www.adai.ai',
    'location': 'Beijing China',
    'instructions': ''
    })
    builder.set_double_blind(True)

    builder.set_authorpage_header({'schedule':
      '''<h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: 4th of June, 2019</strong></li>
          <li>Authors can revise their paper as many times as needed up to the paper submission deadline.</li>
          <li>Authors can submit an abstract without a paper through 30th of May. After that the pdf is required to create a submission.</li>
          <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>
      <br>
      <h4>Rebuttal/Discussion Period</h4>
        <p><ul>
          <li><strong>18th-20th of July, 2019(23:59 UTC-12) </strong></li>
          <li>During the review period, authors will not be allowed to revise their paper. </li>
        </ul></p>
      <br>
      <h4>Decisions</h4>
        <p><ul>
          <li><strong>TBD </strong></li>
        </ul></p>'''})

    builder.set_reviewerpage_header({'schedule':
      '''<h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: June 4th, 2019</strong></li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>
      <br>
      <h4>Reviewing Period</h4>
        <p><ul>
          <li><strong>Due: 18th of July, 2019(23:59 UTC-12) </strong></li>
          <li>During the review period, authors will not be allowed to revise their paper. </li>
        </ul></p>
      <br>
      <h4>Rebuttal/Discussion Period</h4>
        <p><ul>
          <li><strong>18th-20th of July, 2019(23:59 UTC-12) </strong></li>
          <li>Final review due 23rd July, 2019(23:59 UTC-12) </li>
        </ul></p>'''})
    return builder.get_result()


