import argparse
import re
import csv
import openreview
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('neurips_papers')
parser.add_argument('--baseurl', help='base url')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference_id = 'NeurIPS.cc/2019/Reproducibility_Challenge'

existing_papers_by_title = {
    note.content['title']: note for note in openreview.tools.iterget_notes(
    client, invitation=conference_id+'/-/NeurIPS_Submission')
}

accepted_info = []
org_pattern = pattern = '\(.*\)'

with open(args.neurips_papers) as f:
    reader = csv.reader(f)

    headers = next(reader)
    # Paper Title, Abstract, Authors (Organization), Author Names, Primary Contact
    for paper_title, abstract, authors_and_orgs, author_names, primary_contact in reader:
        authors_list = [re.sub(org_pattern, '', author).strip() for author in authors_and_orgs.split(';')]

        paper_info = {
            'title': paper_title,
            'abstract': abstract,
            'authors': authors_list,
            'authorids': [
                primary_contact.replace('*','').strip() if '*' in name else '' \
                for name in authors_list
            ]
        }
        accepted_info.append(paper_info)

post_count = 0
for info in tqdm(accepted_info):
    title = info['title']

    neurips_paper = openreview.Note(
        invitation=conference_id+'/-/NeurIPS_Submission',
        signatures=[conference_id+'/Program_Chairs'],
        writers=[conference_id, conference_id+'/Program_Chairs'],
        readers=['everyone'],
        content={
            'title': title,
            'authors': info['authors'],
            'authorids': info['authorids'],
            'abstract': info['abstract'],
            'venue': 'NeurIPS 2019'
        }
    )

    if title in existing_papers_by_title:
        neurips_paper.id = existing_papers_by_title[title].id

    try:
        posted_note = client.post_note(neurips_paper)

        if posted_note:
            post_count += 1
    except openreview.OpenReviewException as e:
        print(e)

print(post_count)
