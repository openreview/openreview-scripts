'''

'''

import argparse
import openreview
import iclr19
import invitations
import notes


oral_template = '''
Dear Author,


We are very pleased to inform you that your ICLR 2019 submission {number} - {title} has been accepted as an oral presentation. Your area chair's meta-review has been posted in OpenReview.


You should now prepare the deanonymised camera ready version of your contribution, which should include inserting the statement \iclrfinalcopy in your LaTeX source file.


We ask that you update your paper on OpenReview with this latest version no later than February 22nd, 2019.


https://openreview.net/forum?id={forum}&noteId={noteId}


Please don't forget to make your travel arrangements. Registration for the conference will open on January 29, 2019, and you can register directly through the conference website https://iclr.cc/. There, you will also find suggestions for local accommodation.


Note that at least one author for each paper must be registered for ICLR 2019.


We received 1591 submissions. Out of these we accepted only 24 for oral presentation (1.5%) and 500 for poster presentation (31%).


Congratulations and thank you for your contribution.


We look forward to seeing you in New Orleans!


Alexander, Karen, Sergey, and Shakir -- the ICLR 2019 program committee
'''

poster_template = '''
Dear Author,


We are pleased to inform you that your ICLR 2019 submission {number} - {title} has been accepted as a poster presentation. Your area chair's meta-review has been posted in OpenReview.


You should now prepare the deanonymised camera ready version of your contribution, which should include inserting the statement \iclrfinalcopy in your LaTeX source file.


We ask that you update your paper on OpenReview with this latest version no later than February 22nd, 2019.


https://openreview.net/forum?id={forum}&noteId={noteId}


Please don't forget to make your travel arrangements. Registration for the conference will open on January 29, 2019, and you can register directly through the conference website https://iclr.cc/. There, you will also find suggestions for local accommodation.


Note that at least one author for each paper must be registered for ICLR 2019.


We received 1591 submissions. Out of these we accepted only 24 for oral presentation (1.5%) and 500 for poster presentation (31%).


Congratulations and thank you for your contribution.


We look forward to seeing you in New Orleans!


Alexander, Karen, Sergey, and Shakir -- the ICLR 2019 program committee
'''

reject_template = '''
Dear Author,


We regret to inform you that your ICLR 2019 submission {number} - {title} was not accepted. Your area chair's meta-review has been posted in OpenReview.

https://openreview.net/forum?id={forum}&noteId={noteId}


We received 1591 submissions. Out of these we accepted only 24 for oral presentation (1.5%) and 500 for poster presentation (31%).


Thank you for your interest in the conference, and we hope you'll nevertheless consider joining us in New Orleans.


Alexander, Karen, Sergey, and Shakir -- the ICLR 2019 program committee
'''


def send_email(client, submission, metareview):

    template = None

    if 'Oral' in metareview.content['recommendation']:
        template = oral_template
    if 'Poster' in metareview.content['recommendation']:
        template = poster_template
    if 'Reject' in metareview.content['recommendation']:
        template = reject_template

    if template:
        message = template.format(number = submission.number, title = submission.content['title'], forum = submission.forum, noteId = metareview.id)
        client.send_mail(subject = 'ICLR 2019 Decision', recipients = submission.content['authorids'], message = message)
    else:
        print('Template error', submission)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    # print('Update invitations...')
    # meta_reviews_invitations = list(openreview.tools.iterget_invitations(client, regex = 'ICLR.cc/2019/Conference/-/Paper.*/Meta_Review'))
    # for i in meta_reviews_invitations:
    #     i.reply['readers']['values'] = ['everyone']
    #     client.post_invitation(i)


    # print('Post decisions...')
    meta_reviews = list(openreview.tools.iterget_notes(client, invitation = 'ICLR.cc/2019/Conference/-/Paper.*/Meta_Review'))
    # submissions = list(openreview.tools.iterget_notes(client, invitation = 'ICLR.cc/2019/Conference/-/Blind_Submission', details = 'original'))
    # submissions_dict = {}
    # for s in submissions:
    #     submissions_dict[s.id] = s
    # for m in meta_reviews:
    #     if m.forum in submissions_dict:
    #         submission = submissions_dict[m.forum]
    #         m.readers = ['everyone']
    #         if m.content['recommendation'] == 'Invite to Workshop Track':
    #             m.content['recommendation'] = 'Reject'
    #         client.post_note(m)


    # # Release authors names
    # print('Release author names...')
    # meta_reviews = list(openreview.tools.iterget_notes(client, invitation = 'ICLR.cc/2019/Conference/-/Paper.*/Meta_Review'))
    # for m in meta_reviews:
    #     if m.forum in submissions_dict:
    #         submission = submissions_dict[m.forum]
    #         decision = m.content['recommendation']
    #         original_note = openreview.Note.from_json(submission.details['original'])
    #         if 'Reject' in decision:
    #             accepted = False

    #         if decision in ['Oral', 'Poster']:
    #             accepted = True

    #         overwriting_note = openreview.Note(
    #             id = submission.id,
    #             original = submission.original,
    #             invitation = iclr19.BLIND_SUBMISSION_ID,
    #             forum = submission.forum,
    #             signatures = [iclr19.CONFERENCE_ID],
    #             writers = [iclr19.CONFERENCE_ID],
    #             readers = ['everyone'],
    #             content = {
    #                 '_bibtex': openreview.tools.get_bibtex(
    #                     original_note,
    #                     'International Conference on Learning Representations',
    #                     '2019',
    #                     url_forum=submission.forum,
    #                     accepted=accepted,
    #                     anonymous=False)
    #                 })
    #         client.post_note(overwriting_note)

    #         if accepted:
    #             revision_invitation = client.get_invitation(id = '{conference_id}/-/Paper{number}/Revision'.format(conference_id = iclr19.CONFERENCE_ID, number = submission.number))
    #             revision_invitation.expdate = 1576843200000
    #             client.post_invitation(revision_invitation)

    # # Update home page
    # print('update home page...')
    # home_group = client.get_group(iclr19.CONFERENCE_ID)
    # with open('../webfield/conferenceWebfield_decision_tabs.js') as f:
    #     content = f.read()
    #     home_group.web = content
    #     client.post_group(home_group)

    # Send emails to authors
    print('Send emails to authors...')
    submissions = list(openreview.tools.iterget_notes(client, invitation = 'ICLR.cc/2019/Conference/-/Blind_Submission', details = 'original'))
    submissions_dict = {}
    for s in submissions:
        submissions_dict[s.id] = s

    for m in meta_reviews:
        if m.forum in submissions_dict:
            submission = submissions_dict[m.forum]
            send_email(client, submission, m)

