import argparse
import re
import csv
import openreview
from tqdm import tqdm
from openreview import tools

parser = argparse.ArgumentParser()
parser.add_argument('assignments_file', help='csv file')
parser.add_argument('--baseurl', help='base url')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

conference = openreview.helpers.get_conference(client, '6tlp9iYQvsy')

papers = conference.get_submissions()

revs_by_title = {}
clincial_revs_by_title = {}
acs_by_title = {}

with open(args.assignmnents_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    next(csv_reader, None)

    for row in csv_reader:
        title = row[0]
        rev1 = row[2]
        rev2 = row[3]
        clincal_rev = row[4]
        ac = row[5]
        revs_by_title[title] = [rev1,rev2]
        clincial_revs_by_title[title] = clincal_rev
        acs_by_title[title] = ac

def get_readers(num):
    readers = [
        conference.get_id(),
        conference.get_program_chairs_id(),
        conference.get_area_chairs_id(number = num)
    ]
    return readers

for paper in papers:
    num = paper.number
    revs = revs_by_title[paper.content['title']]
    readers = get_readers(num)
    invitees = ['OpenReview.net/Support']
    for rev in revs:
        user, groups = tools.add_assignment(client, num, conference.get_id(), rev,
                            parent_label = 'Reviewers',
                            individual_label = 'AnonReviewer',
                            individual_group_params = {
                                'readers': readers,
                                'writers': readers
                            },
                            parent_group_params = {
                                'readers': readers,
                                'writers': readers
                            })
        
        r = re.compile('MICCAI.org/2021/Challenges/Paper.*/AnonReviewer.*')
        anongroup = list(filter(r.match, groups))[0]
        invitees.append(anongroup)

    #set only these reviewers as invitees of review invitation
    rev_invitation = client.get_invitation('MICCAI.org/2021/Challenges/Paper{}/-/Official_Review'.format(num))
    rev_invitation.invitees = invitees

    clinical_rev = clincial_revs_by_title[paper.content['title']]
    user, groups = tools.add_assignment(client, num, conference.get_id(), clinical_rev,
                            parent_label = 'Reviewers',
                            individual_label = 'AnonReviewer',
                            individual_group_params = {
                                'readers': readers,
                                'writers': readers
                            },
                            parent_group_params = {
                                'readers': readers,
                                'writers': readers
                            })
    
    r = re.compile('MICCAI.org/2021/Challenges/Paper.*/AnonReviewer.*')
    anongroup = list(filter(r.match, groups))[0]
    
    #set only this reviewer as invitee of clinical review invitation
    clinical_rev_invitation = client.get_invitation('MICCAI.org/2021/Challenges/Paper{}/-/Clinical_Review'.format(num))
    clinical_rev_invitation.invitees = [anongroup, 'OpenReview.net/Support']
    
    ac = acs_by_title[paper.content['title']]
    tools.add_assignment(client, num, conference.get_id(), ac, parent_label = 'Area_Chairs', individual_label = 'Area_Chair')