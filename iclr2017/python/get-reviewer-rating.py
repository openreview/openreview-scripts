import argparse
import openreview
import csv
import requests

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ofile', help="output file name - default to status.csv")
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
## Initialize output file name
file_name = "review_rating.csv"
if args.ofile!=None:
    file_name = args.ofile

author_rate = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/Author/Review/Rating')
ac_rate = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/AC/Review/Rating')
headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + client.token}
anon_reviewers = requests.get(client.baseurl+'/groups?id=ICLR.cc/2017/conference/paper.*/AnonReviewer.*', headers = headers)

# reviewer_rating[paper_num][reviewer][type][name] = rating
reviewer_rating = {}
# fills in reviewer_rating, creating new sections as needed
def add_rating(reviewer_type, note):
    invite_str = '/' + str(reviewer_type) + '/Review/Rating'
    paper_num = int(note.invitation.split('paper')[1].split(invite_str)[0])
    reviewer = note.writers[0]
    if paper_num not in reviewer_rating:
        reviewer_rating[paper_num] = {}
    if reviewer not in reviewer_rating[paper_num]:
        reviewer_rating[paper_num][reviewer] = {}
    if reviewer_type not in reviewer_rating[paper_num][reviewer]:
        reviewer_rating[paper_num][reviewer][reviewer_type] = {}

    for key in note.content.keys():
        if key != 'title':
            rating = note.content[key].split('.')[0]
            ''' For now, ignore repeat review rating notes
            if key in reviewer_rating[paper_num][reviewer][reviewer_type]:
                print("Error double review")
                print('%s, %s, %s, %s,  %s' % (paper_num, reviewer, reviewer_type, rating, key))
                print('vs. %s' % reviewer_rating[paper_num][reviewer][reviewer_type][key])'''
            reviewer_rating[paper_num][reviewer][reviewer_type][key] = rating


# Author/Review/ratings
for note in author_rate:
    add_rating('Author', note)

# Area Chair reviews
for note in ac_rate:
    add_rating('AC', note)


################################################################
# Convert anonymous names/ email addresses to reviewer id's/names
################################################################

# profile_by_email[email_id] = ~name
profile_by_email = {}
def check_profile(member):

    if member.startswith('~'):
        return member

    if '@' in member:
        if member in profile_by_email:
            return profile_by_email[member]

        response = requests.get(client.baseurl+'/user/profile?email=' + member, headers = headers)
        if 'profile' not in response.json():
            profile_by_email[member] = member
            return member
        profile = response.json()['profile']
        profile_by_email[member] = profile['id']
        return profile_by_email[member]

    return member

# attach real name to the anonymized name for reviewers
reviewers = {}
for r in anon_reviewers.json():
    reviewer_id = r['id']
    members = r['members']
    if members:
        reviewers[reviewer_id] =check_profile(members[0])

################################################################
# End of anonymous name conversion
################################################################


# print results
# csv
with open(file_name, 'wb') as outfile:
    csvwriter = csv.writer(outfile, delimiter=',')
    row = []
    # paper ids, title, comment, recommendation, acceptance
    row.append("Paper ID")
    row.append("Author/AC Name")
    row.append("Rating Type")
    row.append("Reviewer Name")
    row.append("Rating")
    csvwriter.writerow(row)
    for paper_num in reviewer_rating:
        for reviewer in reviewer_rating[paper_num]:
            for reviewer_type in reviewer_rating[paper_num][reviewer]:
                for name in reviewer_rating[paper_num][reviewer][reviewer_type]:
                    author_id = ('ICLR.cc/2017/conference/paper%s/%s' % (paper_num, name))
                    row = []
                    row.append(paper_num)
                    row.append(reviewer.encode('utf-8'))
                    row.append(reviewer_type)
                    row.append(author_id.encode('utf-8'))
                    row.append(reviewer_rating[paper_num][reviewer][reviewer_type][name])
                    csvwriter.writerow(row)
