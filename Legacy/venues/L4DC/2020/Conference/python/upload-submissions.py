import argparse
import re
import csv
import openreview
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('l4dc_papers', help='csv file')
parser.add_argument('--pdfs_filepath', help='filepath to directory with pdfs')
parser.add_argument('--author_details', help='file with author names and emails')
parser.add_argument('--baseurl', help='base url')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference_id = 'L4DC.org/2020/Conference'

submission_invitation = client.get_invitation('L4DC.org/2020/Conference/-/Submission')

submission_invitation.reply['readers'] = {
    'values': ['everyone']
    }
submission_invitation.reply['signatures'] =  {
    'values': [conference_id]
    }
submission_invitation.reply['writers'] = {
    'values': [conference_id, conference_id+'/Program_Chairs']
}
client.post_invitation(submission_invitation)

#Dictionary to match authors to emails from author_details.csv
author_to_email = {}

with open(args.author_details) as csv_file1:
    csv_reader1 = csv.reader(csv_file1, delimiter = ',')
    next(csv_reader1, None)
    
    for row in csv_reader1:
        title = row[1]
        name = row[2]+' '+row[3]
        email = row[4].lower()
        author_to_email[(name, title)] = email

failed_papers = []
with open(args.l4dc_papers) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    next(csv_reader, None)

    for row in csv_reader:
        
        pdf_link = client.put_attachment(args.pdfs_filepath+'/'+row[2], 'L4DC.org/2020/Conference/-/Submission', 'pdf')
        authors = [author.strip() for author in row[0].replace(' and ', ', ').split(',')]
        try:
            authorids = [author_to_email[(author, row[1])] for author in authors]
        except:
            failed_papers.append(row[1])
            continue

        l4dc_paper = openreview.Note(
            invitation=conference_id+'/-/Submission',
            signatures=[conference_id],
            writers=[conference_id, conference_id+'/Program_Chairs'],
            readers=['everyone'],
            content={
                'title': row[1],
                'authors': authors,
                'authorids': authorids,
                'abstract': row[3],
                'venue': 'L4DC 2020', 
                'venueid': 'L4DC.org/2020/Conference',
                'pdf': pdf_link
            }
        )

        try:
            posted_paper = client.post_note(l4dc_paper)
            print('Posted paper', posted_paper.forum)
        except openreview.OpenReviewException as e:
            print(e)

print(failed_papers)

