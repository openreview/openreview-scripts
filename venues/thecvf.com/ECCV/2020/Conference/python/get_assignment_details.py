import openreview
import argparse
import csv
import json
from tqdm import tqdm
from collections import defaultdict

def write_assignments(client, submissions_map, user_type='reviewers'):
    outfile = 'reviewer_alloc.json' if user_type.lower() == 'reviewers' else 'areachair_alloc.json'
    regex = 'thecvf.com/ECCV/2020/Conference/Paper[0-9]*/' + ('AnonReviewer[0-9]*' if user_type.lower() == 'reviewers' else 'Area_Chair1' ) + '$'

    user_grps = list(openreview.tools.iterget_groups(client=client, regex=regex))
    print('Found {} user groups for regex {}'.format(len(user_grps), regex))

    map_member_to_anon = defaultdict(list)
    for grp in tqdm(user_grps):
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        paper_note = submissions_map.get(paper_num)
        if paper_note and grp.members:
            map_member_to_anon[grp.members[0]].append({ 'paper_number': paper_num, 'paper_id': paper_note.id, 'anon_group_id': grp.id})

    with open(outfile, 'w') as f:
        json.dump(map_member_to_anon, f)
        # csv_writer = csv.writer(f)
        # csv_writer.writerow(['Reviewer ID', '# of papers assigned', 'assigned paper numbers,ids'])
        # for user, papers in map_member_to_anon.items():
        #     row = [user, len(papers)]
        #     row.extend(papers)
        #     csv_writer.writerow(row)

    print ('Finished writing {}'.format(outfile))

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    submissions_map = {note.number: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}
    print('Found {} submissions'.format(len(submissions_map)))

    write_assignments(client, submissions_map, user_type='Reviewers')

    write_assignments(client, submissions_map, user_type='Area_Chairs')
