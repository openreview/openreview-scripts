import openreview
import argparse


def get_profile_info(i):

    if '@' in i:
        profile=client.search_profiles(emails=[i])[i]
    elif '~' in i:
        profile=client.search_profiles(ids=[i])[0]  
    try:
        test=profile.content
    except:
        return "profile not found: {}".format(i)
    
    domains = set()
    emails=set()
    relations = set()
    common_domains = ['gmail.com', 'qq.com', '126.com', '163.com', 
                      'outloook.com', 'hotmail.com', 'yahoo.com', 'aol.com', 'msn.com', 'ymail.com', 'googlemail.com', 'live.com']

    ## Institution section, get history within the last three years
    for h in profile.content.get('history', []):
        if h.get('end') is None or int(h.get('end')) > 2017:
            domain = h.get('institution', {}).get('domain', '')
            domains.update(openreview.tools.subdomains(domain))

    ## Relations section, get coauthor/coworker relations within the last three years + all the other relations
    for r in profile.content.get('relations', []):
        if r.get('relation', '') in ['Coauthor','Coworker']:
            if r.get('end') is None or int(r.get('end')) > 2017:
                relations.add(r['email'])
        else:
            relations.add(r['email'])
    
    ## Emails section        
    for email in profile.content['emails']:
        emails.add(email)
        # if institution section is empty, add email domains
        if not domains: 
            domains.update(openreview.tools.subdomains(email))
            
    ## Filter common domains
    for common_domain in common_domains:
        if common_domain in domains:
            domains.remove(common_domain)

    return {
        'id': profile.id,
        'domains': domains,
        'emails': emails,
        'relations': relations
    }


def _get_edge_readers(tail):
    readers = [conference.id]
    if should_read_by_area_chair:
        if conference.use_senior_area_chairs:
            readers.append(conference.get_senior_area_chairs_id())
        readers.append(conference.get_area_chairs_id())
    readers.append(tail)
    return readers


def _create_edge_invitation(edge_id, match_group, edited_by_assigned_ac=False):
    '''
    Creates an edge invitation given an edge name
    e.g. "Affinity_Score"
    '''
    is_assignment_invitation=edge_id.endswith('Assignment') or edge_id.endswith('Aggregate_Score')
    paper_number='{head.number}' if is_assignment_invitation else None

    edge_readers = [conference.get_id()]
    edge_writers = [conference.get_id()]
    edge_signatures = [conference.get_id() + '$', conference.get_program_chairs_id()]
    edge_nonreaders = {
        'values-regex': conference.get_authors_id(number='.*')
    }
    if should_read_by_area_chair:
        if conference.use_senior_area_chairs:
            edge_readers.append(conference.get_senior_area_chairs_id(number=paper_number))
        ## Area Chairs should read the edges of the reviewer invitations.
        edge_readers.append(conference.get_area_chairs_id(number=paper_number))
        if is_assignment_invitation:
            if conference.use_senior_area_chairs:
                edge_writers.append(conference.get_senior_area_chairs_id(number=paper_number))
                edge_signatures.append(conference.get_senior_area_chairs_id(number=paper_number))
            edge_writers.append(conference.get_area_chairs_id(number=paper_number))
            edge_signatures.append(conference.get_anon_area_chair_id(number=paper_number, anon_id='.*'))
            edge_nonreaders = {
                'values': [conference.get_authors_id(number=paper_number)]
            }

    readers = {
        'values-copied': edge_readers + ['{tail}']
    }

    edge_head_type = 'Note'
    edge_head_query = {
        'invitation' : conference.get_blind_submission_id()
    }
    if 'Custom_Max_Papers' in edge_id:
        edge_head_type = 'Group'
        edge_head_query = {
            'id' : edge_id.split('/-/')[0]
        }
    if is_senior_area_chair:
        edge_head_type = 'Profile'
        edge_head_query = {
            'group' : conference.get_area_chairs_id()
        }

    invitation = openreview.Invitation(
        id=edge_id,
        invitees=[conference.get_id(), conference.support_user],
        readers=[conference.get_id(), conference.get_senior_area_chairs_id(), conference.get_area_chairs_id()],
        writers=[conference.get_id()],
        signatures=[conference.get_id()],
        reply={
            'readers': readers,
            'nonreaders': edge_nonreaders,
            'writers': {
                'values': edge_writers
            },
            'signatures': {
                'values-regex': '|'.join(edge_signatures),
                'default': conference.get_program_chairs_id()
            },
            'content': {
                'head': {
                    'type': edge_head_type,
                    'query' : edge_head_query
                },
                'tail': {
                    'type': 'Profile',
                    'query' : {
                        'group' : match_group.id
                    }
                },
                'weight': {
                    'value-regex': r'[-+]?[0-9]*\.?[0-9]*'
                },
                'label': {
                    'value-regex': '.*'
                }
            }
        })

    invitation = client.post_invitation(invitation)
    client.delete_edges(invitation.id)
    return invitation


def build_conflicts(match_group):
    edges=[]

    invitation=_create_edge_invitation(conference.get_invitation_id('Conflict',prefix=match_group.id), match_group)

    for submission in submissions:
        author_ids=submission.details['original']['content']['authorids']

        author_domains = set()
        author_emails = set()
        author_relations = set()

        for author in author_ids:
            author_info = get_profile_info(author)
            author_domains.update(author_info['domains'])
            author_emails.update(author_info['emails'])
            author_relations.update(author_info['relations'])

        for user in match_group.members:
            user_info = get_profile_info(user)
            conflicts = set()
            conflicts.update(author_domains.intersection(user_info['domains']))
            conflicts.update(author_relations.intersection(user_info['emails']))
            conflicts.update(author_emails.intersection(user_info['relations']))
            conflicts.update(author_emails.intersection(user_info['emails']))

            if conflicts:
                edges.append(openreview.Edge(
                    invitation=invitation.id,
                    head=submission.id,
                    tail=user_info['id'],
                    weight=-1,
                    label='Conflict',
                    readers=_get_edge_readers(tail=user_info['id']),
                    writers=[conference.id],
                    signatures=[conference.id]
                    ))

    openreview.tools.post_bulk_edges(client, edges=edges)

    # Perform sanity check
    edges_posted = client.get_edges_count(invitation=invitation.id)
    if edges_posted < len(edges):
        raise openreview.OpenReviewException('Failed during bulk post of Conflict edges! Scores found: {0}, Edges posted: {1}'.format(len(edges), edges_posted))
    
    return edges


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference=openreview.helpers.get_conference(client, '5-TLJ7mpH8g') ## neurips2021 dev site id

    submissions = list(openreview.tools.iterget_notes(conference.client,
                    invitation=conference.get_blind_submission_id(), details='original'))

    sac_group=client.get_group(conference.get_senior_area_chairs_id())
    ac_group=client.get_group(conference.get_area_chairs_id())
    rev_group=client.get_group(conference.get_reviewers_id())

    for match_group in [sac_group, ac_group, rev_group]:
        is_area_chair = conference.get_area_chairs_id() == match_group.id
        is_senior_area_chair = conference.get_senior_area_chairs_id() == match_group.id
        should_read_by_area_chair = conference.get_reviewers_id() == match_group.id
        post_edges=build_conflicts(match_group)

