import argparse
import openreview

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('request_id', help='enter request form id')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = openreview.helpers.get_conference(client, args.request_id)

    print ('inviting reviewers now')

    reviewer_emails = ['muniyal@cs.umass.edu', 'mbok@cs.umass.edu']
    reviewer_names = ['Mohit', 'Melisa']

    message = '''Dear {first_name},

    You have been nominated by the program chair committee of RSS 2019 Workshop to serve as a reviewer. As a respected researcher in the area, we hope you will accept and help us make the workshop a success.

    Reviewers are also welcome to submit papers, so please also consider submitting to the workshop!

    We will be using OpenReview.net and a reviewing process that we hope will be engaging and inclusive of the whole community.

    The success of the workshop depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers.

    To ACCEPT the invitation, please click on the following link:

    {accept_url}

    To DECLINE the invitation, please click on the following link:

    {decline_url}

    Please answer within 10 days.

    If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using. Visit http://openreview.net/profile after logging in.

    If you have any questions, please contact us at info@openreview.net.

    Cheers!

    Program Chairs
    '''

    for fname, email in zip (reviewer_names, reviewer_emails):
        formatted_msg = message.replace('{first_name}', fname)
        conference.recruit_reviewers(
            emails = [email],
            title = 'RSS 2019 Workshop: Invitation to serve as a reviewer',
            message = formatted_msg,
        )

    print ('done')
