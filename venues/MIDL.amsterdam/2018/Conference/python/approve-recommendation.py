## Import statements
import argparse
import csv
import config
import openreview
from openreview import tools
from collections import defaultdict

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print "connecting to ", client.baseurl

recommend_reviewer_notes = client.get_notes(
    invitation = 'MIDL.amsterdam/2018/Conference/Paper.*/-/Recommend_Reviewer')

recs_by_papernum = defaultdict(list)
for rec in recommend_reviewer_notes:
    splits = rec.invitation.split('/')
    papernum = int(splits[3].split('Paper')[-1])
    recs_by_papernum[papernum].append(rec)

reviewer_invitation_notes = client.get_notes(
    invitation = 'MIDL.amsterdam/2018/Conference/-/Paper.*/Reviewer_Invitation')

responses_by_papernum = defaultdict(list)
for response in reviewer_invitation_notes:
    splits = response.invitation.split('/')
    papernum = int(splits[4].split('Paper')[-1])
    responses_by_papernum[papernum].append(response)

reviewer_groups = client.get_groups('MIDL.amsterdam/2018/Conference/Paper.*/Reviewers')
anonreviewer_groups = client.get_groups('MIDL.amsterdam/2018/Conference/Paper.*/AnonReviewer.*')

revgroups_by_papernum = defaultdict()
anongroups_by_papernum = defaultdict(list)
for group in reviewer_groups:
    splits = group.id.split('/')
    groupnum = int(splits[3].split('Paper')[-1])
    revgroups_by_papernum[groupnum] = group

for group in anonreviewer_groups:
    splits = group.id.split('/')
    groupnum = int(splits[3].split('Paper')[-1])
    anongroups_by_papernum[groupnum].append(group)

papers = client.get_notes(invitation='MIDL.amsterdam/2018/Conference/-/Submission')
papers_by_papernum = {p.number: p for p in papers}

replacement_by_number = defaultdict(list)
unfilled_by_number = defaultdict(list)

for number, response_list in responses_by_papernum.iteritems():
    recs = recs_by_papernum.get(number)
    recommender_by_recommended = {rec.content['email']: rec.signatures[0] for rec in recs}

    for response in response_list:
        email = response.content.get('email', None)
        recommender = None
        if not email:
            print number, response.id, response.content
        else:
            new_reviewer_identities = client.get_groups(member=email)
            for rev in new_reviewer_identities:
                if rev.id in recommender_by_recommended:
                    recommender = recommender_by_recommended[rev.id]

        if response.content['response'] == 'Yes' and recommender and email:
            replacement_by_number[number].append((recommender, email))

reviewer_subject = '[MIDL 2018] You have been assigned to Paper {}'
reviewer_message = '''Dear Reviewer,

Thank you for accepting the invitation to review for MIDL 2018.

Your review assignment can be found here:

https://openreview.net/forum?id={}

Please email the MIDL program chairs for policy questions, and info@openreview.net with technical issues.

Best,
The OpenReview Team

'''

recommender_subject = '[MIDL 2018] You have been un-assigned from Paper {}'
recommender_message = '''Dear Reviewer,

Based on your recommendation, we have unassigned you as a reviewer from Paper {number}, and assigned {new_rev}.

For your reference, the paper can be found here:

https://openreview.net/forum?id={forum}

At this point, you should *not* be assigned as a reviewer to this paper.

Please email the MIDL program chairs for policy questions, and info@openreview.net with technical issues.

Best,
The OpenReview Team

'''


for num, repl_list in replacement_by_number.iteritems():
    paper = papers_by_papernum[num]
    for recommender, new_reviewer in repl_list:
        anongroups = client.get_groups('MIDL.amsterdam/2018/Conference/Paper{}/AnonReviewer.*'.format(num))
        revgroup = client.get_group('MIDL.amsterdam/2018/Conference/Paper{}/Reviewers'.format(num))
        new_reviewer_identities = client.get_groups(member=new_reviewer)
        if not any([g.id in a.id for g in new_reviewer_identities for a in anongroups]):
            tools.assign(
                client,
                num,
                'MIDL.amsterdam/2018/Conference',
                reviewer_to_remove = recommender,
                reviewer_to_add = new_reviewer
            )

            reviewer_response = client.send_mail(
                reviewer_subject.format(paper.number),
                [new_reviewer],
                reviewer_message.format(paper.forum)
            )

            recommender_response = client.send_mail(
                recommender_subject.format(paper.number),
                [recommender],
                recommender_message.format(number=paper.number, new_rev=new_reviewer, forum=paper.forum)
            )
            print reviewer_response, recommender_response
        else:
            print "{} already done: {} --> {}".format(paper.number, recommender, new_reviewer)
