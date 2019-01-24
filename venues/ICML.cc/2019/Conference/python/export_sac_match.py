import openreview
import icml
import os
import argparse
import json, csv
from collections import defaultdict

def id_to_name(id):
	return id.replace('~', '').replace('1', '').replace('_', ' ')

def main(client):
	csv_rows = []

	jrac_placeholders = client.get_notes(invitation='ICML.cc/2019/Conference/-/JrAC_Placeholder')
	jrac_by_forum = {n.forum: n.content['title'] for n in jrac_placeholders}

	for assignment in openreview.tools.iterget_notes(client, invitation='ICML.cc/2019/Conference/-/Paper_Assignment'):
		assigned_groups = assignment.content['assignedGroups']
		assert len(assigned_groups) == 1, 'too many assigned groups'
		assignment_entry = assigned_groups[0]

		score = assignment_entry['scores']['bid']
		bid = icml.bids_by_score[score]
		srac_id = assignment_entry['userId']
		jrac_id = jrac_by_forum[assignment.forum]

		current_row = [id_to_name(srac_id), id_to_name(jrac_id), bid]
		csv_rows.append(current_row)

	return sorted(csv_rows, key=lambda x: x[0])



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', default='../data/exports')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print('connecting to {} with username {}'.format(client.baseurl, client.username))

    rows = main(client)

    with open(os.path.join(args.output_dir, 'sac_ac_match.csv'), 'w') as f:
    	writer = csv.writer(f)
    	for row in rows:
    		writer.writerow(row)

