import openreview
import csv
from tqdm import tqdm

baseurl = 'http://localhost:3000'
username = 'user'
password = 'password'
group_id = 'thecvf.com/ECCV/2020/Conference/Area_Chairs'
submission_invitation = 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'
scores_a_name = 'TPMS'
scores_b_name = 'ELMo'
scores_a_path = '/Users/cmondragonch/Desktop/tpms_scores_acs.csv'
scores_b_path = '/Users/cmondragonch/Desktop/elmo_scores/eccv_elmo_acs.csv'
weight_a = 0.8
weight_b = 0.2
combined_scores_path = '/Users/cmondragonch/Desktop/combined_scores_acs.csv'

client = openreview.Client(baseurl=baseurl, username=username, password=password)

def get_profile_ids(client, group_id):
    print('Getting Profile ids...')
    tilde_members = []
    group = client.get_group(group_id)
    profile_members = [member for member in group.members if '~' in member]
    email_members = [member for member in group.members if '@' in member]
    profile_search_results = client.search_profiles(emails=email_members, ids=None, term=None)

    if profile_members:
        tilde_members.extend(profile_members)
    if profile_search_results and type(profile_search_results) == dict:
        tilde_members.extend([p.id for p in profile_search_results.values()])

    return set(tilde_members)

def get_submission_ids(client, invitation_id):
    submission_ids = set()

    submissions = openreview.tools.iterget_notes(client, invitation=invitation_id)

    for submission in tqdm(submissions, desc='Getting Submission Ids'):
        submission_ids.add(submission.id)

    return submission_ids

members = get_profile_ids(client, group_id)
note_ids = get_submission_ids(client, submission_invitation)

def load_csv(csv_scores_path):
    all_scores = {}
    note_ids = set()
    profile_ids = set()
    with open(csv_scores_path, 'r') as f:
        content = csv.reader(f)
        for row in tqdm(content, desc='Loading csv...'):
            note_ids.add(row[0])
            profile_ids.add(row[1])
            all_scores[(row[0], row[1])] = row[2]
    return all_scores, note_ids, profile_ids

scores_a, note_ids_a, members_a = load_csv(scores_a_path)
scores_b, note_ids_b, members_b = load_csv(scores_b_path)

def combine_scores(score_a, weight_a, score_b, weight_b):
    if score_a is None and score_b is None:
        return 0.0
    if score_a is None:
        return float(score_b) * (weight_a + weight_b)
    if score_b is None:
        return float(score_a) * (weight_a + weight_b)
    return float(score_a) * weight_a + float(score_b) * weight_b

def set_missing(score_a, score_b, note_id, profile_id, missing):
    if score_a is None and score_b is None:
        missing['expertise'].add((note_id, profile_id))
    elif score_a is None:
        missing[scores_a_name].add((note_id, profile_id))
    elif score_b is None:
        missing[scores_b_name].add((note_id, profile_id))

combined_scores = []
missing = {
    'expertise': [],
    scores_a_name: [],
    scores_b_name: []
}

for member in members:
    if member not in members_a and member not in members_b:
        missing['expertise'].append(member)
    elif member not in members_a:
        missing[scores_a_name].append(member)
    elif member not in members_b:
        missing[scores_b_name].append(member)

for note_id in tqdm(note_ids, total=len(note_ids), desc='Combining Scores'):
    for member in members:
        score_a = scores_a.get((note_id, member))
        score_b = scores_b.get((note_id, member))
        combined_score = combine_scores(score_a, weight_a, score_b, weight_b)
        combined_scores.append((note_id, member, combined_score))

print(scores_a_name, missing[scores_a_name], '\n', scores_b_name, missing[scores_b_name])

with open(combined_scores_path, 'w') as f:
    for note_id, profile_id, score in combined_scores:
        f.write('{0},{1},{2}\n'.format(note_id, profile_id, score))
