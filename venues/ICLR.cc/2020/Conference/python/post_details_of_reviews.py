import openreview
import argparse
import csv

from tqdm import tqdm

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference_id = 'ICLR.cc/2020/Conference'

    map_number_to_blind_notes = {str(note.number): note for note in openreview.tools.iterget_notes(client, invitation=conference_id+'/-/Blind_Submission')}
    print ('{0} papers found'.format(len(map_number_to_blind_notes)))

    with open('sorted_by_calibrated_nonlinear_scores.csv', 'r') as f:
        csv_lines = csv.DictReader(f)
        for line in tqdm(csv_lines):
            paper_number = line['paper id']
            if paper_number in map_number_to_blind_notes:
                comment_text = ''

                for header, value in line.items():
                    comment_text += '{curr_header} : {curr_value} \n'.format(curr_header = header, curr_value = value) if header != '' else '\n'

                comment = openreview.Note(
                    invitation = conference_id + '/Paper{0}/-/Official_Comment'.format(paper_number),
                    forum = map_number_to_blind_notes[paper_number].id,
                    replyto = map_number_to_blind_notes[paper_number].id,
                    readers = [conference_id + '/Program_Chairs', conference_id + '/Paper{}/Area_Chairs'.format(paper_number)],
                    writers = [conference_id + '/Program_Chairs'],
                    signatures = [conference_id + '/Program_Chairs'],
                    content = {
                        'title': 'Calibrated Review Score details for Paper {0}'.format(paper_number),
                        'comment': comment_text
                    }
                )
                posted_comment = client.post_note(comment)