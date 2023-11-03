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
parser.add_argument('--baseurl_v2', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--confid')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
client_v2 = openreview.api.OpenReviewClient(baseurl=args.baseurl_v2, username=args.username, password=args.password)
confid = args.confid

# Post acl submission (calls post_blind_submission)
def post_acl_submission(arr_submission_forum, acl_commitment_note, submission_output_dict):
    # Depends on the workshop
    eligible_arr_invitations = [ ## Should move this to a regex match?
        'aclweb.org/ACL/ARR/2021/May/',
        'aclweb.org/ACL/ARR/2021/Jun/',
        'aclweb.org/ACL/ARR/2021/July/',
        'aclweb.org/ACL/ARR/2021/August/',
        'aclweb.org/ACL/ARR/2021/September/',
        'aclweb.org/ACL/ARR/2021/October/',
        'aclweb.org/ACL/ARR/2021/November/',
        'aclweb.org/ACL/ARR/2021/December/',
        'aclweb.org/ACL/ARR/2022/January/',
        'aclweb.org/ACL/ARR/2022/February/',
        'aclweb.org/ACL/ARR/2022/March/',
        'aclweb.org/ACL/ARR/2022/April/',
        'aclweb.org/ACL/ARR/2022/June/',
        'aclweb.org/ACL/ARR/2022/July/',
        'aclweb.org/ACL/ARR/2022/September/',
        'aclweb.org/ACL/ARR/2022/October/',
        'aclweb.org/ACL/ARR/2022/December/',
        'aclweb.org/ACL/ARR/2023/February/',
        'aclweb.org/ACL/ARR/2023/April/',
        'aclweb.org/ACL/ARR/2023/June/',
        'aclweb.org/ACL/ARR/2023/August/',
        'aclweb.org/ACL/ARR/2023/October/',
        ]
    original_arr_sub_id = None
    note_exists = False
    #submission_output_dict['acl_commitment_forum'] = acl_commitment_note.forum
    try:
        original_arr_sub = client.get_note(arr_submission_forum)
        if(original_arr_sub.original):
            original_arr_sub_id = original_arr_sub.original
        else:
            original_arr_sub_id = original_arr_sub.id
        note_exists = True
    except:
        print(f"Note {arr_submission_forum} does not exist")
    if note_exists and original_arr_sub_id and ((client.get_note(original_arr_sub_id)).invitation.startswith(tuple(eligible_arr_invitations))):
        #print(original_arr_sub_id)
        original_arr_sub = client.get_note(original_arr_sub_id)
        submission_output_dict[acl_commitment_note.forum]['arr_submission_forum'] = original_arr_sub.forum
        print(acl_commitment_note.id)
        first_author = openreview.tools.get_profiles(client,[acl_commitment_note.content['authorids']['value'][0]])[0].id
        authorids_ids = [profile.id for profile in openreview.tools.get_profiles(client, original_arr_sub.content['authorids'])]
        if first_author in authorids_ids:
            # Create new note to submit to ACL
            content = {}
            conf_submission_invitation = client_v2.get_invitation(f"{confid}/-/Migrated_Submission")
            for key in acl_commitment_note.content.keys():
                content[key]= acl_commitment_note.content[key]
            for key in original_arr_sub.content.keys():
                if key in conf_submission_invitation.edit['note']['content']:
                    if key not in content.keys():
                        content[key] = {}
                    content[key]['value'] = original_arr_sub.content[key]
            content['paper_link'] = {}
            content['paper_link']['value'] =f'https://openreview.net/forum?id={arr_submission_forum}'
            content['commitment_note'] = {}
            content['commitment_note']['value'] = f"https://openreview.net/forum?id={acl_commitment_note.forum}"
            acl_sub = openreview.api.Note(
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
            arr_submission = original_arr_sub

            # Create PaperX group -- Submission groups automatically create

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
                    reviewers = '{arr_conf_id}/Paper{number}/Reviewers'.format(arr_conf_id = arr_conf_id, number = arr_number)
                    area_chairs = '{arr_conf_id}/Paper{number}/Area_Chairs'.format(arr_conf_id = arr_conf_id, number = arr_number)
                    conflict_members.append(reviewers)
                    conflict_members.append(area_chairs)

            # CHANGE: Move to group edit
            conflicts = openreview.api.Group(
                id=f'{confid}/Submission{acl_commitment_note.number}/Conflicts',
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
                members=list(set(conflict_members))
            )
            conflicts_posted = client_v2.post_group_edit(
                invitation = f"{confid}/-/Edit",
                readers = [confid],
                writers = [confid],
                signatures = [confid],
                group = conflicts
            )
            
            assert conflicts_posted, print('Failed to post conflict group: ', f'{confid}/Submission{acl_commitment_note.number}/Conflicts')

            # post blinded note
            # CHANGE: move to note edit
            content['authors']['readers'] = [
                confid,
                f"{confid}/Submission{acl_commitment_note.number}/Authors"
            ]
            content['authorids']['readers'] = [
                confid,
                f"{confid}/Submission{acl_commitment_note.number}/Authors"
            ]
            blinded_note = openreview.api.Note(
                readers = [
                    f"{confid}/Program_Chairs",
                    confid,
                    f"{confid}/Submission{acl_commitment_note.number}/Reviewers", f"{confid}/Submission{acl_commitment_note.number}/Area_Chairs", f"{confid}/Submission{acl_commitment_note.number}/Senior_Area_Chairs"
                    #"aclweb.org/ACL/2022/Conference/{sac_track}/Senior_Area_Chairs".format(sac_track = sac_name_dictionary[acl_submission.content['track']])
                ],
                nonreaders = [
                    f"{confid}/Submission{acl_commitment_note.number}/Conflicts"
                ],
                writers = [
                    confid
                ],
                signatures = [
                    confid
                ],
                content = content
            )
            blinded_note_posted = client_v2.post_note_edit( # CHANGE: Move to note edit
                invitation = f"{confid}/-/Migrated_Submission",
                signatures=[confid],
                readers = [
                    f"{confid}/Program_Chairs",
                    confid,
                    f"{confid}/Submission{acl_commitment_note.number}/Reviewers", f"{confid}/Submission{acl_commitment_note.number}/Area_Chairs", f"{confid}/Submission{acl_commitment_note.number}/Senior_Area_Chairs"
                    #"aclweb.org/ACL/2022/Conference/{sac_track}/Senior_Area_Chairs".format(sac_track = sac_name_dictionary[acl_submission.content['track']])
                ],
                nonreaders = [
                    f"{confid}/Submission{acl_commitment_note.number}/Conflicts"
                ],
                writers = [
                    confid
                ],
                note=blinded_note
            )
            acl_submitted = blinded_note_posted

            if blinded_note_posted:
                # Repost the commitment note with a link to the blind submission
                #print(acl_commitment_note)

                # Post review and meta-review invitation edits
                paper_official_review_edit = client_v2.post_invitation_edit(
                    invitations=f"{confid}/-/ARR_Official_Review",
                    readers=[confid],
                    writers=[confid],
                    signatures=[confid],
                    content={
                        'noteId': {
                            'value': blinded_note_posted['note']['id']
                        },
                        'noteNumber': {
                            'value': blinded_note_posted['note']['number']
                        }
                    },
                    invitation=openreview.api.Invitation()
                )
                paper_meta_review_edit = client_v2.post_invitation_edit(
                    invitations=f"{confid}/-/ARR_Meta_Review",
                    readers=[confid],
                    writers=[confid],
                    signatures=[confid],
                    content={
                        'noteId': {
                            'value': blinded_note_posted['note']['id']
                        },
                        'noteNumber': {
                            'value': blinded_note_posted['note']['number']
                        }
                    },
                    invitation=openreview.api.Invitation()
                )

                client_v2.post_note_edit( # CHANGE: Move to note edit
                    invitation = f"{confid}/-/Edit",
                    signatures=[confid],
                    note=openreview.api.Note(
                        id=acl_commitment_note.id,
                        content={
                            'migrated_paper_link': {
                                'value': f"https://openreview.net/forum?id={blinded_note_posted['note']['forum']}"
                            }
                        }
                    )
                )

                submission_output_dict[acl_commitment_note.forum]['was_migrated'] = True
                submission_output_dict[acl_commitment_note.forum]['acl_blind_submission_forum'] = blinded_note_posted['note']['forum']
                acl_submission_dict[acl_submitted['note']['content']['paper_link']['value'].split('=')[1]]=acl_submitted
                blind_submissions[blinded_note_posted['note']['id']] = blinded_note_posted['note']
                post_reviews(blinded_note_posted['note']['id'], blinded_note_posted['note'], arr_submission, submission_output_dict, acl_commitment_note)
            else:
                print(f'Nothing posted for ARR Submission {arr_submission_forum}')
                return submission_output_dict
        else:
            print(f"signature of acl commitment note {acl_commitment_note.id} not in arr submission {arr_submission_forum} authors")
            print(f"first_author={first_author} not in authorids={authorids_ids}")
            return submission_output_dict
    else:
        print(f"acl commitment note {acl_commitment_note.id} links to arr submission {arr_submission_forum} with invalid invitation")
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

            content = arr_review.content
            content['comments_suggestions_and_typos'] = arr_review.content.get('comments,_suggestions_and_typos')
            del content['comments,_suggestions_and_typos']
            new_content = {}
            for key in content.keys():
                if key not in new_content.keys():
                    new_content[key] = {}
                new_content[key]['value'] = content[key]

            if isinstance(acl_blind_submission, openreview.api.Note):
                existing_reviews = [
                    r for r in acl_blind_submission.details['directReplies']
                    if True in ['Official_Review' in inv for inv in r['invitations']]
                ]
                already_posted = True in [new_content['paper_summary']['value'] == r['content']['paper_summary']['value'] for r in existing_reviews]
            else:
                already_posted = False

            if already_posted:
                continue

            acl_review = openreview.api.Note(
                signatures = arr_review.signatures,
                readers = [f'{confid}/Program_Chairs', f"{confid}/Submission{acl_commitment_note.number}/Reviewers", f"{confid}/Submission{acl_commitment_note.number}/Area_Chairs", f"{confid}/Submission{acl_commitment_note.number}/Senior_Area_Chairs"],
                writers = [
                    confid
                ],
                nonreaders=[
                    f"{confid}/Submission{acl_commitment_note.number}/Conflicts"
                ],
                content = new_content
            )
            submission_number = acl_blind_submission['number'] if isinstance(acl_blind_submission, dict) else acl_blind_submission.number
            acl_review.content['title'] = {}
            acl_review.content['title']['value'] = f"Official Review of Submission{submission_number} by {arr_review.invitation.split('/')[4]} Reviewer"

            acl_review_posted = client_v2.post_note_edit( # CHANGE: Move to note edit
                invitation = f"{confid}/Submission{submission_number}/-/ARR_Official_Review",
                readers = [f'{confid}/Program_Chairs', f"{confid}/Submission{acl_commitment_note.number}/Reviewers", f"{confid}/Submission{acl_commitment_note.number}/Area_Chairs", f"{confid}/Submission{acl_commitment_note.number}/Senior_Area_Chairs"],
                writers = [
                    confid
                ],
                nonreaders=[
                    f"{confid}/Submission{acl_commitment_note.number}/Conflicts"
                ],
                signatures=[confid],
                note=acl_review
            )
            assert acl_review_posted, print('failed to post review ', acl_review.id)
            acl_reviews_dictionary[acl_review_posted['note']['signatures'][0]] = acl_review_posted['note']['replyto']
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
            content = arr_metareview.content
            new_content = {}
            for key in content.keys():
                if key not in new_content.keys():
                    new_content[key] = {}
                new_content[key]['value'] = content[key]

            if isinstance(acl_blind_submission, openreview.api.Note):
                existing_reviews = [
                    r for r in acl_blind_submission.details['directReplies']
                    if True in ['Meta_Review' in inv for inv in r['invitations']]
                ]
                already_posted = True in [new_content['metareview']['value'] == r['content']['metareview']['value'] for r in existing_reviews]
            else:
                already_posted = False

            if already_posted:
                continue

            acl_metareview = openreview.api.Note(
                signatures = arr_metareview.signatures,
                readers = [f'{confid}/Program_Chairs', f"{confid}/Submission{acl_commitment_note.number}/Reviewers", f"{confid}/Submission{acl_commitment_note.number}/Area_Chairs", f"{confid}/Submission{acl_commitment_note.number}/Senior_Area_Chairs"],
                nonreaders=[
                    f"{confid}/Submission{acl_commitment_note.number}/Conflicts"
                ],
                writers = [
                    confid
                ],
                content = new_content
            )
            #acl_metareview.content['link_to_original_metareview'] = f'https://openreview.net/forum?id={arr_metareview.forum}&noteId={arr_metareview.id}'
            submission_number = acl_blind_submission['number'] if isinstance(acl_blind_submission, dict) else acl_blind_submission.number
            acl_metareview.content['title'] = {}
            acl_metareview.content['title']['value'] = f"Meta Review of Submission{submission_number} by {arr_metareview.invitation.split('/')[4]} Action Editor"
            #profile = client.get_profile(arr_metareview.tauthor)
            #acl_metareview.content['action_editor_id'] = f"{profile.id}"

            acl_metareview_posted = client_v2.post_note_edit( # CHANGE: Move to note edit
                invitation = f"{confid}/Submission{submission_number}/-/ARR_Meta_Review",
                signatures=[confid],
                readers = [f'{confid}/Program_Chairs', f"{confid}/Submission{acl_commitment_note.number}/Reviewers", f"{confid}/Submission{acl_commitment_note.number}/Area_Chairs", f"{confid}/Submission{acl_commitment_note.number}/Senior_Area_Chairs"],
                writers = [
                    confid
                ],
                nonreaders=[
                    f"{confid}/Submission{acl_commitment_note.number}/Conflicts"
                ],
                note=acl_metareview
            )
            assert acl_metareview_posted, print('failed to post metareview ', acl_metareview.id)
            acl_metareviews_dictionary[acl_metareview_posted['note']['signatures'][0]] = acl_metareview_posted['note']['replyto']
    return submission_output_dict


print('Load commitment notes and rest of the data')
# Retrieve all commitment submissions, ACL submissions, ACL blind submissions, and ACL blind submission reviews
commitment_notes = client_v2.get_all_notes(invitation=f'{confid}/-/Submission', content={ 'venueid': f'{confid}/Submission'}, sort='number:asc')
acl_submissions = list(openreview.tools.iterget_notes(client_v2,invitation=f'{confid}/-/Migrated_Submission', details='directReplies'))
blind_submissions = {note.id: note for note in list(openreview.tools.iterget_notes(client_v2, invitation = f'{confid}/-/Migrated_Submission', details='directReplies'))}
acl_reviews_dictionary = {review.signatures[0] : review.replyto for review in list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/ARR_Official_Review'))}
acl_metareviews_dictionary = {review.signatures[0] : review.replyto for review in list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/ARR_Meta_Review'))}

# Save all submissions in a dictionary by paper_link
acl_submission_dict = {(acl_submission.content['paper_link']['value'].split('=')[1]).split('&')[0]:acl_submission for acl_submission in acl_submissions}

submission_output_dict = {}
commitment_invitation = client_v2.get_invitation(f"{confid}/-/Submission")
commitment_invitation.edit['note']['content']['migrated_paper_link'] = {
    "order": 20,
    "description": "Link to the forum of migrated data",
    "value": {
        "param": {
            "type": "string",
            "regex": "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "optional": True,
            "input": "textarea"
        }
    }
}
client_v2.post_invitation_edit(invitations=f"{confid}/-/Edit",
    readers=[confid],
    writers=[confid],
    signatures=[confid],
    invitation=commitment_invitation
)

print(f'Start processing {len(commitment_notes)} notes...')
for note in tqdm(commitment_notes):
    arr_submission_forum = ((note.content['paper_link']['value'].split('=')[1]).split('&')[0]).strip()
    submission_output_dict[note.forum] = {'acl_blind_submission_forum': None, 'arr_submission_forum': None, 'num_reviews':None, 'num_metareviews':None, 'later_versions?':None, 'duplicate_commitments':None,'was_migrated':False}

    later_duplicates = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/ARR/2021/.*',content = {'previous_URL':f'https://openreview.net/forum?id={arr_submission_forum}'}))
    later_duplicates = later_duplicates + list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/ARR/2022/.*',content = {'previous_URL':f'https://openreview.net/forum?id={arr_submission_forum}'}))
    later_duplicates = later_duplicates + list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/ARR/2023/.*',content = {'previous_URL':f'https://openreview.net/forum?id={arr_submission_forum}'}))
    if later_duplicates:
        submission_output_dict[note.forum]['later_versions?'] = [later_duplicate.forum for later_duplicate in later_duplicates]
    else:
        submission_output_dict[note.forum]['later_versions?'] = False
    # Get the arr submission forum. Then check if that is in the submission dictionary. If it is, check for blind. If not, run post_acl

    if arr_submission_forum not in acl_submission_dict:
        post_acl_submission(arr_submission_forum, note, submission_output_dict)
        #print(f"{submission_output_dict['acl_commitment_forum']},{submission_output_dict['acl_blind_submission_forum']},{submission_output_dict['arr_submission_forum']},{submission_output_dict['num_reviews']},{submission_output_dict['num_metareviews']}, {submission_output_dict['is_latest_version']}, {submission_output_dict['was_migrated']}")

    # Check if the blind submission has reviews (it is in blind submissions)
    else:
        submission_output_dict[note.forum]['arr_submission_forum'] = arr_submission_forum
        submission_output_dict[note.forum]['acl_blind_submission_forum'] = blind_submissions[(acl_submission_dict[(note.content['paper_link']['value'].split('=')[1]).split('&')[0]]).forum].forum
        submission_output_dict[note.forum]['was_migrated'] = True
        post_reviews(blind_submissions[acl_submission_dict[arr_submission_forum].id].forum, blind_submissions[acl_submission_dict[arr_submission_forum].id], client.get_note(arr_submission_forum), submission_output_dict, note)
        post_metareviews(blind_submissions[acl_submission_dict[arr_submission_forum].id].forum, blind_submissions[acl_submission_dict[arr_submission_forum].id], client.get_note(arr_submission_forum), submission_output_dict, note)
        #print(f"{submission_output_dict['acl_commitment_forum']},{submission_output_dict['acl_blind_submission_forum']},{submission_output_dict['arr_submission_forum']},{submission_output_dict['num_reviews']},{submission_output_dict['num_metareviews']}, {submission_output_dict['is_latest_version']}, {submission_output_dict['was_migrated']}")

fields = ['acl_commitment_note', 'acl_blind_submission', 'original_arr_submission', 'num_reviews', 'num_metareviews', 'later_versions?', 'duplicate_commitments', 'was_migrated']
rows = []
commitment_links = {commitment.forum: (commitment.content['paper_link']['value'].split('=')[1]).split('&')[0] for commitment in commitment_notes}

for key,value in submission_output_dict.items():
    try:
        acl_submission = client_v2.get_note(id=value['acl_blind_submission_forum'])
    except Exception as e:
        print(f"no submission found: {key}:{value}")
        continue
    count = 0
    duplicate_commitments = []
    # Creates a list of commitment note forums with the same original arr paper link forum
    for forum, link in commitment_links.items(): # key is commitment note forum, value is link
        if link == acl_submission.content.get('paper_link').get('value').split('=')[1]:
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
