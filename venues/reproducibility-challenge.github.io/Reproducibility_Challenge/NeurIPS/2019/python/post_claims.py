import openreview
from openreview import tools
from openreview import invitations
import datetime

# live
#client = openreview.Client(baseurl='https://openreview.net')
# dev site
#client = openreview.Client(baseurl='https://dev.openreview.net', username='OpenReview.net', password='OpenReview_dev')
client = openreview.Client()
print(client.baseurl)
conference_id='reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'


#PAM TODO remember to expire Claim invites manually in November

# Claimant group - those that will be able to see the Report Submisson button
client.post_group(openreview.Group(id = conference_id+'/Claimants',
                    readers = [conference_id+'Program_Chairs'],
                    nonreaders = [],
                    writers = [conference_id],
                    signatories = [conference_id],
                    signatures = ['~Super_User1'],
                    members = [],
                    details = { 'writable': True })
                )

# Claim invitations
notes = client.get_notes(invitation=conference_id+"/-/NeurIPS_Submission")
for note in notes:
    group = client.post_group(openreview.Group(id='{conf_id}/Paper{number}'.format(conf_id = conference_id, number = note.number),
                              readers = ['everyone'],
                              writers = [conference_id],
                              signatures = [conference_id],
                              signatories = [conference_id]))

    claim_inv = openreview.Invitation(
        id = conference_id+"/Paper"+str(note.number)+"/-/Claim",
        readers = ['everyone'],
        invitees = ['~'],
        writers = [conference_id],
        signatures = [conference_id],
        reply = {'content': {'title': {'value': 'Claim',
                                          'order': 0,
                                          'required': True,
                                      },
                             'plan': {'description': 'Your plan to reproduce results(max 5000 chars).',
                                      'order': 1,
                                      'required': True,
                                      'value-regex': '[\\S\\s]{1,5000}'},
                             'institution': {'description': 'Your institution or organization(max 100 chars).',
                                      'order': 2,
                                      'required': True,
                                      'value-regex': '.{1,100}'},
                            },
                 'forum': note.id,
                 'replyto': note.id,
                 'signatures': {'description': 'Your authorized identity to be associated with the above content.',
                                'values-regex': '~.*'},
                 'readers': {'description': 'The users who will be allowed to read the above content.',
                                          'values': [conference_id+'/Program_Chairs']},
                  'writers': {'values-copied': [conference_id,'{signatures}']}

                },
        process='../process/claimProcess.py'
    )
    print(claim_inv.id)
    claim_inv = client.post_invitation(claim_inv)

    # this is the claim that can be seen by everyone,
    # created in process function for Claim
    claim_hold_inv = openreview.Invitation(
        id = conference_id+"/Paper"+str(note.number)+"/-/Claim_Hold",
        readers = [],
        invitees = ['~'],
        writers = [conference_id],
        signatures = [conference_id],
        reply = {'content': {'title': {'value-regex': '.{1,120}',
                                          'order': 0,
                                          'required': True,
                                      }},
                 'forum': note.id,
                 'replyto': note.id,
                 'signatures': {'values': [conference_id]},
                 'readers': {'description': 'The users who will be allowed to read the above content.',
                                          'values': ['everyone']},
                  'writers': {'values-copied': [conference_id,'{signatures}']}

                }
        # process='../process/commentProcess.js',
    )
    print(claim_hold_inv.id)
    claim_hold_inv = client.post_invitation(claim_hold_inv)


#client.post_invitation(invitations.Submission(id=conference_id+'/-/Report_Submission'),
#                       invitees = [conference_id+'/Claimants'])
