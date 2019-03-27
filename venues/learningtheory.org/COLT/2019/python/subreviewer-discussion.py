import argparse
import openreview
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    blind_notes = list(openreview.tools.iterget_notes(client, invitation=conference.id + '/-/Blind_Submission'))

    for index, note in enumerate(blind_notes):
        paper_number = str(note.number)

        # Post the discussion group
        discussion_group = client.post_group(openreview.Group(
            id = conference.id + '/Paper{0}/Reviewers/Discussion'.format(paper_number),
            readers = [
                conference.get_program_chairs_id(),
                conference.id + '/Paper{0}/Program_Committee'.format(paper_number)
            ],
            writers = [
                conference.get_program_chairs_id(),
                conference.id + '/Paper{0}/Program_Committee'.format(paper_number)
            ],
            signatories = [conference.id + '/Paper{0}/Reviewers/Discussion'.format(paper_number)],
            signatures = [conference.id + '/Paper{0}/Program_Committee'.format(paper_number)]
        ))

        # Update the comment invitation for this paper
        comment_invi = client.get_invitations(
            regex = conference.id + '/-/Paper{0}/Comment'.format(paper_number),
            details = 'repliedNotes')[0]

        comment_invi.invitees = [
            conference.id + '/Program_Chairs',
            conference.id + '/Paper{0}/Program_Committee'.format(paper_number),
            conference.id + '/Paper{0}/Reviewers/Discussion'.format(paper_number)
        ]
        comment_invi.noninvitees = [
            conference.id + '/Paper319/Program_Committee/Unsubmitted'
        ]
        comment_invi.readers = [
            conference.id + '/Program_Chairs',
            conference.id + '/Paper{0}/Program_Committee'.format(paper_number),
            conference.id + '/Paper{0}/Reviewers/Discussion'.format(paper_number)
        ]

        comment_invi.reply['readers']['values'] = [
            conference.id + '/Program_Chairs',
            conference.id + '/Paper{0}/Program_Committee'.format(paper_number),
            conference.id + '/Paper{0}/Reviewers/Discussion'.format(paper_number)
        ]

        comment_invi.reply['signatures']['values-regex'] = conference.id + '/Paper{0}/Program_Committee_Member[0-9]+|'.format(paper_number) + \
            conference.id + '/Program_Chairs|' + conference.id + '/Paper{0}/AnonReviewer[0-9]+'.format(paper_number)

        comment_invi.reply['writers']['values-copied'] = [
            conference.id + '',
            '{signatures}'
        ]

        posted_invi = client.post_invitation(comment_invi)

        # Updating the already posted comments on this forum

        for comment in comment_invi.details['repliedNotes']:
            comment_note = openreview.Note.from_json(comment)
            comment_note.readers = comment_invi.reply['readers']['values']
            try:
                client.post_note(comment_note)
            except Exception as e:
                print (comment_note.id)
                print (e)

        # Update the official review invitation for this paper
        review_invi = client.get_invitations(
            regex = conference.id + '/-/Paper{0}/Official_Review'.format(paper_number),
            details = 'repliedNotes')[0]

        review_invi.reply['readers']['values'] = [
            conference.id + '/Program_Chairs',
            conference.id + '/Paper{0}/Program_Committee'.format(paper_number),
            conference.id + '/Paper{0}/Authors'.format(paper_number),
            conference.id + '/Paper{0}/Reviewers/Discussion'.format(paper_number),
        ]

        posted_invi = client.post_invitation(review_invi)

        # Updating the already posted reviews on this forum

        for review in review_invi.details['repliedNotes']:
            review_note = openreview.Note.from_json(review)
            review_note.readers = review_invi.reply['readers']['values']
            try:
                client.post_note(review_note)
            except Exception as e:
                print (review_note.id)
                print (e)

        # Updating Rebuttal invi and already posted rebuttals
        rebuttal_invis = client.get_invitations(
            regex = conference.id + '/-/Paper{0}/Review[0-9]+/Rebuttal$'.format(paper_number),
            details = 'repliedNotes')

        for rebuttal_invi in rebuttal_invis:
            rebuttal_invi.reply['readers']['values'] = [
                conference.id + '/Paper{0}/Authors'.format(paper_number),
                conference.id + '/Paper{0}/Program_Committee'.format(paper_number),
                conference.id + '/Program_Chairs',
                conference.id + '/Paper{0}/Reviewers/Discussion'.format(paper_number)
            ]
            client.post_invitation(rebuttal_invi)
            for rebuttal_json in rebuttal_invi.details['repliedNotes']:
                rebuttal_note = openreview.Note.from_json(rebuttal_json)
                rebuttal_note.readers = rebuttal_invi.reply['readers']['values']
                try:
                    client.post_note(rebuttal_note)
                except Exception as e:
                    print (rebuttal_note.id)
                    print (e)

        # Add Discussion group to readers for PCM and AnonRevs

        pcm_groups = client.get_groups(regex = conference.id + '/Paper{}/Program_Committee_Member[0-9]+$'.format(paper_number))
        for pcm in pcm_groups:
            readers = pcm.readers
            if conference.id + '/Paper{}/Reviewers/Discussion'.format(paper_number) not in readers:
                pcm.readers.append(conference.id + '/Paper{}/Reviewers/Discussion'.format(paper_number))
                client.post_group(pcm)

        anon_groups = client.get_groups(regex = conference.id + '/Paper{}/AnonReviewer[0-9]+$'.format(paper_number))
        for anon in anon_groups:
            readers = anon.readers
            if conference.id + '/Paper{}/Reviewers/Discussion'.format(paper_number) not in readers:
                anon.readers.append(conference.id + '/Paper{}/Reviewers/Discussion'.format(paper_number))
                client.post_group(anon)

        if (index+1)%5 == 0 :
            print ('Processed paper ', index+1)

    print ('Processed ', paper_number)

