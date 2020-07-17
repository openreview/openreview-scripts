import argparse
import openreview
from tqdm import tqdm
import os
import requests
import urllib.request

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
    parser.add_argument('submission_numbers_file', help='Provide the submission file\'s absolute address')
    args = parser.parse_args()

    if not os.path.exists(args.submission_numbers_file):
        raise Exception('Input file "{}" does not exist'.format(args.submission_numbers_file))

    root_dir = os.path.dirname(args.submission_numbers_file)
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    with open(args.submission_numbers_file, 'r') as f:
        sub_nums = [num.strip() for num in f.read().split('\n') if num]
    
    sub_nums = set(sub_nums)
    for sub_num in tqdm(sub_nums):
        sub_num_padded = sub_num.rjust(4, '0')

        paper_dir = os.path.join(root_dir, sub_num_padded)
        if not os.path.exists(paper_dir):
            os.mkdir(os.path.join(root_dir, sub_num_padded))
        
        submission = client.get_notes(
            invitation='thecvf.com/ECCV/2020/Conference/-/Submission',
            number=int(sub_num))[0]

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
        else:
            print('{} has no source'.format(sub_num))

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
        else:
            print('{} has no supplementary_material'.format(sub_num))

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
        else:
            print('{} has no copyright'.format(sub_num))
