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
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

# Creating SAC groups from Track Name
sac_name_dictionary = {
    'Ethics in NLP': 'Ethics_NLP',
    'Linguistic theories, Cognitive Modeling and Psycholinguistics': 'LCMP',
    'Linguistic Theories, Cognitive Modeling and Psycholinguistics': 'LCMP',
    'Machine Learning for NLP': 'Machine_Learning_NLP',
    'Phonology, Morphology and Word Segmentation': 'Phonology_Morphology_Word_Segmentation',
    'Resources and Evaluation': 'Resources_Evaluation',
    'Semantics: Lexical': 'Semantics_Lexical',
    'Semantics: Sentence level, Textual Inference and Other areas': 'Semantics_STO',
    'Syntax: Tagging, Chunking and Parsing': 'Syntax_TCP',
    'Information Extraction': 'Information_Extraction',
    'Computational Social Science and Cultural Analytics': 'CSSCA',
    'Information Retrieval and Text Mining': 'Info_Retrieval_Text_Mining',
    'Interpretability and Analysis of Models for NLP': 'IAM_for_NLP',
    'Machine Translation and Multilinguality': 'Machine_Translation_Multilinguality',
    'NLP Applications': 'NLP_Applications',
    'Question Answering': 'Question_Answering',
    'Dialogue and Interactive Systems': 'Dialogue_and_Interactive_Systems',
    'Discourse and Pragmatics': 'Discourse_and_Pragmatics',
    'Generation': 'Generation',
    'Language Grounding to Vision, Robotics, and Beyond': 'LGVRB',
    'Sentiment Analysis, Stylistic Analysis, and Argument Mining': 'SASAAM',
    'Speech and Multimodality': 'Speech_and_Multimodality',
    'Summarization': 'Summarization',
    'Special Theme on Language Diversity: From Low Resource to Endangered Languages': 'Special_Theme'
    }
# Create dictionary for SAC groups and members
print('Load SAC groups')
track_SAC_profiles = {}
track_groups = { group.id: group for group in client.get_groups('aclweb.org/ACL/2022/Conference/.*/Senior_Area_Chairs')}
profile_ids = []
for track_name, group_abbreviation in sac_name_dictionary.items():
    print(track_name)
    group = track_groups[f'aclweb.org/ACL/2022/Conference/{group_abbreviation}/Senior_Area_Chairs']
    profile_ids = profile_ids + group.members

print(f'Load SAC {len(list(set(profile_ids)))} profiles')
SAC_profiles = { p.id: p for p in openreview.tools.get_profiles(client, list(set(profile_ids)), with_publications = True)}
    # profiles = openreview.tools.get_profiles(client, group.members, with_publications = True)
    # track_SAC_profiles[track_name] = profiles


# Post acl submission (calls post_blind_submission)
def post_acl_submission(arr_submission_forum, acl_commitment_note, submission_output_dict):

    eligible_arr_invitations = ['aclweb.org/ACL/ARR/2021/May/', 'aclweb.org/ACL/ARR/2021/Jun/', 'aclweb.org/ACL/ARR/2021/July/', 'aclweb.org/ACL/ARR/2021/August/', 'aclweb.org/ACL/ARR/2021/September/','aclweb.org/ACL/ARR/2021/October/','aclweb.org/ACL/ARR/2021/November/']
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
            acl_sub = openreview.Note(
                invitation="aclweb.org/ACL/2022/Conference/-/Submission",
                readers = [
                    "aclweb.org/ACL/2022/Conference"
                    ],
                writers = [
                    "aclweb.org/ACL/2022/Conference"
                    ],
                signatures = [
                    "aclweb.org/ACL/2022/Conference"
                    ],
                content = {
                    "paper_link": f'https://openreview.net/forum?id={arr_submission_forum}',
                    "paper_type":acl_commitment_note.content["paper_type"],
                    "track":acl_commitment_note.content["track"],
                    "comments_to_the_senior_area_chairs":acl_commitment_note.content.get("comments to the senior area chairs"),
                    "authorids":original_arr_sub.content["authorids"],
                    "authors": original_arr_sub.content["authors"],
                    "title":original_arr_sub.content["title"],
                    "abstract":original_arr_sub.content["abstract"],
                    "data":original_arr_sub.content.get("data"),
                    "software":original_arr_sub.content.get("software"),
                    "pdf":original_arr_sub.content.get("pdf"), #is it okay that this is the original note forum?
                    "acl_preprint": acl_commitment_note.content.get("ACL_preprint"),
                    "existing_preprints": original_arr_sub.content.get("existing_preprints"),
                    "preprint":original_arr_sub.content.get("preprint"),
                    "TL;DR":original_arr_sub.content.get('TL;DR'),
                    "previous_URL": original_arr_sub.content.get("previous_URL"),
                    "authorship": acl_commitment_note.content.get("authorship"),
                    "paper_version": acl_commitment_note.content.get("paper version"),
                    "anonymity_period": acl_commitment_note.content.get("anonymity period"),
                    "commitment_note": f"https://openreview.net/forum?id={acl_commitment_note.forum}"
                }
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
        id = 'aclweb.org/ACL/2022/Conference/Paper{number}'.format(number = number),
        signatures = [
            'aclweb.org/ACL/2022/Conference'
            ],
        signatories = [
            'aclweb.org/ACL/2022/Conference'
            ],
        readers = [
            'aclweb.org/ACL/2022/Conference'
            #'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
            ],
        writers = [
            'aclweb.org/ACL/2022/Conference'
            ]
    )
    client.post_group(paper_group)

    # Create paperX/Authors
    authors = openreview.Group(
        id = 'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number),
        signatures = [
            'aclweb.org/ACL/2022/Conference'
            ],
        signatories = [
            'aclweb.org/ACL/2022/Conference'
            #'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
            ],
        readers = [
            'aclweb.org/ACL/2022/Conference'
            #'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
            ],
        writers = [
            'aclweb.org/ACL/2022/Conference'
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
            '{conf_id}/Paper{number}/Area_Chairs'.format(conf_id = conf_id, number = arr_number)
            ]
    # Find all previous & future submissions and for each one add the reviewers and ACs to the conflict group
    def get_reviewer_AC_conflicts(current_submission):
        previous_url = current_submission.content.get('previous_URL')
        if previous_url and ("openreview.net" in previous_url):
            print(current_submission.forum)
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
            conf_id = later_submission.invitation.rsplit('/', 2)[0]
            arr_number = later_submission.number
            reviewers = '{conf_id}/Paper{number}/Reviewers'.format(conf_id = conf_id, number = arr_number)
            area_chairs = '{conf_id}/Paper{number}/Area_Chairs'.format(conf_id = conf_id, number = arr_number)
            conflict_members.append(reviewers)
            conflict_members.append(area_chairs)

    author_group = openreview.tools.get_profiles(client, ids_or_emails = authors.members, with_publications=True)

    # Get all SAC profiles from track dictionary, and for each one check conflicts
    for SAC in track_groups[f"aclweb.org/ACL/2022/Conference/{sac_name_dictionary[acl_submission.content['track']]}/Senior_Area_Chairs"].members:
        conflicts = openreview.tools.get_conflicts(author_group, SAC_profiles[SAC], policy = 'neurips', n_years=5)
        if conflicts:
            conflict_members.append(SAC)
    #print(acl_submission.content['track'])
    #for SAC in (openreview.tools.get_group(client, "aclweb.org/ACL/2022/Conference/{sac_track}/Senior_Area_Chairs".format(sac_track = sac_name_dictionary[acl_submission.content['track']]))).members:
        #print(SAC)
    #   SAC_profile = openreview.tools.get_profiles(client, [SAC], with_publications = True)
    #    if(SAC_profile):
    #        conflicts = openreview.tools.get_conflicts(author_group, SAC_profile[0])
    #        if conflicts:
    #            conflict_members.append(SAC_profile[0].id)



    conflicts = openreview.Group(
        id = 'aclweb.org/ACL/2022/Conference/Paper{number}/Conflicts'.format(number = number),
        signatures = [
            'aclweb.org/ACL/2022/Conference'
            ],
        signatories = [
            'aclweb.org/ACL/2022/Conference'
            ],
        readers = [
            'aclweb.org/ACL/2022/Conference'
            ],
        writers = [
            'aclweb.org/ACL/2022/Conference'
            ],
        members = conflict_members
    )
    conflicts_posted = client.post_group(conflicts)
    assert conflicts_posted, print('Failed to post conflict group: ', acl_submission_id)

    # post blinded note
    blinded_note = openreview.Note(
            invitation = "aclweb.org/ACL/2022/Conference/-/Blind_Submission",
            original = acl_submission_id,
            readers = [
                "aclweb.org/ACL/2022/Conference/Program_Chairs",
                "aclweb.org/ACL/2022/Conference"
                #"aclweb.org/ACL/2022/Conference/{sac_track}/Senior_Area_Chairs".format(sac_track = sac_name_dictionary[acl_submission.content['track']])
                ],
            nonreaders = [
                "aclweb.org/ACL/2022/Conference/Paper{number}/Conflicts".format(number = acl_submission.number)
                ],
            writers = [
                "aclweb.org/ACL/2022/Conference"
                ],
            signatures = [
                "aclweb.org/ACL/2022/Conference"
                ],
            content = {
                "authorids" : [f"aclweb.org/ACL/2022/Conference/Paper{acl_submission.number}/Authors"],
                "authors":["Anonymous"]
            }
        )

    blinded_note_posted = client.post_note(blinded_note)
    if blinded_note_posted:
        #print(acl_commitment_note)
        #print(blinded_note_posted.forum)
        submission_output_dict[acl_commitment_note.forum]['acl_blind_submission_forum'] = blinded_note_posted.forum
        blind_submissions[blinded_note_posted.original] = blinded_note_posted
        post_reviews(blinded_note_posted.forum, blinded_note_posted, arr_submission, submission_output_dict, acl_commitment_note)
    else:
        return submission_output_dict
# Post reviews (calls post_metareviews)
def post_reviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict, acl_commitment_note):
    # Migrate all reviews from the original ARR Submission
    # Get invitation for that month's reviews
    conf_id = arr_submission.invitation.rsplit('/', 2)[0]
    review_invitation_arr = '{conf_id}/Paper{number}/-/Official_Review'.format(conf_id = conf_id,number = arr_submission.number)

    # Get all reviews from the original ARR Submission
    arr_reviews = list(openreview.tools.iterget_notes(client, invitation = review_invitation_arr))

    submission_output_dict[acl_commitment_note.forum]['num_reviews'] = len(arr_reviews)

    # Iterate through each review and for each, create and post a new review
    for arr_review in arr_reviews:
        if(arr_review.signatures[0] not in acl_reviews_dictionary):
            acl_review = openreview.Note(
                forum = acl_blind_submission_forum,
                replyto = acl_blind_submission_forum,
                invitation = 'aclweb.org/ACL/2022/Conference/-/Official_Review',
                signatures = arr_review.signatures,
                readers = ['aclweb.org/ACL/2022/Conference/Program_Chairs'],
                writers = [
                    'aclweb.org/ACL/2022/Conference'
                ],
                nonreaders=[
                    "aclweb.org/ACL/2022/Conference/Paper{number}/Conflicts".format(number = acl_blind_submission.number)
                    ],
                content = arr_review.content
            )
            acl_review.content['title'] = f'Official Review of Paper{acl_blind_submission.number} by {arr_review.invitation.split("/")[4]} Reviewer'
            acl_review.content['link_to_original_review'] = f'https://openreview.net/forum?id={arr_review.forum}&noteId={arr_review.id}'
            profile = client.get_profile(arr_review.tauthor)
            acl_review.content['reviewer_id'] = f"{profile.id}"
            acl_review_posted = client.post_note(acl_review)
            assert acl_review_posted, print('failed to post review ', acl_review.id)
            acl_reviews_dictionary[acl_review_posted.signatures[0]] = acl_review_posted.replyto
    post_metareviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict, acl_commitment_note)


# Post metareviews
def post_metareviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict, acl_commitment_note):
    # Migrate all reviews from the original ARR Submission
    # Get invitation for that month's reviews
    conf_id = arr_submission.invitation.rsplit('/', 2)[0]
    metareview_invitation_arr = '{conf_id}/Paper{number}/-/Meta_Review'.format(conf_id = conf_id,number = arr_submission.number)

    # Get all reviews from the original ARR Submission
    arr_metareviews = list(openreview.tools.iterget_notes(client, invitation = metareview_invitation_arr))
    submission_output_dict[acl_commitment_note.forum]['num_metareviews'] = len(arr_metareviews)


    # Iterate through each review and for each, create and post a new review
    for arr_metareview in arr_metareviews:
        if(arr_metareview.signatures[0] not in acl_metareviews_dictionary):
            acl_metareview = openreview.Note(
                forum = acl_blind_submission_forum,
                replyto = acl_blind_submission_forum,
                invitation = f'aclweb.org/ACL/2022/Conference/-/Meta_Review',
                signatures = arr_metareview.signatures,
                readers = ['aclweb.org/ACL/2022/Conference/Program_Chairs'],
                nonreaders=[
                    "aclweb.org/ACL/2022/Conference/Paper{number}/Conflicts".format(number = acl_blind_submission.number)
                    ],
                writers = [
                    'aclweb.org/ACL/2022/Conference'
                ],
                content = arr_metareview.content
            )
            acl_metareview.content['link_to_original_metareview'] = f'https://openreview.net/forum?id={arr_metareview.forum}&noteId={arr_metareview.id}'
            acl_metareview.content['title'] = f'Meta Review of Paper{acl_blind_submission.number} by {arr_metareview.invitation.split("/")[4]} Area Chair'
            profile = client.get_profile(arr_metareview.tauthor)
            acl_metareview.content['action_editor_id'] = f"{profile.id}"
            acl_metareview_posted = client.post_note(acl_metareview)
            assert acl_metareview_posted, print('failed to post metareview ', acl_metareview.id)
            acl_metareviews_dictionary[acl_metareview_posted.signatures[0]] = acl_metareview_posted.replyto
    return submission_output_dict


print('Load commitment notes and rest of the data')
# Retrieve all commitment submissions, ACL submissions, ACL blind submissions, and ACL blind submission reviews
commitment_notes = list(openreview.tools.iterget_notes(client,invitation='aclweb.org/ACL/2022/Conference/-/Commitment_Submission', sort= 'number:asc'))
acl_submissions = list(openreview.tools.iterget_notes(client,invitation='aclweb.org/ACL/2022/Conference/-/Submission'))
blind_submissions = {note.original: note for note in list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))}
acl_reviews_dictionary = {review.signatures[0] : review.replyto for review in list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Official_Review'))}
acl_metareviews_dictionary = {review.signatures[0] : review.replyto for review in list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Meta_Review'))}

# Save all submissions in a dictionary by paper_link
acl_submission_dict = {(acl_submission.content['paper_link'].split('=')[1]).split('&')[0]:acl_submission for acl_submission in acl_submissions}
#print("acl_commitment_forum", "acl_blind_submission_forum", "arr_submission_forum", "num_reviews", "num_metareviews", "is_latest_version", "was_migrated")
# Create an empty list to store information about each paper for the PCs to view
submission_output_dict = {}
print(f'Start processing {len(commitment_notes)} notes...')
for note in tqdm(commitment_notes):
    arr_submission_forum = (note.content['paper_link'].split('=')[1]).split('&')[0]
    submission_output_dict[note.forum] = {'acl_blind_submission_forum': None, 'arr_submission_forum': None, 'num_reviews':None, 'num_metareviews':None, 'later_versions':None, 'duplicate_commitments':None,'was_migrated':False}

    later_duplicates = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/ARR/2021/.*',content = {'previous_URL':f'https://openreview.net/forum?id={arr_submission_forum}'}))
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
