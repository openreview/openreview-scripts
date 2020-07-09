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

    conference = openreview.get_conference(client, 'tEEXdrgkqm')

    title = 'Reviewer invitation for ICLR 2021 -- please respond by July 16th'
    message = '''
Summary: We would be delighted if you would agree to serve as a reviewer for the 2021 International Conference on Learning Representations (ICLR2021).

Dear {name},

Please accept our invitation to serve as a Reviewer for ICLR2021, which will be held from May 4th to May 8th, 2021. We are hoping to meet in Vienna, Austria, but we are also preparing for a virtual/hybrid conference, in case an in-person conference is not advisable at the time. In either case, we will put public health and safety first. See the call for papers at https://iclr.cc/Conferences/2021/CallForPapers for further details.

ICLR continues to grow rapidly and, to ensure a high-quality programme, we rely on the expertise of recognized researchers such as yourself. For this reason, we highly value your input and hope you can contribute to the review process of ICLR 2021. We expect a load of 3-6 papers, so the commitment should not be onerous. 

Here are the key dates, focused on reviewer duties, that we expect to work towards for ICLR2021: 
- Bidding period starts: Monday, 5 October 2020
- Bidding period ends: Thursday, 9 October 2020
- Review period starts: Monday, 12 October 2020
- Reviewing period ends: Wednesday, 28 October 2020
- Release Reviews: Tuesday, 10 November 2020
- Discussion period starts: Tuesday, 17 November 2020
- Discussion period ends: Tuesday, 24 November 2020

The review process will be similar to last year. In particular, we will be using OpenReview throughout the review process. The submissions are double-blind, and only your public review will be visible to everyone -- neither your name nor any private discussion about the paper. We have provided reviewer instructions (https://iclr.cc/Conferences/2021/ReviewerGuide) to support you in writing your reviews. Reviewers are also required to adhere to the ICLR code of conduct (https://iclr.cc/public/CodeOfConduct). More detailed guidance will be made available in due course, and participation will require acknowledging and adhering to the provided guidelines.

If you accept this invitation, it is important that you are available and responsive during the entire reviewing process. Reviewers are expected to provide high-quality reviews, to consider author feedback, and to actively participate in discussions.

We appreciate that serving as a reviewer for ICLR is time-consuming. As a token of our appreciation, we will provide free registration for top reviewers. We will also publicly acknowledge all reviewers on our website and highlight our top reviewers.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

We would appreciate an answer by July 16th (in 7 days).

If you have any questions, please don’t hesitate to reach out to us at iclr2021programchairs@googlegroups.com.

Thank you as always for your ongoing service to our community, and we look forward to working with you to make this the best ICLR yet.

ICLR2021 Programme Chairs,
Naila Murray, Katja Hofmann, Alice Oh, and Ivan Titov 

'''

    names_list = []
    emails_list = []

    with open('ICLR_2021_invited_reviewers_wave1_final.tsv', 'r') as f:
        content = f.read().split('\n')
        for line in content[1:]:
            if line:
                elements = line.split('\t')
                names_list.append(' '.join([n.strip() for n in elements[2:5] if n.strip()]))
                emails_list.append(elements[5].strip().lower())

    conference.recruit_reviewers(
        title=title,
        invitees=emails_list,
        invitee_names=names_list,
        reviewers_name='Reviewers'
    )
