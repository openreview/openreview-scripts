import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv

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
parser.add_argument('--confid')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
confid = args.confid

# Post acl submission (calls post_blind_submission)
def post_acl_submission(arr_submission_forum, acl_commitment_note, submission_output_dict):
    # Depends on the workshop
    eligible_arr_invitations = ['aclweb.org/ACL/ARR/2021/May/', 'aclweb.org/ACL/ARR/2021/Jun/', 'aclweb.org/ACL/ARR/2021/July/', 'aclweb.org/ACL/ARR/2021/August/', 'aclweb.org/ACL/ARR/2021/September/','aclweb.org/ACL/ARR/2021/October/','aclweb.org/ACL/ARR/2021/November/', 'aclweb.org/ACL/ARR/2021/December/', 'aclweb.org/ACL/ARR/2022/January/' ,'aclweb.org/ACL/ARR/2022/February/']
    original_arr_sub_id = None
    #submission_output_dict['acl_commitment_forum'] = acl_commitment_note.forum
    try:
        original_arr_sub = client.get_note(arr_submission_forum)
        if(original_arr_sub.original):
            original_arr_sub_id = original_arr_sub.original
        else:
            original_arr_sub_id = original_arr_sub.id
    except:
        print(f"Note {arr_submission_forum} does not exist")
    if original_arr_sub_id and ((client.get_note(original_arr_sub_id)).invitation.startswith(tuple(eligible_arr_invitations))):
        #print(original_arr_sub_id)
        original_arr_sub = client.get_note(original_arr_sub_id)
        submission_output_dict[acl_commitment_note.forum]['arr_submission_forum'] = original_arr_sub.forum
        if (openreview.tools.get_profiles(client,[acl_commitment_note.signatures[0]])[0].id) in [profile.id for profile in openreview.tools.get_profiles(client, original_arr_sub.content['authorids'])]:
            # Create new note to submit to ACL
            content = {}
            conf_submission_invitation = client.get_invitation(f"{confid}/-/Migrated_Submission")
            for key in acl_commitment_note.content.keys():
                content[key] = acl_commitment_note.content[key]
            for key in original_arr_sub.content.keys():
                if key in conf_submission_invitation.reply['content']:
                    content[key] = original_arr_sub.content[key]
            content['paper_link'] =f'https://openreview.net/forum?id={arr_submission_forum}'
            content['commitment_note'] = f"https://openreview.net/forum?id={acl_commitment_note.forum}"
            acl_sub = openreview.Note(
                invitation=f"{confid}/-/Migrated_Submission",
                readers = [
                    confid
                    ],
                writers = [
                    confid
                    ],
                signatures = [
                    confid
                    ],
                content = content
            )
            acl_submitted = client.post_note(acl_sub)
            if(acl_submitted):
                submission_output_dict[acl_commitment_note.forum]['was_migrated'] = True
                acl_submission_dict[acl_submitted.content['paper_link'].split('=')[1]]=acl_submitted
                post_blind_submission(acl_submitted.id, acl_submitted, original_arr_sub, submission_output_dict, acl_commitment_note)
            else:
                print(f'Nothing posted for ARR Submission {arr_submission_forum}')
                return(submission_output_dict)
        else:
            print(f"signature of acl commitment note {acl_commitment_note.id} not in arr submission {arr_submission_forum} authors")
            return submission_output_dict
    else:
        print(f"acl commitment note {acl_commitment_note.id} links to arr submission {arr_submission_forum} with invalid invitation")
        return submission_output_dict




# Post blind submission (calls post_reviews)
def post_blind_submission(acl_submission_id, acl_submission, arr_submission, submission_output_dict, acl_commitment_note):
    # Post requisite groups
    number = acl_submission.number
    # Create PaperX group
    paper_group = openreview.Group(
        id = f'{confid}/Commitment{acl_commitment_note.number}',
        signatures = [
            confid
            ],
        signatories = [
            confid
            ],
        readers = [
            confid
            #'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
            ],
        writers = [
            confid
            ]
    )
    client.post_group(paper_group)

    # Create paperX/Authors
    authors = openreview.Group(
        id = f'{confid}/Commitment{acl_commitment_note.number}/Authors',
        signatures = [
            confid
            ],
        signatories = [
            confid,
            f'{confid}/Commitment{acl_commitment_note.number}/Authors'
            #'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
            ],
        readers = [
            confid,
            f'{confid}/Commitment{acl_commitment_note.number}/Authors'
            #'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
            ],
        writers = [
            confid
            ],
        members = acl_submission.content['authorids']
    )

    authors_posted = client.post_group(authors)
    assert authors_posted, print('Failed to post author groups: ', acl_submission_id)



    # Create paperX/Conflicts
    conf_id = arr_submission.invitation.rsplit('/', 2)[0]
    arr_number = arr_submission.number
    conflict_members = [
            '{conf_id}/Paper{number}/Reviewers'.format(conf_id = conf_id, number = arr_number),
            '{conf_id}/Paper{number}/Area_Chairs'.format(conf_id = conf_id, number = arr_number),
            '{conf_id}/Paper{number}/Authors'.format(conf_id = conf_id, number = arr_number)
            ]
    # Find all previous & future submissions and for each one add the reviewers and ACs to the conflict group
    def get_reviewer_AC_conflicts(current_submission):
        previous_url = current_submission.content.get('previous_URL')
        if previous_url and ("openreview.net" in previous_url):
            #print(current_submission.forum)
            previous_forum = (current_submission.content.get('previous_URL').split('=')[1]).split('&')[0]
            previous_submission = client.get_note(previous_forum)
            conf_id = previous_submission.invitation.rsplit('/', 2)[0]
            arr_number = previous_submission.number
            reviewers = '{conf_id}/Paper{number}/Reviewers'.format(conf_id = conf_id, number = arr_number)
            area_chairs = '{conf_id}/Paper{number}/Area_Chairs'.format(conf_id = conf_id, number = arr_number)
            conflict_members.append(reviewers)
            conflict_members.append(area_chairs)
            if (previous_submission.forum != current_submission.forum) and (previous_submission.forum != current_submission.id):
                get_reviewer_AC_conflicts(previous_submission)

    get_reviewer_AC_conflicts(arr_submission)
    later_versions = submission_output_dict[acl_commitment_note.forum]['later_versions?']
    if later_versions:
        for version in later_versions:
            later_submission = client.get_note(version)
            arr_conf_id = later_submission.invitation.rsplit('/', 2)[0]
            arr_number = later_submission.number
            reviewers = '{conf_id}/Paper{number}/Reviewers'.format(arr_conf_id = arr_conf_id, number = arr_number)
            area_chairs = '{conf_id}/Paper{number}/Area_Chairs'.format(arr_conf_id = arr_conf_id, number = arr_number)
            conflict_members.append(reviewers)
            conflict_members.append(area_chairs)

    conflicts = openreview.Group(
        id = f'{confid}/Commitment{acl_commitment_note.number}/Conflicts',
        signatures = [
            confid
            ],
        signatories = [
            confid
            ],
        readers = [
            confid
            ],
        writers = [
            confid
            ],
        members = conflict_members
    )
    conflicts_posted = client.post_group(conflicts)
    assert conflicts_posted, print('Failed to post conflict group: ', acl_submission_id)

    # post blinded note
    blinded_note = openreview.Note(
            invitation = f"{confid}/-/Migrated_Blind_Submission",
            original = acl_submission_id,
            readers = [
                f"{confid}/Program_Chairs",
                confid
                #"aclweb.org/ACL/2022/Conference/{sac_track}/Senior_Area_Chairs".format(sac_track = sac_name_dictionary[acl_submission.content['track']])
                ],
            nonreaders = [
                f"{confid}/Commitment{acl_commitment_note.number}/Conflicts"
                ],
            writers = [
                confid
                ],
            signatures = [
                confid
                ],
            content = {
                "authorids" : [f"{confid}/Commitment{acl_commitment_note.number}/Authors"],
                "authors":["Anonymous"]
            }
        )
    blinded_commitment_note = openreview.Note(
            invitation = f"{confid}/-/Blind_Commitment_Submission",
            original = acl_commitment_note.id,
            readers = [
                f"{confid}/Program_Chairs",
                f"{confid}/Commitment{acl_commitment_note.number}/Authors",
                confid
                #"aclweb.org/ACL/2022/Conference/{sac_track}/Senior_Area_Chairs".format(sac_track = sac_name_dictionary[acl_submission.content['track']])
                ],
            nonreaders = [
                f"{confid}/Commitment{acl_commitment_note.number}/Conflicts"
                ],
            writers = [
                confid
                ],
            signatures = [
                confid
                ],
            content = {
                "authorids" : [f"{confid}/Commitment{acl_commitment_note.number}/Authors"],
                "authors":["Anonymous"]
            }
        )
    client.post_note(blinded_commitment_note)

    blinded_note_posted = client.post_note(blinded_note)
    if blinded_note_posted:
        # Repost the commitment note with a link to the blind submission 
        acl_commitment_note.content['migrated_paper_link'] = f'https://openreview.net/forum?id={blinded_note_posted.forum}'
        #print(acl_commitment_note)
        client.post_note(acl_commitment_note)
        submission_output_dict[acl_commitment_note.forum]['acl_blind_submission_forum'] = blinded_note_posted.forum
        blind_submissions[blinded_note_posted.original] = blinded_note_posted
        post_reviews(blinded_note_posted.forum, blinded_note_posted, arr_submission, submission_output_dict, acl_commitment_note)
    else:
        return submission_output_dict
# Post reviews (calls post_metareviews)
def post_reviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict, acl_commitment_note):
    # Migrate all reviews from the original ARR Submission
    # Get invitation for that month's reviews
    arr_conf_id = arr_submission.invitation.rsplit('/', 2)[0]
    review_invitation_arr = '{arr_conf_id}/Paper{number}/-/Official_Review'.format(arr_conf_id = arr_conf_id,number = arr_submission.number)

    # Get all reviews from the original ARR Submission
    arr_reviews = list(openreview.tools.iterget_notes(client, invitation = review_invitation_arr))

    submission_output_dict[acl_commitment_note.forum]['num_reviews'] = len(arr_reviews)

    # Iterate through each review and for each, create and post a new review
    for arr_review in arr_reviews:
        if(arr_review.signatures[0] not in acl_reviews_dictionary):
            acl_review = openreview.Note(
                forum = acl_blind_submission_forum,
                replyto = acl_blind_submission_forum,
                invitation = f'{confid}/-/ARR_Official_Review',
                signatures = arr_review.signatures,
                readers = [f'{confid}/Program_Chairs'],
                writers = [
                    confid
                ],
                nonreaders=[
                    f"{confid}/Commitment{acl_commitment_note.number}/Conflicts"
                    ],
                content = arr_review.content
            )
            acl_review.content['title'] = f'Official Review of Paper{acl_blind_submission.number} by {arr_review.invitation.split("/")[4]} Reviewer'
            acl_review.content['link_to_original_review'] = f'https://openreview.net/forum?id={arr_review.forum}&noteId={arr_review.id}'
            #profile = client.get_profile(arr_review.tauthor)
            #acl_review.content['reviewer_id'] = f"{profile.id}"
            acl_review_posted = client.post_note(acl_review)
            assert acl_review_posted, print('failed to post review ', acl_review.id)
            acl_reviews_dictionary[acl_review_posted.signatures[0]] = acl_review_posted.replyto
    post_metareviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict, acl_commitment_note)


# Post metareviews
def post_metareviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict, acl_commitment_note):
    # Migrate all reviews from the original ARR Submission
    # Get invitation for that month's reviews
    arr_conf_id = arr_submission.invitation.rsplit('/', 2)[0]
    metareview_invitation_arr = '{arr_conf_id}/Paper{number}/-/Meta_Review'.format(arr_conf_id = arr_conf_id,number = arr_submission.number)

    # Get all reviews from the original ARR Submission
    arr_metareviews = list(openreview.tools.iterget_notes(client, invitation = metareview_invitation_arr))
    submission_output_dict[acl_commitment_note.forum]['num_metareviews'] = len(arr_metareviews)


    # Iterate through each review and for each, create and post a new review
    for arr_metareview in arr_metareviews:
        if(arr_metareview.signatures[0] not in acl_metareviews_dictionary):
            acl_metareview = openreview.Note(
                forum = acl_blind_submission_forum,
                replyto = acl_blind_submission_forum,
                invitation = f'{confid}/-/ARR_Meta_Review',
                signatures = arr_metareview.signatures,
                readers = [f'{confid}/Program_Chairs'],
                nonreaders=[
                    f"{confid}/Commitment{acl_commitment_note.number}/Conflicts"
                    ],
                writers = [
                    confid
                ],
                content = arr_metareview.content
            )
            acl_metareview.content['link_to_original_metareview'] = f'https://openreview.net/forum?id={arr_metareview.forum}&noteId={arr_metareview.id}'
            acl_metareview.content['title'] = f'Meta Review of Paper{acl_blind_submission.number} by {arr_metareview.invitation.split("/")[4]} Area Chair'
            #profile = client.get_profile(arr_metareview.tauthor)
            #acl_metareview.content['action_editor_id'] = f"{profile.id}"
            acl_metareview_posted = client.post_note(acl_metareview)
            assert acl_metareview_posted, print('failed to post metareview ', acl_metareview.id)
            acl_metareviews_dictionary[acl_metareview_posted.signatures[0]] = acl_metareview_posted.replyto
    return submission_output_dict


print('Load commitment notes and rest of the data')
# Retrieve all commitment submissions, ACL submissions, ACL blind submissions, and ACL blind submission reviews
commitment_notes = list(openreview.tools.iterget_notes(client,invitation=f'{confid}/-/Commitment_Submission', sort= 'number:desc'))
acl_submissions = list(openreview.tools.iterget_notes(client,invitation=f'{confid}/-/Migrated_Submission'))
blind_submissions = {note.original: note for note in list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/Migrated_Blind_Submission'))}
acl_reviews_dictionary = {review.signatures[0] : review.replyto for review in list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/ARR_Official_Review'))}
acl_metareviews_dictionary = {review.signatures[0] : review.replyto for review in list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/ARR_Meta_Review'))}

# Save all submissions in a dictionary by paper_link
acl_submission_dict = {(acl_submission.content['paper_link'].split('=')[1]).split('&')[0]:acl_submission for acl_submission in acl_submissions}

submission_output_dict = {}
commitment_invitation = client.get_invitation(f"{confid}/-/Commitment_Submission")
commitment_invitation.reply['content']['migrated_paper_link'] = {
                "description": "Link to the forum of migrated data",
                "value-regex": "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                "required": False,
                "order": 20
                } 
client.post_invitation(commitment_invitation)
print(f'Start processing {len(commitment_notes)} notes...')
for note in tqdm(commitment_notes):
    arr_submission_forum = ((note.content['paper_link'].split('=')[1]).split('&')[0]).strip()
    submission_output_dict[note.forum] = {'acl_blind_submission_forum': None, 'arr_submission_forum': None, 'num_reviews':None, 'num_metareviews':None, 'later_versions?':None, 'duplicate_commitments':None,'was_migrated':False}

    later_duplicates = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/ARR/2021/.*',content = {'previous_URL':f'https://openreview.net/forum?id={arr_submission_forum}'}))
    later_duplicates = later_duplicates + list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/ARR/2022/.*',content = {'previous_URL':f'https://openreview.net/forum?id={arr_submission_forum}'}))
    if later_duplicates:
        submission_output_dict[note.forum]['later_versions?'] = [later_duplicate.forum for later_duplicate in later_duplicates]
    else:
        submission_output_dict[note.forum]['later_versions?'] = False
    # Get the arr submission forum. Then check if that is in the submission dictionary. If it is, check for blind. If not, run post_acl

    if arr_submission_forum not in acl_submission_dict:
        post_acl_submission(arr_submission_forum, note, submission_output_dict)
        #print(f"{submission_output_dict['acl_commitment_forum']},{submission_output_dict['acl_blind_submission_forum']},{submission_output_dict['arr_submission_forum']},{submission_output_dict['num_reviews']},{submission_output_dict['num_metareviews']}, {submission_output_dict['is_latest_version']}, {submission_output_dict['was_migrated']}")

    # Check if the acl_submission.id is in blind_submissions (it is in acl_submissions)
    elif acl_submission_dict[arr_submission_forum].id not in blind_submissions:
        submission_output_dict[note.forum]['arr_submission_forum'] = arr_submission_forum
        submission_output_dict[note.forum]['was_migrated'] = True
        post_blind_submission(acl_submission_dict[arr_submission_forum].id, acl_submission_dict[arr_submission_forum], client.get_note(arr_submission_forum), submission_output_dict, note)
        #print(f"{submission_output_dict['acl_commitment_forum']},{submission_output_dict['acl_blind_submission_forum']},{submission_output_dict['arr_submission_forum']},{submission_output_dict['num_reviews']},{submission_output_dict['num_metareviews']}, {submission_output_dict['is_latest_version']}, {submission_output_dict['was_migrated']}")

    # Check if the blind submission has reviews (it is in blind submissions)
    else:
        submission_output_dict[note.forum]['arr_submission_forum'] = arr_submission_forum
        submission_output_dict[note.forum]['acl_blind_submission_forum'] = blind_submissions[(acl_submission_dict[(note.content['paper_link'].split('=')[1]).split('&')[0]]).forum].forum
        submission_output_dict[note.forum]['was_migrated'] = True
        post_reviews(blind_submissions[acl_submission_dict[arr_submission_forum].id].forum, blind_submissions[acl_submission_dict[arr_submission_forum].id], client.get_note(arr_submission_forum), submission_output_dict, note)
        #post_metareviews(blind_submissions[acl_submission_dict[arr_submission_forum].id].forum, blind_submissions[acl_submission_dict[arr_submission_forum].id], client.get_note(arr_submission_forum), submission_output_dict)
        #print(f"{submission_output_dict['acl_commitment_forum']},{submission_output_dict['acl_blind_submission_forum']},{submission_output_dict['arr_submission_forum']},{submission_output_dict['num_reviews']},{submission_output_dict['num_metareviews']}, {submission_output_dict['is_latest_version']}, {submission_output_dict['was_migrated']}")

fields = ['acl_commitment_note', 'acl_blind_submission', 'original_arr_submission', 'num_reviews', 'num_metareviews', 'later_versions?', 'duplicate_commitments', 'was_migrated']
rows = []
commitment_links = {commitment.forum: (commitment.content['paper_link'].split('=')[1]).split('&')[0] for commitment in commitment_notes}

for key,value in submission_output_dict.items():
    acl_submission = client.get_note(value['acl_blind_submission_forum'])
    count = 0
    duplicate_commitments = []
    # Creates a list of commitment note forums with the same original arr paper link forum
    for forum, link in commitment_links.items(): # key is commitment note forum, value is link
        if link == acl_submission.content.get('paper_link').split('=')[1]:
            count+=1
            duplicate_commitments.append(forum)
    if count > 1:
        value['duplicate_commitments'] = duplicate_commitments
    list = [key, value['acl_blind_submission_forum'], value['arr_submission_forum'], value['num_reviews'], value['num_metareviews'], value['later_versions?'], value['duplicate_commitments'], value['was_migrated']]
    rows.append(list)
with open('output_data.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
