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

    print ('inviting SPC members now')

    spc_emails = []
    spc_name = []
    
    message = '''Dear {first name},

    As program chairs of UAI 2019, it is our pleasure to invite you to serve as a member of the Senior Program Committee (SPC) for the 2019 Uncertainty in AI Conference (UAI). The conference will be held in Tel Aviv, Israel from July 22 to July 25, 2019.

    UAI is the premier international conference on research related to representation, inference, learning and decision making in the presence of uncertainty, as they relate to the fields of artificial intelligence and machine learning. As a Senior Program Committee Member for the UAI 2019 conference you will help us select a high quality program for the conference. We count on your help and your expertise.

    Your main responsibilities will be to help to control the quality of the reviewing process and include:
    a) Help us form the Program Committee (PC) by suggesting 5 to 10 potential members.
    b) Help us with reviewer assignment by suggesting 3 to 5 reviewers (from the PC) for each paper assigned to you, if you happen to know some good candidates. Based on recent years, we expect that you will be assigned between 8 to 10 papers.
    c) Read the reviews for the papers assigned to you and, if necessary, ask the reviewers to improve their quality.
    d) Proactively lead the discussions among reviewers.
    e) Write an informative meta-review for each paper assigned to you, and make an accept/reject recommendation.

    To ACCEPT the invitation, please click on the following link:

    {accept_url}

    To DECLINE the invitation, please click on the following link:

    {decline_url}

    The timeline of SPC actions is the following:

    1. By Feb 20, 2019: Please respond by clicking above indicating whether you accept the SPC invitation or not.
    2. March 4-10, 2019: Enter bids for submitted papers.
    3. March 17-20, 2019: View the initial paper assignment. Propose alternative reviewers which will be taken into account in the final assignment. Report any possible conflict of interest as soon as possible so that we can assign the paper to another SPC
    4. March 21 - April 21, 2019: Review period. If a reviewer drops out, we might need your help in finding additional emergency reviewers for the paper.
    5. April 13 - April 21, 2019: Check reviews and chase reviewers for missing ones.
    6. April 25 to April 27, 2019: Discussion period with reviewers, suggest further reviewers if necessary.
    7. By May 7, 2019, write a meta-review for each paper.
    8. May 7 - May 13, 2019: Your meta-reviews will be used for making the final decisions. If we need additional input on a particular paper we might contact you.

    We really hope you will be able to accept our invitation and help us select a high quality program for UAI 2019.  Please reply to this invitation by following the link at the beginning of this message, no later than February 20th, 2019.

    Thanks in advance for your help!

    Ryan Adams, Vibhav Gogate
    UAI 2019 Program Chairs
    uai2019chairs@gmail.com
    '''

    for fname, email in zip (spc_name, spc_emails):
        formatted_msg = message.replace('{first name}', fname)
        conference.recruit_reviewers(
            emails = [email],
            title = 'UAI 2019: Invitation to serve on the Senior Program Committee',
            message = formatted_msg,
            reviewers_name = 'Senior_Program_Committee'
        )

    print ('done')
