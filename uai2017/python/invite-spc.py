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

We would like to invite you to serve as a member of the Senior Program Committee (SPC) for the 2017 Uncertainty in AI Conference (UAI), http://www.auai.org/uai2017/, to be held in the Sydney, Australia, from August 11th - 15th, 2017. UAI is the premier international conference on research related to representation, inference, learning and decision making in the presence of uncertainty as they relate to the field of artificial intelligence.

As a Senior Program Committee Member for the UAI 2017 conference your primary role will be quality control of the reviewing process. Your main responsibilities include:

a) Help us forming the Program Committee (PC) by suggesting 3 to 5 potential members.
b) Help us with reviewer assignment by suggesting 3 to 5 reviewers (from PC) for each paper assigned to you if you happen to know some good candidates. We expect that you will be assigned around 8 papers.
c) Read the reviews for the papers assigned to you and, if necessary, ask the reviewers to improve their quality.
d) Proactively lead the discussions among reviewers.
e) Write an informative meta-review for each paper assigned to you and make an accept/reject recommendation.

To ACCEPT the invitation, please click on the following link:

%s

To DECLINE the invitation, please click on the following link:

%s


You may want to read through the detailed instructions and timeline below, before making a decision, to make sure you are aware of what we expect you to do and the dates when we will need your help.

1. By January 15th, 2017: Please respond by clicking above indicating whether you accept the SPC invitation or not.

2. If you accept, please log into OpenReview at https://openreview.net and visit your "Tasks" page to provide your areas of subject matter expertise. If you have not yet done so, we also ask that you visit your user profile to provide the domain names of institutions which represent your conflicts of interest. OpenReview is the web-based system we will be using for online submission and reviewing of papers. If you have not used OpenReview before you will need to register at https://openreview.net/signup. Even if you have used OpenReview before, please login and check your subject areas.

3. Also by January 15th, 2017: we would very much appreciate you suggesting potential members for the Program Committee that we can invite, and email the information to uai2017chairs@gmail.com. For each candidate, please provide their full name, affiliation, email address, and specialty area of expertise. If the candidate is a PhD student, please state the year of study. We are particularly interested in finding good reviewers that we may not know about and that were not on the UAI 2016 reviewer list (e.g., junior researchers that are postdocs or above). For reference, the UAI 2016 reviewer list is at http://www.auai.org/uai2016/PC.shtml. When picking PC members, dependability is as important as qualification.

4. April 1-6, 2017: Enter "bids" into the OpenReview system for submitted papers. Note that "bids" are really just a way for you to indicate which papers you feel you are qualified to review and which ones match your expertise particularly well. It's important that you do this so that you are assigned papers that are a good match to you.

5. April 7-10: Suggest 3 to 5 reviewers for each paper assigned to you and rank them in suitability if you happen to know some good candidates. Your suggestion will be combined with other information to generate the paper assignment for PC members. We believe that, by utilizing your knowledge of the field, this scheme would improve the match between papers and reviewers.

6. April 15 to May 14th: Review period. You will be able to see (in OpenReview) the papers assigned to you and the list of assigned reviewers. If a reviewer drops out, we might need your help in finding additional reviewers for some papers. When a review is submitted, you should do a quick read to identify potential problems as early as possible. Ask reviewers to edit their reviews to improve quality if necessary.

New for 2017:
Reviews will be available for authors as soon as they are submitted, and the authors will be allow to respond to a review even before the rebuttal period.
Reviewers can optionally choose to respond to author's comments or revise their reviews
Once a review is submitted, it is visible to other reviewers and SPCs who can comment on the review
(not will not be visible to the authors)

7. May 7th to May 14th:
- Chase the missing reviews. This will be followed by author feedback.
- Check reviews and read papers when necessary. Ask reviewers to edit their reviews to improve quality if necessary.

8. May 15th to May 31st:
- Initiate and proactively lead discussions among reviewers, especially if there is significant disagreement.
- Request an additional review for a paper if you think it's needed. We will help get the paper to the appropriate reviewer once you let us know about them.

9. By June 1st, write an informative meta-review for each paper. This is especially important for papers around the borderline. Make recommendations as to whether the paper should be rejected, accepted for poster presentation, accepted for oral presentation, or be considered for best papers.

10. June 1st - June 11th: The program chairs will make the final paper acceptance decisions based on the reviews. If we need additional input on a particular paper we might contact you, but if the reviews and meta-reviews are of good quality we probably won't need to.

Thanks in advance for your help!

Gal Elidan and Kristian Kersting
UAI 2017 Program Chairs
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


