import openreview
import config
import json

client = openreview.Client()
conference = config.get_conference(client)

stoc_review_invitation_template = {
    'id' : 'learningtheory.org/COLT/2019/Conference/-/Paper<number>/STOC_Review',
    'invitees' : [
        'learningtheory.org/COLT/2019/Conference/Program_Chairs'
    ],
    'duedate': 1553990400000,
    'signatures' : [conference.get_id()],
    'readers' : ['learningtheory.org/COLT/2019/Conference/Program_Chairs'],
    'writer' : [conference.get_id()],
    'reply' : {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {'values': [
            conference.id + '/Paper<number>/Authors',
            conference.id + '/Paper<number>/Program_Committee/Submitted',
            conference.id + '/Program_Chairs']
        },
        'writers': {'values': [conference.id + '/Program_Chairs']},
        'signatures': {'values-regex': conference.id + '/Program_Chairs'},
        'content': {
            'title': {
                'order': 1,
                'value-regex': '.{0,500}',
                'description': 'Title of the STOC review.',
                'required': True
            },
            'review': {
                'order': 2,
                'value-regex': '[\\S\\s]{1,200000}',
                'description': 'Maximum 200000 characters.',
                'required': True
            }
        }
    }
}

stoc_rebuttal_invitation_template = {
    'id' : 'learningtheory.org/COLT/2019/Conference/-/Paper<number>/Review_<review_number>/STOC_Rebuttal',
    'invitees' : [
        'learningtheory.org/COLT/2019/Conference/Program_Chairs',
        'learningtheory.org/COLT/2019/Conference/Paper<number>/Authors'
    ],
    'duedate': 1553990400000,
    'signatures' : [conference.get_id()],
    'readers' : [
        'learningtheory.org/COLT/2019/Conference/Program_Chairs',
        'learningtheory.org/COLT/2019/Conference/Paper<number>/Authors'
    ],
    'writer' : [conference.get_id()],
    'reply' : {
        'forum': '<forum>',
        'replyto': None,
        'readers': {'values': [
            'learningtheory.org/COLT/2019/Conference/Paper<number>/Authors',
            'learningtheory.org/COLT/2019/Conference/Paper<number>/Program_Committee/Submitted',
            'learningtheory.org/COLT/2019/Conference/Program_Chairs'
            ]
        },
        'writers': {'values': ['learningtheory.org/COLT/2019/Conference/Paper<number>/Authors']},
        'signatures': {
            'values-regex': conference.id + '/Paper<number>/Authors'
        },
        'content': {
            'title': {
                'order': 1,
                'value-regex': '.{0,500}',
                'description': 'Title of the STOC rebuttal.',
                'required': True
            },
            'rebuttal': {
                'order': 2,
                'value-regex': '[\\S\\s]{1,200000}',
                'description': 'Maximum 200000 characters.',
                'required': True
            }
        }
    }
}

with open('../Data/output.json', 'r') as data_file:
    data_loaded = json.load(data_file)

for review_data in data_loaded:
    paper_number = review_data['number']
    reviews = review_data['reviews']

    for index, review in enumerate(reviews):
        # Post invitation for each paper
        blind_note = client.get_notes(
            invitation = 'learningtheory.org/COLT/2019/Conference/-/Blind_Submission', 
            number = paper_number
        )[0]
        
        stoc_review_invitation = client.post_invitation(
            openreview.Invitation.from_json(
                openreview.tools.fill_template(stoc_review_invitation_template, blind_note)
            )
        )
        

        # Post STOC reviews
        stoc_review_note_template = {
            'invitation'  :   stoc_review_invitation.id,
            'forum'       :   '<forum>',
            'replyTo'     :   '<forum>',
            'signatures'  :   [conference.get_program_chairs_id()],
            'writers'     :   [conference.get_program_chairs_id()],
            'readers'     :   [
                'learningtheory.org/COLT/2019/Conference/Paper<number>/Authors',
                'learningtheory.org/COLT/2019/Conference/Paper<number>/Program_Committee/Submitted',
                'learningtheory.org/COLT/2019/Conference/Program_Chairs'
            ],
            'content'     :   {
                'title': 'STOC Review ' + str(index+1),
                'review': review
            }
        }
        stoc_review_note = client.post_note(
            openreview.Note.from_json(
                openreview.tools.fill_template(stoc_review_note_template, blind_note)
            )
        )
        print ('Posted stoc review - ', stoc_review_note.id)

        # Post author rebuttal invitation
        new_stoc_rebuttal_invitation = openreview.Invitation.from_json(
            openreview.tools.fill_template(stoc_rebuttal_invitation_template, blind_note))

        new_stoc_rebuttal_invitation.id = new_stoc_rebuttal_invitation.id.replace('<review_number>', str(index+1))
        new_stoc_rebuttal_invitation.reply['replyto'] = stoc_review_note.id
        posted_stoc_rebuttal_invitation = client.post_invitation(new_stoc_rebuttal_invitation)
        print ("Rebuttal invitation posted with id: ", posted_stoc_rebuttal_invitation.id )

