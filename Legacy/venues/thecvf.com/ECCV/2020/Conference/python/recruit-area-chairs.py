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

    conference = openreview.helpers.get_conference(client, 'Skx6tVahYB')

    title = 'ECCV 2020 Area Chair Invitation'
    message = '''Dear {name},

We would like to invite you to serve as an Area Chair (AC) for ECCV 2020, which will be held in Glasgow during August 2020. The quality of the conference is in the hands of the ACs, and we hope you can be one of them.
Area Chairs ensure that the conference is interesting, diverse, and scientifically solid.

In doing so an Area Chair will:
- overlook a set of 20-30 papers;
- identify possible Reviewers for those papers;
- ensure that submitted reviews are consistent, possibly contacting Reviewers in order to improve their evaluation;
- encourage discussion among Reviewers for papers where the decision is uncertain;
- discuss a lager set of papers (~2x the original set) with other Area Chairs to make a final recommendation;
- write a short summary (meta review) explaining the final recommendation.

This year we will be using the OpenReview software, but the review process remains essentially unchanged form the past editions of ECCV (e.g. reviews, discussions, etc. will not be public).

Below is a tentative schedule. Please check your calendar if you are available in these time windows and only accept if you can meet all deadlines.

Until November 30, 2019: ACs update their profile in OpenReview
March 5, 2020: Paper submission deadline
March 6 - 12: ACs enter their bids for a preselected set of papers
March 16 - 24: ACs suggest reviewers for each paper
May 10 - 13: ACs chase missing reviews
May 14 - 20: ACs coordinate emergency reviews
May 21 - 27: Rebuttal period
May 28 - June 7: ACs coordinate reviewer discussion, decide clear reject cases, write preliminary meta-review
June 8 - 21: Discussion with other ACs on a superset of papers
June 21: Decisions and meta-reviews due

This information as well as specific instructions for each step will be added to the Google Doc link
https://docs.google.com/document/d/1lStXLu0Fuqxjw0Ag2NPTOZtztNT_PGXIYRoVexSe2FE/edit?usp=sharing
The document will be updated with new details as they become available.

There will not be a physical AC meeting. We are planning free registration for all ACs who handle all their papers properly and in time. Moreover, ACs will be invited to an invitation-only event (lunch/dinner) during the conference.

Click this link to accept:
{accept_url}

Click this link to decline:
{decline_url}

The invitation expires on November 6, 2019.

Thank you and best regards,
Horst Bischof, Thomas Brox, Jan-Michael Frahm, Andrea Vedaldi
ECCV 2020 Program Chairs'''

    names_list = []
    emails_list = []
    name_email_text = ''''''

    for s in name_email_text.split('\n'):
        *full_name, email = [element.strip() for element in s.split(';')]
        names_list.append(' '.join([name for name in full_name]))
        emails_list.append(email.lower())

    conference.recruit_reviewers(emails= emails_list, reviewers_name = 'Area_Chairs', title = title , message = message, invitee_names = names_list)