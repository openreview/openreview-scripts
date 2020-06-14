import openreview
import csv
import time
from tqdm import tqdm
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help='base url')
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    ac_group = client.get_group('thecvf.com/ECCV/2020/Conference/Area_Chairs')
    secondary_ac_group = client.post_group(openreview.Group(
        id = 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs',
        signatures = ['thecvf.com/ECCV/2020/Conference'],
        signatories = ['thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'],
        readers = [
            'thecvf.com/ECCV/2020/Conference',
            'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'],
        writers = ['thecvf.com/ECCV/2020/Conference'],
        members = ac_group.members
    ))
    print ('Posted Secondary AC group: {}\n'.format(secondary_ac_group.id))

    aggregate_score_invitation = client.post_invitation(openreview.Invitation(
        id='thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Aggregate_Score',
        readers=[
            'thecvf.com/ECCV/2020/Conference',
            'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'],
        writers=['thecvf.com/ECCV/2020/Conference'],
        invitees=['thecvf.com/ECCV/2020/Conference'],
        signatures=['thecvf.com/ECCV/2020/Conference'],
        reply={
            'readers': {
                'values-copied': [
                    'thecvf.com/ECCV/2020/Conference',
                    '{tail}']
                },
            'nonreaders': {
                'values-regex': 'thecvf.com/ECCV/2020/Conference/Paper.*/Authors'
                },
            'writers': {
                'values': ['thecvf.com/ECCV/2020/Conference']
                },
            'signatures': {
                'values': ['thecvf.com/ECCV/2020/Conference']
                },
            'content': {
                'head': {
                    'type': 'Note',
                    'query': {'invitation': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'}
                },
                'tail': {
                    'type': 'Profile',
                    'query': {'group': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'}
                },
                'weight': {'value-regex': '[-+]?[0-9]*\\.?[0-9]*'},
                'label': {'value-regex': '.*'}
            }
        }))
    print('Posted aggregate score invitation:', aggregate_score_invitation.id)

    map_submissions = {note.number: note for note in openreview.tools.iterget_notes(client, invitation = 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}
    
    all_meta_reviews = list(openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/-/Meta_Review$'))
    print('Found {} official meta reviews\n'.format(len(all_meta_reviews)))
    set_reject_papers = set()
    for meta in all_meta_reviews:
        paper_num = int(meta.invitation.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions:
            if meta.content['clear_reject'] == 'Yes':
                set_reject_papers.add(paper_num)

    print('Found {} submissions with clear rejects'.format(len(set_reject_papers)))
    custom_demand_invitation = client.post_invitation(openreview.Invitation(
        id='thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Custom_User_Demands',
        signatures=['thecvf.com/ECCV/2020/Conference'],
        readers=[
            'thecvf.com/ECCV/2020/Conference',
            'thecvf.com/ECCV/2020/Conference/Area_Chairs'],
        writers=['thecvf.com/ECCV/2020/Conference'],
        invitees=['thecvf.com/ECCV/2020/Conference'],
        reply = {
            'readers': {'values-copied': [
                'thecvf.com/ECCV/2020/Conference',
                'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                '{tail}']},
            'nonreaders': {'values-regex': 'thecvf.com/ECCV/2020/Conference/Paper.*/Authors'},
            'writers': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'signatures': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'content': {
                'head': {
                    'query' : {'invitation': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'},
                    'type': 'Note'
                },
                'tail': {
                    'query' : {'id': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'},
                    'type': 'Profile'
                },
                'weight': {
                    'value-regex': '[-+]?[0-9]*\\.?[0-9]*'
                },
                'label': {
                    'value-regex': '.*'
                }
            }
        }
    ))
    print('Posted invitation {}\n'.format(custom_demand_invitation.id))

    print('\nPosting Custom_Max_Papers invitation')
    custom_max_papers_invitation = client.post_invitation(openreview.Invitation(
        id='thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Custom_Max_Papers',
        signatures=['thecvf.com/ECCV/2020/Conference'],
        readers=[
            'thecvf.com/ECCV/2020/Conference',
            'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'],
        writers=['thecvf.com/ECCV/2020/Conference'],
        invitees=['thecvf.com/ECCV/2020/Conference'],
        reply = {
            'readers': {'values-copied': [
                'thecvf.com/ECCV/2020/Conference',
                'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs',
                '{tail}']},
            'nonreaders': {'values-regex': 'thecvf.com/ECCV/2020/Conference/Paper.*/Authors'},
            'writers': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'signatures': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'content': {
                'head': {
                    'query' : {'id': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'},
                    'type': 'Profile'
                },
                'tail': {
                    'query' : {'invitation': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'},
                    'type': 'Note'
                },
                'weight': {
                    'value-regex': '[-+]?[0-9]*\\.?[0-9]*'
                },
                'label': {
                    'value-regex': '.*'
                }
            }
        }
    ))
    print('Done posting Custom_Max_Papers invitation\n')

    print('\nDeleting old edges for invitation:"thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Custom_User_Demands"')
    client.delete_edges(invitation='thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Custom_User_Demands')
    print('Done Deleting old edges\n')

    secondary_ac_demands = []
    total_review_demand = 0
    print('Accumulating Custom_User_Demand edges')
    for paper_num, sub in tqdm(map_submissions.items()):
        weight = 0
        if paper_num not in set_reject_papers:
            weight = 1
            total_review_demand += 1
        
        secondary_ac_demands.append(openreview.Edge(
            head=sub.id,
            tail='thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs',
            weight=weight,
            invitation='thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Custom_User_Demands',
            readers=[
                'thecvf.com/ECCV/2020/Conference',
                ],
            writers=['thecvf.com/ECCV/2020/Conference'],
            signatures=['thecvf.com/ECCV/2020/Conference']
        ))

    print('Custom_User_Demands: Posting {0} edges'.format(len(secondary_ac_demands)))
    posted_edges = openreview.tools.post_bulk_edges(client, secondary_ac_demands)
    print('Custom_User_Demands: Posted {0} edges\n'.format(len(posted_edges)))

    conflicts = []

    print('\nDeleting old edges for invitation:"thecvf.com/ECCV/2020/Conference/Area_Chairs/-/Conflict" and label: "Already Assigned"')
    client.delete_edges(invitation='thecvf.com/ECCV/2020/Conference/Area_Chairs/-/Conflict', label='Already Assigned')
    print('Done Deleting old edges\n')

    area_chair_groups = list(openreview.tools.iterget_groups(
        client, 
        regex='^thecvf.com/ECCV/2020/Conference/Paper.*/Area_Chair1$'))
    print('\nFound {} area chair groups'.format(len(area_chair_groups)))

    for grp in area_chair_groups:
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions and grp.members:
            conflicts.append(openreview.Edge(
                head=map_submissions[paper_num].id,
                tail=grp.members[0],
                invitation='thecvf.com/ECCV/2020/Conference/Area_Chairs/-/Conflict',
                readers=[
                    'thecvf.com/ECCV/2020/Conference',
                    grp.members[0]
                ],
                writers=['thecvf.com/ECCV/2020/Conference'],
                signatures=['thecvf.com/ECCV/2020/Conference'],
                weight=-1,
                label='Already Assigned'
            ))

    print('\nArea_Chairs/-/Conflict: Posting {0} edges'.format(len(conflicts)))
    posted_edges = openreview.tools.post_bulk_edges(client, conflicts)
    print('\nArea_Chairs/-/Conflict: Posted  {0} edges'.format(len(posted_edges)))


    print('\nChecking if Secondary_Area_Chairs matching is set up already')
    secondary_ac_assignment_config = openreview.tools.get_invitation(
        client, 
        'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Assignment_Configuration')
    
    if secondary_ac_assignment_config:
        print('\nSecondary ac matching has been setup already')
    else:
        print('Secondary ac matching not set up. Setting it up now.')
        secondary_ac_assignment_config = client.post_invitation(
            openreview.Invitation(
                id='thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Assignment_Configuration',
                signatures=['thecvf.com/ECCV/2020/Conference'],
                readers=['thecvf.com/ECCV/2020/Conference'],
                writers=['thecvf.com/ECCV/2020/Conference'],
                invitees=['thecvf.com/ECCV/2020/Conference'],
                reply={
                    'readers': {'values': ['thecvf.com/ECCV/2020/Conference']},
                    'writers': {'values': ['thecvf.com/ECCV/2020/Conference']},
                    'signatures': {'values': ['thecvf.com/ECCV/2020/Conference']},
                    'content': {
                        'title': {
                            'value-regex': '.{1,250}',
                            'required': True,
                            'description': 'Title of the configuration.',
                            'order': 1
                        },
                        'user_demand': {
                            'value-regex': '[0-9]+',
                            'required': True,
                            'description': 'Number of users that can review a paper',
                            'order': 2
                        },
                        'max_papers': {
                            'value-regex': '[0-9]+',
                            'required': True,
                            'description': 'Max number of reviews a user has to do',
                            'order': 3
                        },
                        'min_papers': {
                            'value-regex': '[0-9]+',
                            'required': True,
                            'description': 'Min number of reviews a user should do',
                            'order': 4
                        },
                        'alternates': {
                            'value-regex': '[0-9]+',
                            'required': True,
                            'description': 'The number of alternate reviewers to save (per-paper)',
                            'order': 5
                        },
                        'paper_invitation': {
                            'value-regex': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission.*',
                            'default': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission',
                            'required': True,
                            'description': 'Invitation to get the configuration note',
                            'order': 6
                        },
                        'match_group': {
                            'value-regex': 'thecvf.com/ECCV/2020/Conference/.*',
                            'default': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs',
                            'required': True,
                            'description': 'Group id containing users to be matched',
                            'order': 7
                        },
                        'scores_specification': {
                            'value-dict': {},
                            'required': False,
                            'description': 'Manually entered JSON score specification',
                            'order': 8,
                            'default': {
                                'thecvf.com/ECCV/2020/Conference/Area_Chairs/-/TPMS_Score': {
                                    'default': 0,
                                    'weight': 1
                                },
                                'thecvf.com/ECCV/2020/Conference/Area_Chairs/-/Affinity_Score': {
                                    'default': 0,
                                    'weight': 0.5
                                },
                                'thecvf.com/ECCV/2020/Conference/Area_Chairs/-/Bid': {
                                    'translate_map': {
                                        'Neutral': 0,
                                        'Very High': 0.15,
                                        'High': 0.1,
                                        'Low': -0.5,
                                        'Very Low': -1
                                    },
                                    'default': 0,
                                    'weight': 1
                                }
                            }
                        },
                        'aggregate_score_invitation': {
                            'value-regex': 'thecvf.com/ECCV/2020/Conference/.*',
                            'default': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Aggregate_Score',
                            'required': True,
                            'description': 'Invitation to store aggregated scores',
                            'order': 9
                        },
                        'conflicts_invitation': {
                            'value-regex': 'thecvf.com/ECCV/2020/Conference/.*',
                            'default': 'thecvf.com/ECCV/2020/Conference/Area_Chairs/-/Conflict',
                            'required': True,
                            'description': 'Invitation to store conflict scores',
                            'order': 10
                        },
                        'assignment_invitation': {
                            'value': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Paper_Assignment',
                            'required': True,
                            'description': 'Invitation to store paper user assignments',
                            'order': 11
                        },
                        'custom_user_demand_invitation': {
                            'value-regex': 'thecvf.com/ECCV/2020/Conference/.*/-/Custom_User_Demands$',
                            'default': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Custom_User_Demands',
                            'description': 'Invitation to store custom number of users required by papers',
                            'order': 12,
                            'required': False
                        },
                        'custom_max_papers_invitation': {
                            'value-regex': 'thecvf.com/ECCV/2020/Conference/.*/-/Custom_Max_Papers$',
                            'default': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Custom_Max_Papers',
                            'description': 'Invitation to store custom max number of papers that can be assigned to reviewers',
                            'order': 13,
                            'required': False
                        },
                        'config_invitation': {
                            'value': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Assignment_Configuration',
                            'order': 14
                        },
                        'solver': {
                            'value-radio': [
                                'MinMax',
                                'FairFlow'
                                ],
                            'default': 'MinMax',
                            'required': True,
                            'order': 15
                        },
                        'status': {
                            'default': 'Initialized',
                            'value-dropdown': [
                                'Initialized',
                                'Running',
                                'Error',
                                'No Solution',
                                'Complete',
                                'Deployed'
                            ],
                            'order': 16
                        },
                        'error_message': {
                            'value-regex': '.*',
                            'required': False,
                            'order': 17
                        }
                    }
                }
            )
        )

        print('\nPosting invitation "thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Paper_Assignment"')
        client.post_invitation(openreview.Invitation(
            id='thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs/-/Paper_Assignment',
            readers=['thecvf.com/ECCV/2020/Conference', 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'],
            writers=['thecvf.com/ECCV/2020/Conference'],
            invitees=['thecvf.com/ECCV/2020/Conference'],
            signatures=['thecvf.com/ECCV/2020/Conference'],
            multiReply=True,
            reply={
                'readers': {
                    'values-copied': [
                        'thecvf.com/ECCV/2020/Conference',
                        '{tail}'
                    ]
                },
                'nonreaders': {'values-regex': 'thecvf.com/ECCV/2020/Conference/Paper.*/Authors'},
                'writers': {'values': ['thecvf.com/ECCV/2020/Conference']},
                'signatures': {'values': ['thecvf.com/ECCV/2020/Conference']},
                'content': {
                    'tail': {
                        'query': {'group': 'thecvf.com/ECCV/2020/Conference/Secondary_Area_Chairs'},
                        'type': 'Profile'
                    },
                    'label': {'value-regex': '.*'},
                    'weight': {'value-regex': '[-+]?[0-9]*\\.?[0-9]*'},
                    'head': {
                        'query': {'invitation': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'},
                        'type': 'Note'
                    }
                }
            }
        ))

        print('Secondary_Area_Chairs match setup done.')


    print('\nTotal Secondary AC meta review demand: {}'.format(total_review_demand))
