import argparse
import openreview
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm

"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password

"""
request_by_month = {
    'June': 'ppm4ce0nOSy',
    'July': 'DEi06YBuGF5',
    'August': 'oTiQrZFIKsq'
}

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('-v','--month', required=True)

args = parser.parse_args()
baseurl=args.baseurl
input_month = args.month
forum_id=request_by_month[input_month]

client = openreview.Client(baseurl=baseurl, username=args.username, password=args.password)

conf = openreview.helpers.get_conference(client, forum_id)
conf_id = conf.get_id()
print(conf_id)
month = conf_id.split('/')[-1]
print(month)

subject = f'[ARR {month}] Reviews Available'
message = f'''Dear ARR Authors,

We are writing to inform you that your reviews are now available in OpenReview, please log in to your account to view them at the ARR site:
https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/{month}

If you are interested in having your paper submitted for consideration at a publication venue, please fill out the following form (this paper will be updated periodically, and you can fill it in at any point):
https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAANAAZTm0F9URTY1VzhKWlZCTlVJTlU4VUZRVUpGTlpITy4u

Thank you for participating in ARR, and we are looking forward to your submissions in the future.

ARR Editors in Chief
editors@aclrollingreview.org'''

def _get_reviews_for_submission(sub, meta=False):
    """
    Retrieves the reviews for a given submission, where the submission is a Note.
    """
    base_id = conf_id + "/Paper%d" % sub.number
    forum = sub.forum

    if meta:
        inv = base_id + "/-/Meta_Review"
    else:
        inv = base_id + "/-/Official_Review"
    
    return client.get_notes(forum=forum, invitation=inv)

def _enable_review_sharing(sub, meta):
    """
    Enables the sharing of reviews with authors by changing the readers and nonreaders fields.
    """
    base_id = conf_id + "/Paper%d" % sub.number
    authors_id = base_id + "/Authors"
    revs_submitted = base_id + "/Reviewers/Submitted"

    if meta:
        invid = base_id + "/-/Meta_Review"
    else:
        invid = base_id + "/-/Official_Review"

    inv = client.get_invitation(invid)
    if authors_id not in inv.reply["readers"]["values"]:
        inv.reply["readers"]["values"] += [authors_id]

    if meta and "nonreaders" in inv.reply and authors_id in inv.reply["nonreaders"]:
        inv.reply["nonreaders"].remove(authors_id)
    elif not meta and authors_id in inv.reply["nonreaders"]["values"]:
        inv.reply["nonreaders"]["values"].remove(authors_id)

    client.post_invitation(inv)

def get_submissions_with_finished_reviews(min_num_reviews = -1):
    """
    Gets the submissions with finished reviews and meta-reviews.
    """
    # conf is the conference object
    sub_notes = conf.get_submissions()
    print('All Papers:', len(sub_notes))

    result = []
    for sn in sub_notes:
        # get ids
        forum = sn.forum

        base_id = conf_id + "/Paper%d" % sn.number
        rev_id = base_id + "/Reviewers"
        ac_id = base_id + "/Area_Chairs"

        # number of reviewers and ACs
        if min_num_reviews < 0:
            num_reviewers = len(client.get_group(rev_id).members)
            thresh = num_reviewers
        else:
            thresh = min_num_reviews

        # number of submitted reviews (and meta-reviews)
        reviews = _get_reviews_for_submission(sn)
        num_reviews = len(reviews)

        if num_reviews < thresh:
            continue

        # todo could do it with less requests in a single batch and then filtering, but for now...
        num_acs = len(client.get_group(ac_id).members)

        mreviews = _get_reviews_for_submission(sn, meta=True)
        num_mreviews = len(mreviews)

        if num_mreviews < 1:
            continue

        result += [sn]

    return result

def share_reviews_with_authors(sub):
    """
    Shares the reviews and meta-review for a given submission with the respective authors.
    """
    count=0
    revs = _get_reviews_for_submission(sub)
    mrevs = _get_reviews_for_submission(sub, meta=True)

    base_id = conf_id + "/Paper%d" % sub.number
    authors_id = base_id + "/Authors"

    # allow shared reviews
    _enable_review_sharing(sub, False)
    _enable_review_sharing(sub, True)

    for r in revs + mrevs:
        changed = False
        if authors_id in r.nonreaders:
            r.nonreaders.remove(authors_id)
            changed = True
        if authors_id not in r.readers:
            r.readers += [authors_id]
            changed = True

        if changed:
            count+=1
            client.post_note(r)

    if changed:
        client.post_message(subject = subject, recipients = [authors_id], message = message)

all_papers = client.get_notes(invitation=conf_id+'/-/Blind_Submission')
submissions = get_submissions_with_finished_reviews(min_num_reviews = 3)

paper_ids = []
for paper in submissions:
    paper_ids.append(paper.forum)

for submission in tqdm(submissions):
    share_reviews_with_authors(submission)

file_name = 'ARR-{}-data.csv'.format(month)
print('File name:', file_name)

with open(file_name, 'w') as f:
    row = ['Paper number','Paper Id','Paper link', 'Reviews released?']
    f.write(','.join(row) + '\n')
    for paper in all_papers:
        if paper.id in paper_ids:
            row = []
            row.append(str(paper.number))
            row.append(paper.forum)
            link = "https://openreview.net/forum?id={}".format(paper.forum)
            row.append(link)
            row.append('Yes')
        else:
            row = []
            row.append(str(paper.number))
            row.append(paper.forum)
            link = "https://openreview.net/forum?id={}".format(paper.forum)
            row.append(link)
            row.append('No')
        f.write(','.join(row) + '\n')