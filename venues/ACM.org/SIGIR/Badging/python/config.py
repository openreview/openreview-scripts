'''
ACM SIGIR Badging demo configuration
https://acm.org
'''
import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('ACM.org/SIGIR/Badging')
    builder.set_conference_name('ACM - Special Interests Group on Information Retrieva')
    builder.set_conference_short_name('ACM Badging')
    builder.set_homepage_header({
    'title': 'ACM SIGIR Badging',
    'subtitle': 'ACM - Special Interests Group on Information Retrieval',
    'date': 'Continuous process',
    'website': 'http://sigir.org/',
    'location': 'Global',
    'instructions': '<p><strong>Questions or Concerns</strong></p>\
    <p>Please contact the OpenReview support team at \
    <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>\
    </p>'
    })
    builder.set_homepage_layout('simple')
    builder.set_submissions_public(True)
    builder.set_conference_program_chairs_name('Chairs')
    return builder.get_result()
