import openreview
import argparse

# Make sure you modify the subject line and message content before executing the script

subject_line = '[UAI 19] Insert the subject line here'

message = '''Dear Program Committee Member,

Insert the plain text email body here.

Sincerely,
The Program Chairs'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="in most cases, this should be \"https://openreview.net\"")
    parser.add_argument('--username', help="the email address that you use to log into OpenReview")
    parser.add_argument('--password', help="your OpenReview account password")
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    '''
    recipient_groups is a list of Group IDs that this message will be sent to.

    These can be IDs of groups that contain multiple users, such as the Program Committee group,
    or it can be IDs of groups that represent individuals (for example, email addresses, which
    are treated in OpenReview as Groups with a single member).

    '''
    recipient_groups = [
        'auai.org/UAI/2019/Conference/Program_Committee'
    ]

    confirmed_recipients = client.send_mail(
        subject_line,
        recipient_groups,
        message
    )

    print('confirmed recipients: ', confirmed_recipients)

