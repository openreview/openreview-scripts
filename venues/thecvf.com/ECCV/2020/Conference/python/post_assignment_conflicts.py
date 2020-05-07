import openreview
import csv
from tqdm import tqdm
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    map_submissions = {note.number: note for note in openreview.tools.iterget_notes(
        client,
        invitation = 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}
    
    # Create a map of paper reviewer groups to group members
    conflicts = []
    
    reviewer_groups = list(openreview.tools.iterget_groups(client, regex='thecvf.com/ECCV/2020/Conference/Paper.*/AnonReviewer[0-9]*$'))
    print('Found {} anonymous reviewer groups'.format(len(reviewer_groups)))

    for grp in reviewer_groups:
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions and grp.members:
            conflicts.append(openreview.Edge(
                head=map_submissions[paper_num].id,
                tail=grp.members[0],
                invitation='thecvf.com/ECCV/2020/Conference/Reviewers/-/Conflict',
                readers=[
                    'thecvf.com/ECCV/2020/Conference',
                    'thecvf.com/ECCV/2020/Conference/Area_Chairs'
                ],
                writers=['thecvf.com/ECCV/2020/Conference'],
                signatures=['thecvf.com/ECCV/2020/Conference'],
                weight=-1,
                label='Already Assigned'
            ))

    print ('thecvf.com/ECCV/2020/Conference/Reviewers/-/Conflict: Posting {0} edges'.format(len(conflicts)))
    posted_edges = openreview.tools.post_bulk_edges(client, conflicts)
    print ('thecvf.com/ECCV/2020/Conference/Reviewers/-/Conflict: Posted {0} edges'.format(len(posted_edges)))

    conference = openreview.helpers.get_conference(
        client, 
        request_form_id='Skx6tVahYB')
    
    conference.setup_matching(delete_existing_conflicts=False)
