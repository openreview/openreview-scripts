import openreview
import argparse
import csv
from tqdm import tqdm

def get_pref_email(profile):
    if not profile:
        return None
    pref_email = profile.content.get('preferredEmail')
    if pref_email:
        return pref_email
    confirmed_emails = profile.content.get('emailsConfirmed')
    if confirmed_emails:
        return confirmed_emails[0]
    emails = profile.content.get('emails')
    return emails[0]

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    submissions_map = {note.number: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}
    
    author_groups = openreview.tools.iterget_groups(client, regex='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/Authors$')
    
    paper_author_map = {}
    for grp in author_groups:
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        if grp.members:
            paper_author_map[paper_num] = grp.members

    with open('author_contacts.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Paper Number', 'Paper ID', 'Author Emails'])
        for num, sub in tqdm(sorted(submissions_map.items(), key=lambda x: x)):
            profiles = client.search_profiles(ids=paper_author_map[num])
            paper_emails = [get_pref_email(profile) for profile in profiles]
            row = [num, sub.id]
            row.extend(paper_emails)
            csv_writer.writerow(row)
    
    print ('Finished writing')