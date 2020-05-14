def process_update(client, note, invitation, existing_note):

    support = 'OpenReview.net/Support'
    article_group_id = invitation.id.split('/-/')[0]
    reviewers_group_id = '{}/Reviewers'.format(article_group_id)
    reviewers_group = openreview.Group(
        id=reviewers_group_id,
        readers=['everyone'],
        writers=[support],
        signatures=[support],
        signatories=[reviewers_group_id],
        members=note.content.get('assigned_reviewers', []),
    )
    client.post_group(reviewers_group)