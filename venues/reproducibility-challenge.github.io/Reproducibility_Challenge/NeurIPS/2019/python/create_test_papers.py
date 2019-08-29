import argparse
import openreview

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

conference_id = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'

client = openreview.Client()

neurips_papers = client.get_notes(invitation='dblp.org/-/record', content={'venueid': 'dblp.org/conf/NIPS/2018'})

accepted_info = [{'title': n.content['title'], 'abstract': n.content['abstract'], 'authors': n.content['authors']} for n in neurips_papers if 'abstract' in n.content]

post_count = 0
for info in accepted_info:
    try:
        posted_note = client.post_note(openreview.Note(
            id=None,
            original=None,
            invitation=conference_id+"/-/NeurIPS_Submission",
            forum=None,
            signatures=[conference_id+"/Program_Chairs"],
            writers=[conference_id],
            readers=['everyone'],
            content={
                "title": info['title'],
                "authors": info['authors'],
                "abstract": info['abstract']
            }
        ))
        if posted_note:
            post_count += 1

    except openreview.OpenReviewException:
        pass

    if post_count >= 100:
        break

