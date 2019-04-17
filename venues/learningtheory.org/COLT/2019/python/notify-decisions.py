import openreview
import argparse
import csv

acceptance_subject = 'COLT 2019 notification for Paper "<PAPER NUMBER>"'
acceptance_message = '''Dear Authors,

We are happy to inform you that Paper <PAPER NUMBER>, titled “<PAPER TITLE>”, has been accepted for presentation at COLT 2019. Congratulations!

We received 393 submissions this year, a record number. Many submissions were of very high quality, and it was a difficult process to narrow down the list of accepted papers. All accepted papers will be presented as a 10 minute talk and in a poster session.

We will contact you soon with details about preparing the camera-ready version of your paper for inclusion in the proceedings of the conference (including the extended abstract option), as well as details about the presentation format.

We are in the process of finalizing the reviews of all papers, to incorporate discussion by the program committee. We will make them visible to you on OpenReview in a few days. Note that these reviews will not be visible to the general public.

Please take the reviews of your paper into careful consideration. Please make sure that you follow up on all the revisions promised in your response.

We also remind you that at least one of the authors of your paper is expected to register and present the paper at COLT 2019. You can find the relevant registration information on the conference website. We advise participants who need a travel visa apply for it as soon as possible.

We are looking forward to seeing you in Phoenix on June 25-28 and hearing about your work!


Sincerely,
Alina Beygelzimer and Daniel Hsu
COLT 2019 Program Chairs
'''

rejection_subject = 'COLT 2019 notification for Paper "<PAPER NUMBER>"'
rejection_message = '''Dear Authors,

Thank you for submitting your work to COLT 2019.

We regret to inform you that Paper <PAPER NUMBER>, titled “<PAPER TITLE>”, was not accepted to the conference.

We received 393 submissions this year, a record number. Unfortunately, due to the constraints of the conference format, we had to reject many interesting and worthy papers.

We are in the process of finalizing the reviews of all papers, to incorporate discussion by the program committee. We will make them visible to you on OpenReview in a few days. Note that these reviews will not be visible to the general public.

None of the decisions were taken lightly, and the program committee have put significant effort to understand and compare the merits of different submissions. We do hope that this decision will not discourage you from submitting to COLT in the future, and that you will find the provided feedback useful.

We hope you will be able to join us in Phoenix on June 25-28 for the conference. Registration information is available on the conference webpage.


Sincerely,
Alina Beygelzimer and Daniel Hsu
COLT 2019 Program Chairs
'''


if __name__ == '__main__':

    program_chair_test_mode = True

    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile')
    parser.add_argument('--baseurl', help="in most cases, this should be \"https://openreview.net\"")
    parser.add_argument('--username', help="the email address that you use to log into OpenReview")
    parser.add_argument('--password', help="your OpenReview account password")
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    submission_by_number = {n.number: n for n in client.get_notes(
    invitation='learningtheory.org/COLT/2019/Conference/-/Blind_Submission')}
    original_by_forum = {n.forum: n for n in client.get_notes(
    invitation='learningtheory.org/COLT/2019/Conference/-/Submission')}

    with open(args.csvfile) as f:
        reader = csv.reader(f)
        for row in reader:
            paper_number = int(row[0].strip())
            decision = row[1].strip()
            try:
                blind_note = submission_by_number[paper_number]
                original = original_by_forum[blind_note.original]
                if (decision == 'Accept'):
                    formatted_subject = acceptance_subject.replace('<PAPER NUMBER>', str(blind_note.number))
                    formatted_message = acceptance_message.replace('<PAPER NUMBER>', str(blind_note.number))
                    formatted_message = formatted_message.replace('<PAPER TITLE>', blind_note.content['title'])
                    confirmed_recipients = client.send_mail(
                        formatted_subject,
                        original.content['authorids'] if not program_chair_test_mode else ['learningtheory.org/COLT/2019/Conference/Program_Chairs'],
                        formatted_message
                    )
                    print('Paper: {0} --> Decision: {1}, Email sent to: {2}'.format(str(paper_number), decision, confirmed_recipients))
                elif (decision == 'Reject'):
                    formatted_subject = rejection_subject.replace('<PAPER NUMBER>', str(blind_note.number))
                    formatted_message = rejection_message.replace('<PAPER NUMBER>', str(blind_note.number))
                    formatted_message = formatted_message.replace('<PAPER TITLE>', blind_note.content['title'])
                    confirmed_recipients = client.send_mail(
                        formatted_subject,
                        original.content['authorids'] if not program_chair_test_mode else ['learningtheory.org/COLT/2019/Conference/Program_Chairs'],
                        formatted_message
                    )
                    print('Paper: {0} --> Decision: {1}, Email sent to: {2}'.format(str(paper_number), decision, confirmed_recipients))
                else:
                    print ('Invalid decision provided for paper number {0}. Decision should be "Accept" or "Reject"'.format(str(paper_number)))

            except Exception as e:
                print ('An error occurred: ', e)
