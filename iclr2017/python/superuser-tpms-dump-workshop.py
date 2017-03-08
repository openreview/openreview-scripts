import openreview
import re
import unicodecsv as csv
import os
import requests
import argparse

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('outdir', help='output file path')
parser.add_argument('outfilename',help='the csv filename to write the dump to. will appear in /outdir')
parser.add_argument('group',help='the group to dump')
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)

outputdir = args.outdir

def get_profiles(groupname):
    members = client.get_group(groupname).members

    p = re.compile('~.*')

    canonical_ids = []
    missing_users = []
    for m in members:
        m = m.strip()
        try:
            client.get_group(m)
            g = client.get_group(m)
            groupmembers = [member for member in g.members if p.match(member)]

            if len(groupmembers) ==0:
                print "No canonical IDs found for member ",m
                missing_users.append(m)
            else:
                if len(groupmembers) > 1:
                    print "More than one canonical ID found for member ",m,"; Using first ID in the list."

                tildeId = groupmembers[0]
                canonical_ids.append(tildeId)

        except openreview.OpenReviewException as e:
            missing_users.append(m)
            print e

    profiles = []

    for id in canonical_ids:
        profiles.append(client.get_note(id).to_json())

    return profiles,missing_users


def dump_names(profiles,outfilename):
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    with open(outputdir+'/'+outfilename,'wb') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')
        for profile in profiles:
            p = profile['content']
            name = p['names'][0]
            firstname = name['first']
            lastname = name['last']
            email = p['emails'][0]
            csvwriter.writerow([email,firstname,lastname])

def write_pdfs(papers):
    p = re.compile('.*arxiv\.org\/pdf')
    for s in papers:
        if p.match(s['content']['pdf']):
            r = requests.get(s['content']['pdf'])
        else:
            r = requests.get(client.baseurl+'/pdf?id='+s['id'], headers=client.headers)
        print "number",s['number'],"response",r
        if not os.path.exists(outputdir+'/pdfs'):
            os.makedirs(outputdir+'/pdfs')
        with open(outputdir+'/pdfs/paper'+str(s['number'])+'.pdf', 'wb') as f:
            f.write(r.content)
            f.close()

def get_conflicts(profile):
    conflicts = set()
    for h in profile['content']['history']:
        conflicts.add(h['institution']['domain'])
    for e in profile['content']['emails']:
        domain = e.split('@')[1]
        conflicts.add(domain)
    return conflicts

def dump_conflicts(profiles, missing, papers, outfilename):
    with open(outputdir+'/'+outfilename,'wb') as outfile:
        csvwriter=csv.writer(outfile,delimiter=',')
        for profile in profiles:

            email = profile['content']['emails'][0]

            profile_conflicts = get_conflicts(profile)

            for paper in papers:
                paper_id = str(paper['number'])
                if not profile_conflicts.isdisjoint(paper['content']['conflicts']):
                    print "conflict detected:",email,profile_conflicts,paper['content']['conflicts']
                    csvwriter.writerow([paper_id,email])

        for email in missing:
            domain = email.split('@')[1]
            for paper in papers:
                paper_id = str(paper['number'])
                if domain in paper['content']['conflicts']:
                    csvwriter.writerow([paper_id,email])


def dump_missing(list):
    with open(outputdir+'/missing-dump.csv','wb') as outfile:
        for email in list:
            csvwriter=csv.writer(outfile,delimiter=',')
            first = all_reviewers[email][0]
            last = all_reviewers[email][1]
            csvwriter.writerow([])

profiles, missing = get_profiles(args.group)
papers = [s.to_json() for s in client.get_notes(invitation='ICLR.cc/2017/workshop/-/submission')]

missing.remove('ICLR.cc/2017/workshop')
missing.remove('ICLR.cc/2017/pcs')

dump_names(profiles,args.outfilename)
write_pdfs(papers)
dump_conflicts(profiles,missing,papers,"conflicts-dump.csv")



