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

    title = 'ECCV 2020 Reviewer Invitation'
    message = '''Dear {name},

Due to your scientific profile and expertise, we invite you to serve as a reviewer for ECCV 2020 (https://eccv2020.eu/). The quality of our conference depends on the willingness of reviewers like you to provide thoughtful, high-quality reviews. We hope you can join us and make ECCV 2020 a success.

This time we offer two bonuses to reviewers:
We will have a substantial number of *outstanding reviewer awards*. These will be based on the accumulated review quality ratings by the ACs. All outstanding reviewers will receive *free registration* to ECCV 2020.
Furthermore, all reviewers in good standing (meeting all deadlines and submitting reviews of acceptable quality according to the ACs) will be *guaranteed the possibility of registering* to the conference for a certain period of time.

By accepting this invitation you accept to review a maximum of 7 papers by the deadline below. This is a conservative number for the case that ECCV will receive far more submissions than expected. Most likely, the maximum will be reduced to 5 papers for all.

Based on the reviews, authors will be able to submit rebuttals to address the reviewer's comments. A discussion among reviewers will follow, moderated by the responsible area chair. Then you must make your final recommendation for each paper.

The schedule is as follows:
Jan 30:          Finish updating your profile on OpenReview
March 5:         Paper submission deadline
March 6-15:      Reviewers bid for papers
Apr 3 - May 10:  Reviewing period
*May 10:          Reviews due*
May 28 - June 7: Discussion period and final recommended due
*June 7:          Final recommendation due*
July 3:          Decisions to authors

We will use OpenReview as a submission and reviewing portal, but the review process will remain the same as for prior ECCVs. In particular, the reviews will be double blind and not open to the public.

You find reviewer instructions and FAQs here:
https://docs.google.com/document/d/1ifx0sIOnCQ2lCjBxy6IQun4xjZlSNyozTQexcMzcN9o/edit?usp=sharing

On behalf of the computer vision community, we count on your expertise and hope you will accept this invitation. If you got multiple invitations, please use the one sent to your most recent email address and ignore the others.

Click the link below to accept.
{accept_url}

Click the link below to decline.
{decline_url}

This invitation expires on Dec 3.

Thank you,
Horst Bischof, Thomas Brox, Jan-Michael Frahm, Andrea Vedaldi
ECCV 2020 Program Chairs
'''

    names_list = []
    emails_list = []

    with open('reviewer_details.csv', 'r') as f:
        all_text = f.read()
        for s in all_text.split('\n'):
            *full_name, email, tilde = [element.strip() for element in s.split(',')]
            names_list.append(' '.join([name for name in full_name]))
            if tilde.startswith('~'):
                emails_list.append(tilde)
            else:
                emails_list.append(email.lower())

    conference.set_recruitment_reduced_load(['4','5','6','7'])

    conference.recruit_reviewers(emails= emails_list, title = title , message = message, invitee_names = names_list)