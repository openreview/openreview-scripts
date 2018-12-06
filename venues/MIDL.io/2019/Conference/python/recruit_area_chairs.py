import sys, os
import argparse
import openreview
import config

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print('connecting to {0}'.format(client.baseurl))

conference = config.get_conference(client)

formatted_acs = []

title = 'MIDL 2019 Conference: Invitation to Review'
message = '''
Thank you for accepting our invitation to be an Area Chair for the Medical Imaging with Deep Learning Conference. With this email, we are inviting you to log on to the OpenReview system for MIDL 2019 and provide you the guidelines for acting as an AC in MIDL.

To ACCEPT the invitation, please click on the following link:

{accept_url}

If you changed your mind please DECLINE the invitation by clicking on the following link:

{decline_url}

We’d appreciate an answer within five days. If you have any questions please contact MIDL Program Chairs at <program-chairs@midl.io>.

We are looking forward to your reply.

MIDL Program Chairs
Ipek Oguz
Gozde Unal
Ender Konukoglu


Guidelines:

For MIDL 2019, the review process and the responsibilities of the Area Chairs (AC) during the review period are summarised as follows:

1. Each AC will propose and add 5-6 reviewers/delegates whom they trust to deliver "high quality" and "in time" feedback/review and who were not already proposed by other ACs, into the OpenReview system. Note that this means it will be easier to identify unique reviewers for the early responding AC’s. This should be completed by December 1st, 2018. All reviewers should sign up to the system before the full paper submission deadline of December 13, 2018.

2. After the full paper submission deadline has passed, a certain number of (we estimate about 10, but may vary depending on the number of total submissions to MIDL this year) will be assigned to each AC.

3. Each AC will delegate each of their assigned papers to 3 reviewers. Hence, we estimate that each AC will be responsible to collect roughly 10x3=30 reviews in total, which will be distributed to about 5-6 reviewers. The ACs are not restricted to use only their proposed reviewers. They can select from the pool constructed by all ACs. This flexibility will allow choosing an appropriate reviewer for each article.

4. The system will send periodic review reminders to the ACs and the reviewers. In addition, ACs will be responsible to remind their reviewers to complete their reviews in time, which has the deadline of January 28th, 2019.

5. During the review period, each AC is expected to read and be able to give a score/opinion on their assigned papers (about 10 papers).

6. It is important that each paper receives 3 reviews from the reviewers. In case  there are missing reviews (we hope this number will be minimal this year), the Area Chairs, by informing/help of the Program Chairs, will select last-minute reviewers, each of whom should be able to complete 1-2 reviews in at most 2-3 days. Last minute reviews can be handled by other ACs.

7. The official reviews (i.e. the 3 reviews ) for each paper will be posted publicly and anonymously after all three reviews for each paper are collected. The reviewers will have the option of de-anonymizing their reviews to be posted after the decisions are announced. At this point, the OpenReview system will also be open to receiving public posts/comments, however, those will not be made public until the decisions are announced. They will not be visible to Area Chairs and the Program Chairs, however they will be visible to the Authors during the whole process.

8. The authors will be able to address feedback of the official reviewers in by responding to reviewer comments on the OpenReview system and make changes to the paper, if they would like to. The rebuttal and discussion period will be from January 28, 2019 until February 04, 2019. The author responses will be publicly visible at the OpenReview system.

9. After the rebuttal process ends, each AC will evaluate the 3 received reviews/scores and responses/rebuttal for each of their papers. They will submit  a score and a tentative recommendation for all the papers in their pool. The deadline for AC recommendation upload to the system is February 13, 2019. ACs will have the chance to override the majority voting decision from the reviewers, in special certain cases where they believe that the comments of the reviewers do not match the quantitative scores given to a paper. In that case, AC should provide a justification for their recommendation. We again do not expect that this will happen much or even at all due to the "carefully" constructed reviewer pool.

10. The program chairs will collect all the AC recommendations and will do a final check on the consistency of the reviewer scores + AC scores + AC recommendations. The final decisions will be announced on February 20th, 2019.

In summary, finally, the Program chairs will go through the 4 scores (3 Reviewers + 1 AC review + AC recommendation) to detect any major inconsistencies, if any. In most cases, AC recommendation will be the base resulting decision, however, we will check outlier cases, where for instance 3 reviewers return with negative results and the AC returns with a positive decision and such.

'''

conference.recruit_reviewers(emails = formatted_acs, title = title, message = message, reviewers_name = 'Area_Chairs')
