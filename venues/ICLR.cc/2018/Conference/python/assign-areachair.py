import argparse
import sys
import csv
import openreview

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-p','--paper', required=True)
parser.add_argument('-a','--add')
parser.add_argument('-r','--remove')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

paper_number = args.paper
ac_to_remove = args.remove
ac_to_add = args.add

if ac_to_remove and '@' in ac_to_remove:
    ac_to_remove = ac_to_remove.lower()

if ac_to_add and '@' in ac_to_add:
    ac_to_add = ac_to_add.lower()
acs_group = client.get_group('ICLR.cc/2018/Conference/Area_Chairs')
ac_paper_group = client.get_group('ICLR.cc/2018/Conference/Paper{0}/Area_Chair'.format(paper_number))

def get_domains(email):
    full_domain = email.split('@')[1]
    domain_components = full_domain.split('.')
    domains = ['.'.join(domain_components[index:len(domain_components)]) for index, path in enumerate(domain_components)]
    valid_domains = [d for d in domains if '.' in d]
    return valid_domains

def get_user_conflicts(profile_or_email):

    domain_conflicts = set()
    relation_conflicts = set()
    relation_conflicts.update([profile_or_email])
    try:
        profile = client.get_profile(profile_or_email)

        profile_domains = []
        for e in profile.content['emails']:
            profile_domains += get_domains(e)

        domain_conflicts.update(profile_domains)

        institution_domains = [h['institution']['domain'] for h in profile.content['history']]
        domain_conflicts.update(institution_domains)

        if 'relations' in profile.content:
            relation_conflicts.update([r['email'] for r in profile.content['relations']])

        if 'gmail.com' in domain_conflicts:
            domain_conflicts.remove('gmail.com')

        return (domain_conflicts, relation_conflicts)

    except openreview.OpenReviewException as e:
        return (set(), set())

def get_paper_conflicts(n):
    authorids = n.content['authorids']
    domain_conflicts = set()
    relation_conflicts = set()
    for e in authorids:
        author_domain_conflicts, author_relation_conflicts = get_user_conflicts(e)
        if author_domain_conflicts:
            domain_conflicts.update(author_domain_conflicts)
        if author_relation_conflicts:
            relation_conflicts.update(author_relation_conflicts)
        if '@' in e:
            domain_conflicts.update(get_domains(e))

    relation_conflicts = set([e for e in authorids if '@' in e])

    # remove the domain "gmail.com"
    if 'gmail.com' in domain_conflicts:
        domain_conflicts.remove('gmail.com')

    return (domain_conflicts, relation_conflicts)

if ac_to_remove:
    if ac_to_remove in ac_paper_group.members:
        print "removing {0} from {1}".format(ac_to_remove, ac_paper_group.id)
        client.remove_members_from_group(ac_paper_group, ac_to_remove)

if ac_to_add:
    paper = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Submission', number=paper_number)[0]
    user_domain_conflicts, user_relation_conflicts = get_user_conflicts(ac_to_add)
    paper_domain_conflicts, paper_relation_conflicts = get_paper_conflicts(paper)

    domain_conflicts = paper_domain_conflicts.intersection(user_domain_conflicts)
    relation_conflicts = paper_relation_conflicts.intersection(user_relation_conflicts)

    if domain_conflicts:
        print 'Domain conflicts detected: {0}'.format(domain_conflicts)

    if relation_conflicts:
        print 'Relation conflicts detected: {0}'.format(relation_conflicts)

    if domain_conflicts or relation_conflicts:
        user_continue = raw_input('continue with assignment? y/[n]: ').lower() == 'y'
    else:
        user_continue = True

    if user_continue:
        ac_id = 'ICLR.cc/2018/Conference/Paper{0}/Area_Chair'.format(paper_number)
        paper_authors = 'ICLR.cc/2018/Conference/Paper{0}/Authors'.format(paper_number)

        ac_group = openreview.Group(
            id = ac_id,
            readers = [
                'ICLR.cc/2018/Conference',
                'ICLR.cc/2018/Conference/Area_Chairs',
                'ICLR.cc/2018/Conference/Program_Chairs',
                ac_id
                ],
            nonreaders = [
                paper_authors
                ],
            writers = ['ICLR.cc/2018/Conference'],
            signatories = [ac_id],
            signatures = ['ICLR.cc/2018/Conference'],
            members = [ac_to_add])

        print "adding {0} to {1}".format(ac_to_add, ac_group.id)
        client.post_group(ac_group)

        if ac_to_add not in acs_group.members:
            print "adding {0} to {1}".format(ac_to_add, acs_group.id)
            client.add_members_to_group(acs_group, ac_to_add)
    else:
        print "aborting assignment."
