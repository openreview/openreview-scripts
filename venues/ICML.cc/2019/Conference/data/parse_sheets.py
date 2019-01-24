import sys, os
import csv, json
import argparse
import openreview

sys.path.insert(0, '../python')
import icml

def process_reviewers(reviewer_data):
    reviewer_ids = set()
    expert_reviewer_ids = set()

    for first, m_i, last, email, org, country, conflicts, is_expert in reviewer_data:
        reviewer_id = '~{}_{}1'.format(first.replace(' ', '_'), last.replace(' ', '_'))

        if 'TRUE' in is_expert:
            reviewer_ids.add(reviewer_id)
        elif 'FALSE' in is_expert:
            expert_reviewer_ids.add(reviewer_id)
        else:
            print('invalid value for {}{}: {}'.format(first, last, is_expert))

    return sorted(list(reviewer_ids)), sorted(list(expert_reviewer_ids))

def process_jr_areachairs(areachair_data):
    areachair_ids = set()

    for first, m_i, last, email, org, country, conflicts in areachair_data:
        ac_id = '~{}_{}1'.format(first.replace(' ', '_'), last.replace(' ', '_'))
        areachair_ids.add(ac_id)

    return sorted(list(areachair_ids))


def process_senior_areachairs(senior_areachair_data):
    senior_areachair_ids = set()

    for first, m_i, last, email, org, country, conflicts in senior_areachair_data:
        senior_areachair_ids.add('~{}_{}1'.format(first.replace(' ', '_'), last.replace(' ', '_')))

    return sorted(list(senior_areachair_ids))

def process_sac_ac_bids(sac_ac_bids, sorted_sac_ids):
    sac_ac_bids = sac_ac_bids[1:]
    bid_map = {
        '1': '1 - Not Willing',
        '2': '2 - Neutral',
        '3': '3 - Willing',
        '4': '4 - Eager'
    }

    bids = []

    for row in sac_ac_bids:
        first, last, org, interest = row[:4]
        jrac_id = '~{}_{}1'.format(first.replace(' ', '_'), last.replace(' ', '_'))

        ordered_bids = row[4:]
        assert len(ordered_bids) == len(sorted_sac_ids)

        for bid, sac_id in zip(ordered_bids, sorted_sac_ids):
            if bid and bid in bid_map:
                bids.append({
                    'jrac_id': jrac_id,
                    'tag': bid_map[bid],
                    'signatures': [sac_id],
                    'readers': [icml.CONFERENCE_ID]
                })

    return bids

def main(output_dir, reviewers, areachairs, sr_areachairs, reviewer_quotas, sac_ac_bids):
    reviewer_ids, expert_reviewer_ids = process_reviewers(reviewers)

    with open(os.path.join(output_dir, 'reviewers.csv'), 'w') as f:
        writer = csv.writer(f)
        for reviewer_id in reviewer_ids:
            writer.writerow([reviewer_id])

    with open(os.path.join(output_dir, 'expert_reviewers.csv'), 'w') as f:
        writer = csv.writer(f)
        for expert_reviewer_id in expert_reviewer_ids:
            writer.writerow([expert_reviewer_id])

    areachair_ids = process_jr_areachairs(areachairs)
    with open(os.path.join(output_dir, 'areachairs.csv'), 'w') as f:
        writer = csv.writer(f)
        for areachair_id in areachair_ids:
            writer.writerow([areachair_id])

    sorted_sac_ids = process_senior_areachairs(sr_areachairs)
    with open(os.path.join(output_dir, 'senior_areachairs.csv'), 'w') as f:
        writer = csv.writer(f)
        for senior_areachair_id in sorted_sac_ids:
            writer.writerow([senior_areachair_id])

    bid_jsons = process_sac_ac_bids(sac_ac_bids, sorted_sac_ids)
    with open(os.path.join(output_dir, 'sac_ac_bids.jsonl'), 'w') as f:
        for bid_json in bid_jsons:
            f.write(json.dumps(bid_json) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sheets_dir', help="base url", default='./icml-sheets')
    parser.add_argument('--output_dir', help="base url", default='./icml-sheets-processed')
    args = parser.parse_args()

    data = {}

    for file in os.listdir(args.sheets_dir):
        full_file = os.path.join(args.sheets_dir, file)
        with open(full_file) as f:
            reader = csv.reader(f)
            reader.__next__() # drop the column headers

            filename = file.replace('.csv', '')
            data[filename] = [row for row in reader]

    print(data.keys())

    main(args.output_dir, **data)
