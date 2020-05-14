def process_update(client, note, invitation, existing_note):

    ## Notify authors and editor
    author_subject = 'Agora Covid-19 has received your article titled ' + note.content['title']
    action = 'posted'
    if existing_note:
        action = 'deleted' if note.ddate else 'updated'

    author_message = '''Your submission to Agora Covid-19 has been {action}.

Title: {title}
To view your article, click here: https://openreview.net/forum?id={forum}

'''.format(action=action, number=note.number, title=note.content['title'], forum=note.forum)

    coauthor_message = author_message + '\n\nIf you are not an author of this article and would like to be removed, please contact the author who added you at {tauthor}'.format(tauthor=note.tauthor)

    client.post_message(subject=author_subject,
        recipients=[note.tauthor],
        message=author_message,
        ignoreRecipients=None,
        sender=None
    )

    client.post_message(subject=author_subject,
        recipients=note.content['authorids'],
        message=coauthor_message,
        ignoreRecipients=[note.tauthor],
        sender=None
    )

    support = 'OpenReview.net/Support'
    editor = '-Agora/Covid-19/Editor'

    client.post_message(subject='Article {action} to Agora Covid-10'.format(action=action),
        recipients=[editor, support],
        message='https://openreview.net/forum?id={forum}'.format(forum=note.forum),
        ignoreRecipients=None,
        sender=None
    )

    ## Create article groups
    article_group = openreview.Group(
        id='-Agora/Covid-19/Article{}'.format(note.number),
        readers=['everyone'],
        writers=[support],
        signatures=[support],
        signatories=[support],
        members=[],
    )
    client.post_group(article_group)

    authors_group_id = '{}/Authors'.format(article_group.id)
    authors_group = openreview.Group(
        id=authors_group_id,
        readers=['everyone'],
        writers=[support],
        signatures=[support],
        signatories=[authors_group_id],
        members=note.content['authorids'],
    )
    client.post_group(authors_group)

    editors_group_id = '{}/Editors'.format(article_group.id)
    editors_group = openreview.Group(
        id=editors_group_id,
        readers=['everyone'],
        writers=[support],
        signatures=[support],
        signatories=[editors_group_id],
        members=[],
    )
    client.post_group(editors_group)

    reviewers_group_id = '{}/Reviewers'.format(article_group.id)
    reviewers_group = openreview.Group(
        id=reviewers_group_id,
        readers=['everyone'],
        writers=[support],
        signatures=[support],
        signatories=[reviewers_group_id],
        members=[],
    )
    client.post_group(reviewers_group)

    ## Create invitations
    revision_invitation = openreview.Invitation(
        id = '{}/-/Revision'.format(article_group.id),
        super = '-Agora/Covid-19/-/Revision',
        invitees = [authors_group_id, support],
        writers = [support],
        signatures = [support],
        reply = {
            'forum': note.forum,
            'referent': note.forum,
            'writers': {
                'values': [authors_group_id, support]
            },
            'signatures': {
                'values-regex': '{}|{}'.format(authors_group_id, support)
            }
        }
    )
    client.post_invitation(revision_invitation)

    assign_editor_invitation = openreview.Invitation(
        id = '{}/-/Assign_Editor'.format(article_group.id),
        super = '-Agora/Covid-19/-/Assign_Editor',
        invitees = [editor, support],
        writers = [support],
        signatures = [support],
        reply = {
            'forum': note.forum,
            'referent': note.forum,
            'writers': {
                'values': [editor, support]
            },
            'signatures': {
                'values-regex': '{}|{}'.format(editor, support)
            }
        }
    )
    client.post_invitation(assign_editor_invitation)

    assign_reviewer_invitation = openreview.Invitation(
        id = '{}/-/Assign_Reviewer'.format(article_group.id),
        super = '-Agora/Covid-19/-/Assign_Reviewer',
        invitees = [editors_group_id, support],
        writers = [support],
        signatures = [support],
        reply = {
            'forum': note.forum,
            'referent': note.forum,
            'writers': {
                'values': [editors_group_id, support]
            },
            'signatures': {
                'values-regex': '{}|{}'.format(editors_group_id, support)
            }
        }
    )
    client.post_invitation(assign_reviewer_invitation)

    review_invitation = openreview.Invitation(
        id = '{}/-/Review'.format(article_group.id),
        super = '-Agora/Covid-19/-/Review',
        invitees = [reviewers_group_id, support],
        writers = [support],
        signatures = [support],
        reply = {
            'forum': note.forum,
            'replyto': note.forum,
            'readers': {
                # 'values-dropdown': [
                #    'everyone',
                #     editor,
                #     editors_group_id,
                #     reviewers_group_id
                # ],
                # Temporally use everyone only.
                'values': ['everyone']
                'default': ['everyone']
            },
            'writers': {
                'values-copied': ['{signatures}', support]
            },
            'signatures': {
                'values-regex': '~.*|{}'.format(support)
            }
        }
    )
    client.post_invitation(review_invitation)


