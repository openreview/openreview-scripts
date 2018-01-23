#!/usr/bin/python

"""
Dump csv file of meta-review information to make final decision.
"""
import argparse
import openreview
import csv

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ofile', help="output file name - default to status.csv")
args = parser.parse_args()

def init_paper_info(client):
    print "loading submissions"
    submissions = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
    paper_info={}
    for n in submissions:
        paper_info[n.number] = {}
        paper_info[n.number]['title'] = n.content['title']
        paper_info[n.number]['AC_rec'] = ""
        paper_info[n.number]['AC_conf'] = ""
        paper_info[n.number]['AC_meta'] = ""
        paper_info[n.number]['AC_name'] = ""
        paper_info[n.number]['ave_score'] = 0
        paper_info[n.number]['reviews'] = []
        paper_info[n.number]['num_review'] = 0
    return paper_info

def get_activity(client, paper_info):
    # load in all notes from conference
    print "loading official reviews"
    limit = 1000
    offset = 0
    notes = []
    batch = client.get_notes(invitation="ICLR.cc/2018/Conference/-/.*/Official_Review", limit=limit, offset=offset)
    notes += batch
    while len(batch) == limit:
        offset += limit
        batch = client.get_notes(invitation="ICLR.cc/2018/Conference/-/.*/Official_Review", limit=limit, offset=offset)
        notes += batch
    # grab necessary data from notes
    for n in notes:
        paper_number = int(n.invitation.split('Paper')[1].split('/')[0])
        if paper_number in paper_info:
            # add review data
            paper_info[paper_number]['num_review'] += 1
            paper_info[paper_number]['reviews'].append({'rating': n.content['rating'].split(':')[0],
                                                        'conf': n.content['confidence'].split(':')[0]})


    print "loading meta reviews"
    offset = 0
    notes = client.get_notes(invitation="ICLR.cc/2018/Conference/-/.*/Meta_Review", limit=limit, offset=offset)

    profile_info = {}
    # grab necessary data from notes
    for n in notes:
        paper_number = int(n.invitation.split('Paper')[1].split('/')[0])
        if paper_number in paper_info:
            #fill in meta data
            paper_info[paper_number]['AC_rec'] = n.content['recommendation']
            paper_info[paper_number]['AC_conf'] = n.content['confidence'].split(':')[0]
            paper_info[paper_number]['AC_meta'] = n.content['metareview']
            if n.tauthor in profile_info:
                paper_info[paper_number]['AC_name'] = profile_info[n.tauthor]
            else:
                profile = client.get_profile(n.tauthor)
                profile_info[n.tauthor]=profile.id
                paper_info[paper_number]['AC_name'] = profile.id

    # get the AC name if the Meta_Review hasn't been submitted
    for n in paper_info:
        if paper_info[n]['AC_name'] == "":
            group = client.get_group("ICLR.cc/2018/Conference/Paper{0}/Area_Chair".format(n))
            if len(group.members) > 0:
                paper_info[n]['AC_name'] = group.members[0]

    return paper_info


# output all information needed to make a final decision on a paper
def output_paper_info(file_name, paper_info):
    print "writing to file "+file_name
    with open(file_name, 'wb') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')
        row = ['Paper ID', 'Paper title', 'AC recommendation', 'AC confidence', 'Ave review scores', 'Reviewer scores',
               'Reviewer Confidence', 'AC MetaReview', 'AC name','DONE?', 'PC decision', 'PC notes', 'PC Metareview']
        csvwriter.writerow(row)

        for n in paper_info:
            row = []
            row.append(n)
            row.append(paper_info[n]['title'].encode('utf-8'))
            row.append(paper_info[n]['AC_rec'])
            row.append(paper_info[n]['AC_conf'])

            # average review score
            score = 0.0
            if paper_info[n]['num_review'] > 0:
                for rev in paper_info[n]['reviews']:
                    score += int(rev['rating'])
                score = score / paper_info[n]['num_review']
            row.append('%.2f' % score)

            # reviewer ratings and confidence
            rating = ""
            conf = ""
            for rev in paper_info[n]['reviews']:
                rating = rating+str(rev['rating'])+';'
                conf = conf + str(rev['conf']) + ';'
            row.append(rating[:-1])
            row.append(conf[:-1])

            row.append(paper_info[n]['AC_meta'].encode('utf-8'))
            row.append(paper_info[n]['AC_name'].encode('utf-8'))
            csvwriter.writerow(row)


def main():
    ## Initialize the client library with username and password
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    paper_info = init_paper_info(client)
    paper_info = get_activity(client, paper_info)

    ## Initialize output file name
    file_name = "acceptances.csv"
    if args.ofile!=None:
        file_name = args.ofile
    output_paper_info(file_name, paper_info)

if __name__ == "__main__":
    main()
