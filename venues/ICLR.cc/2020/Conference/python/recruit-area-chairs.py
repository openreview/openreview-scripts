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

    conference = openreview.helpers.get_conference(client, 'SkxpQPWdA4')

    title = '[ICLR2020]: Invitation to serve as an Area Chair'
    message = '''
TL;DR: We would be honoured if you would agree to serve as an Area Chair for the 2020 International Conference on Learning Representations (ICLR2020). Please accept by clicking {accept_url} .

Dear {name},

Please accept our invitation to serve as an area chair for ICLR2020, which will be held in April 2020 in Addis Ababa, Ethiopia.

Areas Chairs at ICLR serve many roles: you guide the reviewing process to enable a rigorous and respectful review process for submitted papers; you are the principal decision maker in the final status of papers; and you are also an action editor of the conference proceedings, which is one of its key outputs. We believe that your experience makes you ideal to serve as an AC and take on these roles. We hope you will accept.

Here are the key dates that we expect to work towards for ICLR2020:
Paper submissions close: Wednesday, 25 September 2019
Review period opens: Thursday, 3 October 2019
Reviewing period ends: Friday, 18 October 2019
Substitute reviewing period starts: Monday, 21 October 2019
Substitute reviewing period ends: Friday, 1 November 2019
Release Reviews: Monday, 4 November 2019
Discussion period starts: Monday, 4 November 2019
Discussion period ends: Friday, 22 November 2019
PC/AC Calibrations ends: Friday, 12 December 2019

The entire process should take around 3 months to complete.
At the initial assignment phase, we will ask you to look through your papers to alert the programme chairs of any papers that don’t meet the submission criteria and to check with your reviewers that their assignments are appropriate.
Because there are always late reviewers and some that can’t contribute in the end, we have an explicit period in which substitute reviewers will need to be found and assigned (this period is not communicated to reviewers).
Most of the AC work is in the month of November where the discussion and clarification on papers’ claims and contributions are held. For borderline cases, we will reach out to ask with help in calibrating reviews in December (in the week after NeurIPS).

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in.

If there are any other questions, please don’t hesitate to reach out to us at iclr2020programchairs@googlegroups.com.

Thank you as always for your ongoing service to our community, and we look forward to working with you to make this the best ICLR yet.

ICLR2020 Programme Chairs,
Shakir Mohamed, Dawn Song, Kyungyhun Cho, Martha White
    '''

    # details = ''''''

    # emails = []
    # names = []
    # for detail in details.split('\n'):
    #     name, email = [i.strip() for i in detail.split(',')]
    #     emails.append(email)
    #     names.append(name)

    # conference.recruit_reviewers(emails= emails, reviewers_name = 'Area_Chairs', title = title , message = message, invitee_names = names)

    conference.recruit_reviewers(reviewers_name = 'Area_Chairs', title = title , message = message, remind = True)