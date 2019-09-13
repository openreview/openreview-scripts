import openreview
import argparse
import re

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = openreview.helpers.get_conference(client, 'SkxpQPWdA4')

    title = '[ICLR 2020]: Invitation to Review'
    message = '''Dear {name},

Please accept our invitation to serve as a Reviewer for ICLR2020, which will be held in April 2020 in Addis Ababa, Ethiopia. See call for papers at: www.iclr.cc. ICLR has grown immensely, and the quality of the conference relies heavily on the quality of the reviews. As a recognized researcher, we highly value your input and hope you can contribute to the review process of ICLR 2020. We are planning for a load of at most 6 papers, so the commitment should not be too onerous.

Here are the key dates that we expect to work towards for ICLR2020:
Paper submissions close: Wednesday, 25 September 2019
Review period opens: Thursday, 3 October 2019
Reviewing period ends: Friday, 18 October 2019
Release Reviews: Monday, 4 November 2019
Discussion period starts: Monday, 4 November 2019
Discussion period ends: Friday, 22 November 2019
Notifications on Thursday, 19 December 2019.

The review process will be similar to last year. There will be three weeks to review and three weeks for discussion. We will be using OpenReview throughout the review process. The submissions are double-blind, and only your public review will be visible to everyone -- not your name nor any private discussion about the paper. We will provide Reviewer Guidelines, to support you in writing your reviews.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

We would appreciate an answer as soon as possible.

If you have not already signed up on openreview.net, please do so. Also, make sure to add the address you received this email on to your OpenReview profile.

If you have any questions, please don’t hesitate to reach out to us at iclr2020programchairs@googlegroups.com .

Thank you as always for your ongoing service to our community, and we look forward to working with you to make this the best ICLR yet.

ICLR2020 Programme Chairs,
Shakir Mohamed, Dawn Song, Kyungyhun Cho, Martha White
'''

    # suggested_group = client.get_group('ICLR.cc/2020/Conference/Reviewers/Suggested')
    # suggested_members = suggested_group.members
    # new_member_list = []
    # removal_list = []
    # pattern = re.compile("^~.*[0-9]+$")
    # for index, member in enumerate(suggested_members):
    #     invited_reviewers_groups = client.get_groups(member = member, regex = 'ICLR.cc/2020/Conference/Reviewers/Invited')
    #     ac_groups = client.get_groups(member = member, regex = 'ICLR.cc/2020/Conference/Area_Chairs')
    #     if member.startswith("~"):
    #         if pattern.match(member):
    #             if len(invited_reviewers_groups) == 0 and len(ac_groups) == 0:
    #                 new_member_list.append(member)
    #                 print(index, '+', member)
    #             else:
    #                 print(index, '.')
    #         else:
    #             print (index, '-', member)
    #             removal_list.append(member)
    #     else:
    #         if '@' in member and len(invited_reviewers_groups) == 0 and len(ac_groups) == 0:
    #             new_member_list.append(member)
    #             print(index, '+', member)
    #         else:
    #             print(index, '.')

    # print (len(new_member_list), " :: ", new_member_list)
    # print (len(removal_list), " :: ", removal_list)

    # conference.recruit_reviewers(emails = new_member_list, title = title , message = message)

    conference.recruit_reviewers(remind=True, title = title , message = message)
