import argparse
import openreview
from tqdm import tqdm
import os
import requests
import urllib.request
import concurrent.futures
import datetime

def download_files(paper_num):
    sub_num_padded = str(paper_num).rjust(4, '0')

    paper_dir = os.path.join(root_dir, sub_num_padded)
    if not os.path.exists(paper_dir):
        os.mkdir(paper_dir)

    submission = map_submissions[paper_num]
    author_names = submission.content['authors']
    author_profiles = [client.search_profiles(ids=[authorid])[0] for authorid in submission.content['authorids']]
    author_emails = [get_pref_email(profile) for profile in author_profiles]
    final_title = submission.content['title']

    with open(os.path.join(paper_dir, sub_num_padded+'-info.csv'), 'w') as f:
        f.write('title:' + final_title + '\n')
        f.write('\n'.join(['{}, {}'.format(name, email) for name, email in zip(author_names, author_emails)]))

    headers_copy = client.headers.copy()

    if 'source' in submission.content:
        response = requests.get(
            client.baseurl + '/attachment',
            params={
                'id': submission.id,
                'name': 'source'
            },
            headers=headers_copy)
        
        source_content = response.content
        with open(os.path.join(paper_dir, sub_num_padded+'.zip'), 'wb') as f:
            f.write(source_content)

    if 'supplementary_material' in submission.content:
        pdf = submission.content['supplementary_material'].endswith('pdf')
        
        supp_path = os.path.join(paper_dir, sub_num_padded+'-supp.zip')
        if pdf:
            supp_path = supp_path = os.path.join(paper_dir, sub_num_padded+'-supp.pdf')
    
        response = requests.get(
            client.baseurl + '/attachment',
            params={
                'id': submission.id,
                'name': 'supplementary_material'
            },
            headers=headers_copy)
        source_content = response.content
        with open(supp_path, 'wb') as f:
            f.write(source_content)

    if 'copyright' in submission.content:
        headers_copy['content-type'] = 'application/pdf'
        response = requests.get(
            client.baseurl + '/attachment',
            params={
                'id': submission.id,
                'name': 'copyright'
            },
            headers=headers_copy)
        source_content = response.content
        with open(os.path.join(paper_dir, sub_num_padded+'-copyright.pdf'), 'wb') as f:
            f.write(source_content)

def get_pref_email(profile):
    pref_email = profile.content.get('preferredEmail', None)
    if not pref_email:
        pref_email = profile.content['emailsConfirmed'][0]
    return pref_email

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    root_dir = '/Users/mohituniyal/Desktop/eccv_paper'
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    start = datetime.datetime.utcnow()

    print('Fetching all submissions')
    map_submissions = {note.number: note for note in openreview.tools.iterget_notes(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/-/Submission')}
    print('Found {} submissions'.format(len(map_submissions)))

    print('Fetching decision notes')
    map_decision_notes = {int(note.invitation.split('Paper')[1].split('/')[0]): note for note in openreview.tools.iterget_notes(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/-/Decision$'
    ) if note.content['decision'].startswith('Accept')}
    print('Found {} accept decisions'.format(len(map_decision_notes)))


    print('Downloading files')
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {
            executor.submit(download_files, paper_num): paper_num for paper_num in map_decision_notes
            }

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))

    end = datetime.datetime.utcnow()
    print('Done', (end - start).total_seconds(), 'seconds')