
import openreview
import icml

def main(client):

    senior_areachairs_group = client.get_group(icml.SENIOR_AREA_CHAIRS_ID)

    for paper in client.get_notes(invitation='ICML.cc/2019/Conference/-/JrAC_Placeholder', details='tags'):
        score_by_signature = {t['signatures'][0]:icml.bid_score_map[t['tag']] for t in paper.details['tags'] if t['invitation'] == 'ICML.cc/2019/Conference/-/SAC_Bid'}
        posted_metadata = client.post_note(openreview.Note(**{
            'forum': paper.id,
            'replyto': paper.id,
            'invitation': icml.jrac_metadata_inv.id,
            'readers': [
                icml.CONFERENCE_ID,
            ],
            'writers': [icml.CONFERENCE_ID],
            'signatures': [icml.CONFERENCE_ID],
            'content': {
                'entries': [{
                    'scores': {'bid': score_by_signature.get(userid, 0.0)},
                    'userid': userid,
                    'conflicts': [True] if score_by_signature.get(userid, 0.0) < 0.0 else []
                } for userid in senior_areachairs_group.members]
            }
        }))

    sac_config_note = openreview.Note(**{
        'id': None,
        'content': {
            'label': 'sac-ac-test',
            'max_users': '1',
            'min_users': '1',
            'max_papers': '8',
            'min_papers': '5',
            'alternates': '0',
            'config_invitation': 'ICML.cc/2019/Conference/-/Assignment_Configuration',
            'paper_invitation': 'ICML.cc/2019/Conference/-/JrAC_Placeholder',
            'metadata_invitation': 'ICML.cc/2019/Conference/-/JrAC_Metadata',
            'assignment_invitation': 'ICML.cc/2019/Conference/-/Paper_Assignment',
            'constraints_invitation': 'ICML.cc/2019/Conference/-/Assignment_Configuration/Lock',
            'match_group': 'ICML.cc/2019/Conference/Senior_Area_Chairs',
            'scores_names': ['bid'],
            'scores_weights': ['1'],
            'status': 'Initialized'
        },
        'invitation': 'ICML.cc/2019/Conference/-/Assignment_Configuration',
        'replyto': None,
        'readers': [
            'ICML.cc/2019/Conference',
            'ICML.cc/2019/Conference/Area_Chairs'
        ],
        'nonreaders': [],
        'signatures': ['ICML.cc/2019/Conference'],
        'writers': ['ICML.cc/2019/Conference']
    })

    client.post_note(sac_config_note)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--processed_files_dir', default='../data/icml-sheets-processed')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print('connecting to {} with username {}'.format(client.baseurl, client.username))

    main(client)
