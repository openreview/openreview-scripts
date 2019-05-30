import openreview
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = openreview.helpers.get_conference(client, 'Skli7GteaN')

    title = '[ICLR 2020]: Invitation to Review'
    message = '''Dear {name},

        You have been nominated by the program chair committee of ICLR 2020 to serve as a reviewer.  As a respected researcher in the area, we hope you will accept and help us make the conference a success.

        Reviewers are also welcome to submit papers, so please also consider submitting to the conference!

        We will be using OpenReview.net and a reviewing process that we hope will be engaging and inclusive of the whole community.

        The success of the conference depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. We hope you will accept our invitation.

        To ACCEPT the invitation, please click on the following link:

        {accept_url}

        To DECLINE the invitation, please click on the following link:

        {decline_url}

        Please answer within 10 days.

        If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in.

        If you have any questions, please contact us at info@openreview.net.

        Cheers!

        Program Chairs
    '''


    emails = ['reviewer_iclr2020@mail.com', '~Mohit_Uniyal1']

    conference.recruit_reviewers(emails= emails, title = title , message = message)