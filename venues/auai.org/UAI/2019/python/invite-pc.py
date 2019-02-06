import argparse
import openreview
from openreview import invitations
import datetime
import os
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    print ('inviting PC members now')

    pc_emails = []
    pc_name = []
    
    message = '''Dear {first name},

    As program co-chairs of UAI 2019, it is our pleasure to invite you to serve as a member of the Program Committee (PC) for the 2019 Uncertainty in AI Conference (UAI). The conference will be held in Tel Aviv, Israel from July 22 to July 25, 2019.

    UAI is the premier international conference on research related to representation, inference, learning and decision making in the presence of uncertainty as they relate to the field of artificial intelligence. The Program Committee has a major responsibility in the selecting a high quality program for the conference: we count on your help and your expertise. The success of the conference depends a great deal on having experts such as you providing constructive reviews for submitted papers.

    We expect you will have about 5-7 papers to review, which hopefully is not too heavy a load (see a detailed timeline below). We would be delighted if you can accept this invitation, and help us turning UAI 2019 into a great event.

    Please let us know by Feb 28th whether you will be able to join the program committee.

    To ACCEPT the invitation, please click on the following link:

    {accept_url}

    To DECLINE the invitation, please click on the following link:

    {decline_url}

    The timeline of PC actions is the following:
    1. By Feb 20th, 2019: Please respond by clicking above indicating whether you accept the PC invitation or not.
    2. March 4-10, 2019: Enter bids for submitted papers.
    3. March 21 to April 21, 2019: Review period.
    4. April 25 to April 27, 2019: Discussion period, and editing the reviews accordingly.
    5. May 13th:  Final decisions sent to authors.

    We really hope you will be able to accept our invitation and help us select a high quality program for UAI 2019!

    Thanks in advance for your help. If you have any questions please contact us at chairs@uai2019.atlassian.net.

    Best regards,

    Ryan Adams, Vibhav Gogate
    UAI 2019 Program Chairs
    chairs@uai2019.atlassian.net
    '''

    for fname, email in zip (pc_name, pc_emails):
        formatted_msg = message.replace('{first name}', fname)
        conference.recruit_reviewers(
            emails = [email],
            title = 'UAI 2019: Invitation to serve on the Program Committee',
            message = formatted_msg,
            reviewers_name = 'Program_Committee'
        )

    print ('done')
