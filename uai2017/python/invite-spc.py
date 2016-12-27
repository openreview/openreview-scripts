#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

## Import statements
import argparse
import csv
import sys
from openreview import *
import re

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)


message = """
Dear %s,

As program chairs of UAI 2017, it is our pleasure to invite you to serve as a member of the Senior Program Committee (SPC) for the 2017 Uncertainty in AI Conference (UAI), http://www.auai.org/uai2017/. The conference will be held in Sydney, Australia, from August 11th - 15th, 2017.

UAI is the premier international conference on research related to representation, inference, learning and decision making in the presence of uncertainty as they relate to the field of artificial intelligence. As a Senior Program Committee Member for the UAI 2017 conference you will help us select a high quality program for the conference: we count on your help and your expertise. Your main responsibilities will be to help to control the quality of the reviewing process and include:

a) Help us form the Program Committee (PC) by suggesting 5 to 10 potential members.
b) Help us with reviewer assignment by suggesting 3 to 5 reviewers (from the PC) for each paper assigned to you, if you happen to know some good candidates. We expect that you will be assigned around 8 papers.
c) Read the reviews for the papers assigned to you and, if necessary, ask the reviewers to improve their quality.
d) Proactively lead the discussions among reviewers.
e) Write an informative meta-review for each paper assigned to you, and make an accept/reject recommendation.

To ACCEPT the invitation, please click on the following link:

%s

To DECLINE the invitation, please click on the following link:

%s


Before making a decision (we really hope you will accept!), you may want to read through the detailed instructions and timeline below to make sure you are aware of what we expect you to do and the dates when we will need your help. Please verify that you can commit to the deadlines.

1. By January 15th, 2017: Please respond by clicking above indicating whether you accept the SPC invitation or not.

2. If you accept, please log into OpenReview at https://openreview.net and visit your "Tasks" page to provide your areas of subject matter expertise. If you have not yet done so, we also ask that you visit your user profile to provide the domain names of institutions which represent your conflicts of interest. OpenReview is the web-based system we will be using for online submission and reviewing of papers. If you have not used OpenReview before you will need to register: Please use the email address that received this message (you may change your preferred email address after signing up). Even if you have used OpenReview before, please login and check your subject areas.

3. Also by January 15th, 2017: We would very much appreciate if you could send suggestions for potential members for the Program Committee to uai2017chairs@gmail.com. For each candidate, please provide their full name, affiliation, email address, and area of expertise (separated by commas; one candidate per line). If the candidate is a PhD student, please state the year of study. We are particularly interested in finding good reviewers that we may not know about and that were not on the UAI 2016 reviewer list (e.g., junior researchers that are postdocs or above). For reference, the UAI 2016 reviewer list is at http://www.auai.org/uai2016/PC.php. When picking PC members, dependability is as important as qualification.

4. April 1-5, 2017: Enter "bids" into the OpenReview system for submitted papers. Note that "bids" are really just a way for you to indicate which papers you feel you are qualified to review and which ones match your expertise particularly well. It's important that you do this so that you are assigned papers that are a good match to you.

5. April 8-11: Suggest 3 to 5 reviewers for each paper assigned to you and rank them for suitability. Your suggestion will be combined with other information to generate the paper assignment for PC members. We believe that, by utilizing your knowledge of the field, this scheme would improve the match between papers and reviewers.

6. April 15 to May 14th: Review period. You will be able to see (in OpenReview) the papers assigned to you and the list of assigned reviewers. If a reviewer drops out, we might need your help in finding additional reviewers for the paper. When a review is submitted, you should quickly give it a preliminary assessment to identify potential problems as early as possible. If necessary, ask reviewers to edit their reviews to improve quality.

New for 2017:
Reviews will be available for authors as soon as they are submitted, and the authors will be allowed to respond to a review even before the formal rebuttal period.
Reviewers can optionally choose to respond to author's comments or revise their reviews.
Once a review is submitted, it is visible to other reviewers and SPCs who can comment on the review
(this will not be visible to the authors)

7. May 7th to May 14th:
- Chase the missing reviews. This will be followed by author feedback.
- Check reviews and read papers when necessary. If needed, ask reviewers to edit their reviews to improve quality.

8. May 15th to May 31st:
- Initiate and proactively lead discussions among reviewers, especially if there is significant disagreement.
- Request an additional review for a paper if you think it's needed. We will help get the paper to the appropriate reviewer once you let us know about them.

9. By June 1st, write an informative meta-review for each paper. This is especially important for papers that are borderline. Make recommendations as to whether the paper should be rejected, accepted for poster presentation, accepted for oral presentation, or be considered for best paper or best student paper.

10. June 1st - June 11th: The program chairs will make the final paper acceptance decisions based on the reviews. If we need additional input on a particular paper we might contact you, but if the reviews and meta-reviews are of good quality we probably won't need to.

Finally, please note that the conference is slightly later than usual (August 11 - 15), and as a consequence the entire schedule is shifted relative to previous years.

We really hope you will be able to accept our invitation and help us select a high quality program for UAI 2017.  Please reply to this invitation by following the link at the beginning of this message, no later than January 15th, 2017.

Thanks in advance for your help!

Gal Elidan and Kristian Kersting
UAI 2017 Program Chairs
uai2017chairs@gmail.com
"""

def sendMail(spc_invited):
    ## For each candidate reviewer, send an email asking them to confirm or reject the request to review
    for count, spc_member in enumerate(spc_invited):
        hashkey = openreview.get_hash(spc_member.encode('utf-8'), "2810398440804348173")
        url = openreview.baseurl+"/invitation?id=UAI.org/2017/conference/-/spc_invitation&username=" + spc_member + "&key=" + hashkey + "&response="
        fullname = re.sub('[0-9]','',spc_member.replace('~','').replace('_',' '))
        print "Sending message to %s (%s)" % (fullname,spc_member)
        openreview.send_mail("Senior Program Committee Invitation for UAI 2017", [spc_member], message %(fullname,url + "Yes", url + "No"))


if openreview.exists("UAI.org/2017/conference/Senior_Program_Committee/invited") and openreview.exists("UAI.org/2017/conference/Senior_Program_Committee/emailed"):
    reviewers_invited = openreview.get_group("UAI.org/2017/conference/Senior_Program_Committee/invited")
    reviewers_emailed = openreview.get_group("UAI.org/2017/conference/Senior_Program_Committee/emailed")
    print reviewers_invited.members
    recipients = [reviewer for reviewer in reviewers_invited.members if reviewer not in reviewers_emailed.members]
    print recipients
    sendMail(recipients)
    reviewers_emailed.members = reviewers_emailed.members+recipients
    openreview.post_group(reviewers_emailed)
else:
    print "Error while retrieving UAI.org/2017/conference/reviewers-invited; group may not exist"


