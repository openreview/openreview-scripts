import openreview
import argparse

subject_line = '[COLT 19] Insert your subject line here'
message = '''Dear Program Committee Member,

This is a sample message.

Sincerely,
The Program Chairs'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="in most cases, this should be \"https://openreview.net\"")
    parser.add_argument('--username', help="the email address that you use to log into OpenReview")
    parser.add_argument('--password', help="your OpenReview account password")
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    program_committee_group = client.get_group('learningtheory.org/COLT/2019/Conference/Program_Committee')

    '''
    recipient_groups is a list of Group IDs that this message will be sent to.

    These can be IDs of groups that contain multiple users, such as the Program Committee group,
    or it can be IDs of groups that represent individuals (for example, email addresses, which
    are treated in OpenReview as Groups with a single member).

    '''
    recipient_groups = [
        'learningtheory.org/COLT/2019/Conference/Program_Committee'
    ]

    confirmed_recipients = client.send_mail(
        subject_line,
        recipient_groups,
        message
    )

    print('confirmed_recipients', confirmed_recipients)

