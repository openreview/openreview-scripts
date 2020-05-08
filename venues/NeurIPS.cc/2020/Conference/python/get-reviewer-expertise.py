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
    parser.add_argument('reviewers', help="csv file path of NeurIPS reviewers")

    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    outfile = 'neurips20_email_status.csv'

    with open(args.reviewers, 'r') as f, open(outfile, 'w') as f2:
        csv_reader = csv.reader(f)
        next(csv_reader)
        map_email_to_details = {}
        for line in tqdm(csv_reader):
            email = line[2].strip().lower()
            map_email_to_details[email] = {
                'fname': line[0].strip(),
                'lname': line[1].strip()}
            role = line[3]
        map_profiles = client.search_profiles(emails=list(map_email_to_details.keys()))
        map_profiles_done = {}
        csv_writer = csv.writer(f2)
        csv_writer.writerow(['email', 'firstName', 'lastName', 'role', 'profile found', 'active', 'count of publications', 'dblp'])
        for email, content in tqdm(map_email_to_details.items()):
            profile = map_profiles.get(email)
            if profile:
                if profile.id in map_profiles_done:
                    print('Found repeated profile id {} with emails: {}, {}'.format(profile.id, map_profiles_done[profile.id], email))
                else:
                    map_profiles_done[profile.id] = email

            subs = get_publications(client, profile.id if profile else email)
            active_status = (True if profile.active and profile.password else False) if profile else False
            dblp_url = profile.content.get('dblp', '') if profile else ''
            csv_writer.writerow([email, content['fname'], content['lname'], role, True if profile else False, active_status, len(subs), dblp_url])
