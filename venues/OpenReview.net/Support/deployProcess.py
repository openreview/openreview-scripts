def process(client, note, invitation):
    print('client:', client.baseurl)
    print('note:', note.id)
    print('invitation:', invitation.id)
    conference = openreview.helpers.get_conference(client, note.forum)
    print(conference.get_id())
    forum = client.get_note(id=note.forum)
    comment_readers = forum.content['Contact Emails'][:]
    comment_readers.append('OpenReview.net/Support')
    comment_note = openreview.Note(
        invitation = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Comment',
        forum = forum.id,
        replyto = forum.id,
        readers = comment_readers,
        writers = ['OpenReview.net/Support'],
        signatures = ['OpenReview.net/Support'],
        content = {
            'title': 'Your venue is available in OpenReview',
            'comment': '''
Hi Program Chairs,

Thanks for submitting a venue request.

We have set up the venue based on the information that you provided here: https://openreview.net/forum?id={noteId}

You can use the following links to access to the conference:

Venue home page: https://openreview.net/group?id={conference_id}
Venue Program Chairs console: https://openreview.net/group?id={program_chairs_id}

If you need to make a change to the information provided in your request form, please edit/revise it directly. We will update your venue accordingly.

If you need special features that are not included in your request form, you can create a comment here or contact us at info@openreview.net and we will assist you.

Thanks!

OpenReview Team
            '''.format(noteId = forum.id, conference_id = conference.get_id(), program_chairs_id = conference.get_program_chairs_id())
        }
    )
    client.post_note(comment_note)

    readers = [conference.get_program_chairs_id(), 'OpenReview.net/Support']
    readers.extend(forum.signatures[:])

    forum.writers = ['OpenReview.net']
    forum.readers = readers
    client.post_note(forum)

    revision_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Revision',
        super = 'OpenReview.net/Support/-/Revision',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'referent': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            }
        },
        signatures = ['OpenReview.net/Support']
    ))

    if (forum.content['Area Chairs (Metareviewers)'] == "Yes, our venue has Area Chairs") :
        metareview_stage_invitation = client.post_invitation(openreview.Invitation(
            id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Meta_Review_Stage',
            super = 'OpenReview.net/Support/-/Meta_Review_Stage',
            invitees = readers,
            reply = {
                'forum': forum.id,
                'referent': forum.id,
                'readers' : {
                    'description': 'The users who will be allowed to read the above content.',
                    'values' : readers
                }
            },
            signatures = [conference.get_program_chairs_id()]
        ))
        recruitment_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Recruitment',
        super = 'OpenReview.net/Support/-/Recruitment',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'replyto': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            }
        },
        signatures = ['OpenReview.net/Support']
    ))
    else:
        recruitment_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Recruitment',
        super = 'OpenReview.net/Support/-/Recruitment',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'replyto': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            },
            'content': {
                'title': {
                    'value': 'Recruitment',
                    'required': True,
                    'order': 1
                },
                'invitee_role': {
                    'description': 'Please select the role of the invitees in the conference.',
                    'value-radio': ['reviewer'],
                    'default': 'reviewer',
                    'required': True,
                    'order': 2
                },
                'invitee_emails': {
                    'value-regex': '[\\S\\s]{1,20000}',
                    'description': 'Please provide comma separated valid emails. (e.g.  captain_rogers@marvel.com, black_widow@mcu.com)',
                    'required': True,
                    'order': 3
                },
                'invitee_names': {
                    'value-regex': '[\\S\\s]{1,20000}',
                    'description': 'Please provide comma separated names in the *same order* as emails. (e.g. Steve Rogers, John, Natasha Romanoff)',
                    'order': 4
                },
                'invitation_email_subject': {
                    'value-regex': '.*',
                    'description': 'Please carefully review the email subject for the recruitment emails. Make sure not to remove the parenthesized tokens.',
                    'order': 5,
                    'required': True,
                    'default': '[{Abbreviated_Venue_Name}] Invitation to serve as {invitee_role}'
                },
                'invitation_email_content': {
                    'value-regex': '[\\S\\s]{1,10000}',
                    'description': 'Please carefully review the template below before you click submit to send out recruitment emails. Make sure not to remove the parenthesized tokens.',
                    'order': 6,
                    'required': True,
                    'default': '''Dear {name},

You have been nominated by the program chair committee of {Abbreviated_Venue_Name} to serve as {invitee_role}. As a respected researcher in the area, we hope you will accept and help us make {Abbreviated_Venue_Name} a success.

You are also welcome to submit papers, so please also consider submitting to {Abbreviated_Venue_Name}.

We will be using OpenReview.net and a reviewing process that we hope will be engaging and inclusive of the whole community.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

Please answer within 10 days.

If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in.

If you have any questions, please contact us at info@openreview.net.

Cheers!

Program Chairs'''
                }
            }
        },
        signatures = ['OpenReview.net/Support']
    ))

    # if forum.content.get('Author and Reviewer Anonymity', None) == 'Double-blind':
    #     anonymize_submissions_invitation = client.post_invitation(openreview.Invitation(
    #         id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Anonymize_Submissions',
    #         super = 'OpenReview.net/Support/-/Anonymize_Submissions',
    #         invitees = readers,
    #         reply = {
    #             'forum': forum.id,
    #             'replyto': forum.id,
    #             'readers' : {
    #                 'description': 'The users who will be allowed to read the above content.',
    #                 'values' : readers
    #             }
    #         },
    #         signatures = [conference.get_program_chairs_id()]
    #     ))

    review_stage_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Review_Stage',
        super = 'OpenReview.net/Support/-/Review_Stage',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'referent': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            }
        },
        signatures = [conference.get_program_chairs_id()]
    ))

    decision_stage_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Decision_Stage',
        super = 'OpenReview.net/Support/-/Decision_Stage',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'referent': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            }
        },
        signatures = [conference.get_program_chairs_id()]
    ))
