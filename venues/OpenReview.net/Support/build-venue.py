import argparse
import openreview

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help='base url')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('id', help='enter request form id')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

conference = openreview.helpers.get_conference(client, args.id)

if conference.is_new():
    subject = 'Your venue is available in OpenReview',
    message = '''
Hi Program Chairs,

Thanks for submitting a venue request.

We have set up the venue based on the information that you provided here: https://openreview.net/forum?id={noteId}

You can use the following links to access to the conference:

Conference home page: https://openreview.net/group?id={conference_id}
Conference Program Chairs console: https://openreview.net/group?id={program_chairs_id}

If you need to make a change to the information provided in your request form, please edit it directly. We will update your venue accordingly.

If you need special features that are not included in your request form, please contact us at info@openreview.net and we will assist you.

Thanks!

OpenReview Team
    '''.format(noteId = args.id, conference_id = conference.get_id(), program_chairs_id = conference.get_program_chairs_id())
    recipients = [conference.get_program_chairs_id()]
    client.send_mail(subject, recipients, message)

print('Conference: ', conference.get_id())