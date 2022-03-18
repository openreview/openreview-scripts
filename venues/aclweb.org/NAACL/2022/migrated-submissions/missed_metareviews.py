import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv
import tracks

"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password

"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

papers_missing_metas = [826,393,334,306,275,175,53,37,36,10]

for number in papers_missing_metas: 
    blind_submission = client.get_notes(invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission', number = number)[0]
    example_review = client.get_notes('aclweb.org/NAACL/2022/Conference/-/ARR_Official_Review', forum = blind_submission.forum)[0]
    original_submission_forum = blind_submission.content['paper_link'].split('=')[1]
    original_submission = client.get_note(original_submission_forum)


    conf_id = original_submission.invitation.rsplit('/', 2)[0]
    metareview_invitation_arr = '{conf_id}/Paper{number}/-/Meta_Review'.format(conf_id = conf_id,number = original_submission.number)

    # Get all reviews from the original ARR Submission
    arr_metareviews = list(openreview.tools.iterget_notes(client, invitation = metareview_invitation_arr))

    # Iterate through each review and for each, create and post a new review
    for arr_metareview in arr_metareviews:
        acl_metareview = openreview.Note(
            forum = blind_submission.forum,
            replyto = blind_submission.forum,
            invitation = f'aclweb.org/NAACL/2022/Conference/-/ARR_Meta_Review',
            signatures = arr_metareview.signatures,
            readers = example_review.readers,
            nonreaders=example_review.nonreaders,
            writers = [
                'aclweb.org/NAACL/2022/Conference'
            ],
            content = arr_metareview.content
        )
        acl_metareview.content['link_to_original_metareview'] = f'https://openreview.net/forum?id={arr_metareview.forum}&noteId={arr_metareview.id}'
        acl_metareview.content['title'] = f'Meta Review of Paper{original_submission.number} by {arr_metareview.invitation.split("/")[4]} Area Chair'
        profile = client.get_profile(arr_metareview.tauthor)
        acl_metareview.content['action_editor_id'] = f"{profile.id}"
        acl_metareview_posted = client.post_note(acl_metareview)
        assert acl_metareview_posted, print('failed to post metareview ', acl_metareview.id)
        


