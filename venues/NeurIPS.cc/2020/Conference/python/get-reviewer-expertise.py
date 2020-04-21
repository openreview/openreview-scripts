import openreview
import argparse
import csv
from tqdm import tqdm

def get_publications(openreview_client, author_id):
    content = {
        'authorids': author_id
    }
    publications = openreview.tools.iterget_notes(openreview_client, content=content)
    return [publication for publication in publications]

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    infile = 'neurips20_program_committee_new.csv'
    outfile = 'neurips20_email_status.csv'

    with open(infile, 'r') as f, open(outfile, 'w') as f2:
        csv_reader = csv.reader(f)
        next(csv_reader)
        map_email_to_details = {}
        for line in tqdm(csv_reader):
            email = line[0].strip().lower()
            map_email_to_details[email] = {
                'fname': line[1].strip(),
                'lname': line[2].strip()}
        map_profiles = client.search_profiles(emails=list(map_email_to_details.keys()))
        map_profiles_done = {}
        csv_writer = csv.writer(f2)
        csv_writer.writerow(['email', 'firstName', 'lastName', 'profile found', 'active', 'count of publications'])
        for email, content in tqdm(map_email_to_details.items()):
            profile = map_profiles.get(email)
            if profile:
                if profile.id in map_profiles_done:
                    continue
                map_profiles_done[profile.id] = email
                
            subs = get_publications(client, profile.id if profile else email)
            active_status = (True if profile.active and profile.password else False) if profile else False
            csv_writer.writerow([email, content['fname'], content['lname'], True if profile else False, active_status, len(subs)])