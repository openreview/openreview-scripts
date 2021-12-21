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
    'Machine Learning for NLP': 'Machine_Learning_NLP', 
    'Phonology, Morphology and Word Segmentation': 'Phonology_Morphology_Word_Segmentation', 
    'Resources and Evaluation': 'Resources_Evaluation', 
    'Semantics: Lexical': 'Semantics_Lexical', 
    'Semantics: Sentence-level Semantics, Textual Inference, and Other areas': 'Semantics_STO', 
    'Syntax: Tagging, Chunking and Parsing': 'Syntax_TCP', 
    'Information Extvaluesraction': 'Information_Extraction', 
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

# Post acl submission (calls post_blind_submission)
def post_acl_submission(arr_submission_forum, acl_commitment_note, submission_output_dict):
    # Check for later duplicates 
    later_duplicates = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/ARR/2021/.*',content = {'previous_URL':f'https://openreview.net/forum?id={arr_submission_forum}'}))  
    eligible_arr_invitations = ['aclweb.org/ACL/ARR/2021/May/', 'aclweb.org/ACL/ARR/2021/Jun/', 'aclweb.org/ACL/ARR/2021/July/', 'aclweb.org/ACL/ARR/2021/August/', 'aclweb.org/ACL/ARR/2021/September/','aclweb.org/ACL/ARR/2021/October/','aclweb.org/ACL/ARR/2021/November/']    
    original_arr_sub_id = None
    submission_output_dict['acl_commitment_forum'] = acl_commitment_note.forum
    try:
        original_arr_sub_id = client.get_note(arr_submission_forum).original
    except:
        print(f"Note {arr_submission_forum} does not exist")
    if original_arr_sub_id and ((client.get_note(original_arr_sub_id)).invitation.startswith(tuple(eligible_arr_invitations))):
        original_arr_sub = client.get_note(original_arr_sub_id)
        submission_output_dict['arr_submission_forum'] = original_arr_sub.forum
        if acl_commitment_note.signatures[0] in original_arr_sub.content['authorids']:
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
                    "paper_link": note.content["paper_link"],
                    "paper_type":note.content["paper_type"],
                    "track":note.content["track"],
                    "comments_to_the_senior_area_chairs":note.content.get("comments_to_the_senior_area_chairs"),
                    "authorids":original_arr_sub.content["authorids"],
                    "authors": original_arr_sub.content["authors"],
                    "title":original_arr_sub.content["title"],
                    "abstract":original_arr_sub.content["abstract"],
                    "data":original_arr_sub.content.get("data"),
                    "software":original_arr_sub.content.get("software"),
                    "pdf":original_arr_sub.content.get("pdf"),
                    "acl_preprint": note.content.get("ACL_preprint"),
                    "existing_preprints": note.content.get("existing_preprints"),
                    "authorship": note.content.get("authorship"),
                    "paper_version": note.content.get("paper version"),
                    "anonymity_period": note.content.get("anonymity period"),
                    "commitment_note": f"https://openreview.net/forum?id={acl_commitment_note.forum}"
                }  
            )
            acl_submitted = client.post_note(acl_sub)
            if(acl_submitted):
                submission_output_dict['was_migrated'] = True
                if later_duplicates:
                    submission_output_dict['is_latest_version'] = False 
                acl_submission_dict[acl_submitted.content['paper_link'].split('=')[1]]=acl_submitted
                post_blind_submission(acl_submitted.id, acl_submitted, client.get_note(original_arr_sub_id), submission_output_dict)
            else: 
                print(f'Nothing posted for ARR Submission {arr_submission_forum}')
        else:
            print(f"signature of acl commitment note {acl_commitment_note.id} not in arr submission {arr_submission_forum} authors")
            if later_duplicates:
                submission_output_dict['is_latest_version'] = False
    else:
        print(f"acl commitment note {acl_commitment_note.id} links to arr submission {arr_submission_forum} with invalid invitation")
            
        
    
        
# Post blind submission (calls post_reviews)
def post_blind_submission(acl_submission_id, acl_submission, arr_submission, submission_output_dict):
    # Post requisite groups 
    number = acl_submission.number
    # Create paperX/Authors 
    authors = openreview.Group(
        id = 'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number), 
        signatures = [
            'aclweb.org/ACL/2022/Conference'
            ],
        signatories = [
            'aclweb.org/ACL/2022/Conference', 
            'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
            ],
        readers = [
            'aclweb.org/ACL/2022/Conference', 
            'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
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
            '{conf_id}/Paper{number}/Area_Chairs'.format(conf_id = conf_id, number = arr_number),
            'aclweb.org/ACL/2022/Conference/Paper{number}/Authors'.format(number = number)
            ]
    author_group = []
    for author in authors.members:
        author_group.append(openreview.tools.get_profile(client, author))
    for SAC in (openreview.tools.get_group(client, "aclweb.org/ACL/2022/Conference/{sac_track}/Senior_Area_Chairs".format(sac_track = sac_name_dictionary[acl_submission.content['track']]))).members: 
        #print(SAC)
        SAC = openreview.tools.get_profile(client, SAC)
        conflicts = openreview.tools.get_conflicts(author_group, SAC)
        if conflicts: 
            conflict_members.append(SAC)
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
                "aclweb.org/ACL/2022/Conference", 
                "aclweb.org/ACL/2022/Conference/{sac_track}/Senior_Area_Chairs".format(sac_track = sac_name_dictionary[acl_submission.content['track']])
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
        submission_output_dict['acl_blind_submission_forum'] = blinded_note_posted.forum
        blind_submissions[blinded_note_posted.original] = blinded_note_posted
        post_reviews(blinded_note_posted.forum, blinded_note_posted, arr_submission, submission_output_dict)

# Post reviews (calls post_metareviews)
def post_reviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict):
    # Migrate all reviews from the original ARR Submission 
    # Get invitation for that month's reviews 
    conf_id = arr_submission.invitation.rsplit('/', 2)[0]
    review_invitation_arr = '{conf_id}/Paper{number}/-/Official_Review'.format(conf_id = conf_id,number = arr_submission.number)
    
    # Get all reviews from the original ARR Submission 
    arr_reviews = list(openreview.tools.iterget_notes(client, invitation = review_invitation_arr))
    
    submission_output_dict['num_reviews'] = len(arr_reviews)

    # Iterate through each review and for each, create and post a new review 
    for arr_review in arr_reviews:
        if(arr_review.signatures[0] not in acl_reviews_dictionary):
            acl_review = openreview.Note(
                forum = acl_blind_submission_forum,
                replyto = acl_blind_submission_forum,
                invitation = 'aclweb.org/ACL/2022/Conference/-/Official_Review',
                signatures = arr_review.signatures,
                readers = acl_blind_submission.readers,
                writers = [
                    'aclweb.org/ACL/2022/Conference'
                ],
                content = arr_review.content
            )
            acl_review_posted = client.post_note(acl_review)
            assert acl_review_posted, print('failed to post review ', acl_review.id)
            acl_reviews_dictionary[acl_review_posted.signatures[0]] = acl_review_posted.replyto
    post_metareviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict)
    
        
# Post metareviews 
def post_metareviews(acl_blind_submission_forum, acl_blind_submission, arr_submission, submission_output_dict):
    print('entered post metareview')
    # Migrate all reviews from the original ARR Submission 
    # Get invitation for that month's reviews 
    conf_id = arr_submission.invitation.rsplit('/', 2)[0]
    metareview_invitation_arr = '{conf_id}/Paper{number}/-/Meta_Review'.format(conf_id = conf_id,number = arr_submission.number)
    
    # Get all reviews from the original ARR Submission 
    arr_metareviews = list(openreview.tools.iterget_notes(client, invitation = metareview_invitation_arr))
    submission_output_dict['num_metareviews'] = len(arr_metareviews)
    print('length of arr_metareviews', len(arr_metareviews))
     
    
    # Iterate through each review and for each, create and post a new review 
    for arr_metareview in arr_metareviews:
        if(arr_metareview.signatures[0] not in acl_metareviews_dictionary):
            acl_metareview = openreview.Note(
                forum = acl_blind_submission_forum,
                replyto = acl_blind_submission_forum,
                invitation = f'aclweb.org/ACL/2022/Conference/-/Meta_Review',
                signatures = arr_metareview.signatures,
                readers = acl_blind_submission.readers,
                writers = [
                    'aclweb.org/ACL/2022/Conference'
                ],
                content = arr_metareview.content
            )
            acl_metareview_posted = client.post_note(acl_metareview)
            assert acl_metareview_posted, print('failed to post metareview ', acl_metareview.id)
            acl_metareviews_dictionary[acl_metareview_posted.signatures[0]] = acl_metareview_posted.replyto
    return submission_output_dict

            
# Retrieve all commitment submissions, ACL submissions, ACL blind submissions, and ACL blind submission reviews  
commitment_notes = list(openreview.tools.iterget_notes(client,invitation='aclweb.org/ACL/2022/Conference/-/Commitment_Submission'))
acl_submissions = list(openreview.tools.iterget_notes(client,invitation='aclweb.org/ACL/2022/Conference/-/Submission'))
blind_submissions = {note.original: note for note in list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))}
acl_reviews_dictionary = {review.signatures[0] : review.replyto for review in list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Official_Review'))}
acl_metareviews_dictionary = {review.signatures[0] : review.replyto for review in list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Meta_Review'))}

# Save all submissions in a dictionary by paper_link
acl_submission_dict = {acl_submission.content['paper_link'].split('=')[1]:acl_submission for acl_submission in acl_submissions}
# Create an empty list to store information about each paper for the PCs to view 
for note in commitment_notes: 
    submission_output_dict = {'acl_commitment_forum': None, 'acl_blind_submission_forum': None, 'arr_submission_forum': None, 'num_reviews':None, 'num_metareviews':None, 'is_latest_version':None, 'was_migrated':False}
    # Get the arr submission forum. Then check if that is in the submission dictionary. If it is, check for blind. If not, run post_acl
    arr_submission_forum = note.content['paper_link'].split('=')[1]
    if arr_submission_forum not in acl_submission_dict:
        post_acl_submission(arr_submission_forum, note, submission_output_dict)
        print(f"{submission_output_dict['acl_commitment_forum']},{submission_output_dict['acl_blind_submission_forum']},{submission_output_dict['arr_submission_forum']},{submission_output_dict['num_reviews']},{submission_output_dict['num_metareviews']}, {submission_output_dict['is_latest_version']}, {submission_output_dict['was_migrated']}")
        
    # Check if the acl_submission.id is in blind_submissions
    elif acl_submission_dict[arr_submission_forum].id not in blind_submissions:
        post_blind_submission(acl_submission_dict[arr_submission_forum].id, acl_submission_dict[arr_submission_forum], client.get_note(arr_submission_forum), submission_output_dict)
        print(f"{submission_output_dict['acl_commitment_forum']},{submission_output_dict['acl_blind_submission_forum']},{submission_output_dict['arr_submission_forum']},{submission_output_dict['num_reviews']},{submission_output_dict['num_metareviews']}, {submission_output_dict['is_latest_version']}, {submission_output_dict['was_migrated']}")

    # Check if the blind submission has reviews
    else: 
        post_reviews(blind_submissions[acl_submission_dict[arr_submission_forum].id].forum, blind_submissions[acl_submission_dict[arr_submission_forum].id], client.get_note(arr_submission_forum), submission_output_dict)
        #post_metareviews(blind_submissions[acl_submission_dict[arr_submission_forum].id].forum, blind_submissions[acl_submission_dict[arr_submission_forum].id], client.get_note(arr_submission_forum), submission_output_dict)
        print(f"{submission_output_dict['acl_commitment_forum']},{submission_output_dict['acl_blind_submission_forum']},{submission_output_dict['arr_submission_forum']},{submission_output_dict['num_reviews']},{submission_output_dict['num_metareviews']}, {submission_output_dict['is_latest_version']}, {submission_output_dict['was_migrated']}")


