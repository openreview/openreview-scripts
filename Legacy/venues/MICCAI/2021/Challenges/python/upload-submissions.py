import argparse
import re
import csv
import openreview
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('miccai_papers', help='csv file')
parser.add_argument('--pdfs_filepath', help='filepath to directory with pdfs')
parser.add_argument('--baseurl', help='base url')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference_id = 'MICCAI.org/2021/Challenges'

submission_invitation = client.get_invitation('MICCAI.org/2021/Challenges/-/Submission')

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

failed_papers = []
count=0
with open(args.miccai_papers) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    next(csv_reader, None)

    for row in csv_reader:
        
        pdf_link = client.put_attachment(args.pdfs_filepath+'/'+row[4], 'MICCAI.org/2021/Challenges/-/Submission', 'pdf')
        authors = [author.strip() for author in row[2].split(',')]
        authorids = [authorid.strip() for authorid in row[3].split(',')]

        miccai_paper = openreview.Note(
            invitation=conference_id+'/-/Submission',
            signatures=[conference_id],
            writers=[conference_id, conference_id+'/Program_Chairs'],
            readers=['everyone'],
            content={
                'title': row[0],
                'authors': authors,
                'authorids': authorids,
                'abstract': row[1],
                'venue': 'MICCAI 2021 Challenge Report', 
                'venueid': 'MICCAI.org/2021/Challenges',
                'pdf': pdf_link
            }
        )

        try:
            posted_paper = client.post_note(miccai_paper)
            print('Posted paper', posted_paper.forum)
            count+=1
        except openreview.OpenReviewException as e:
            print(e)

print(failed_papers)
print('Posted papers: ', count)