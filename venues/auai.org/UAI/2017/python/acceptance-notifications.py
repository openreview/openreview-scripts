import openreview
from uaidata import *
import re
import argparse

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')


def get_oral_accept_message(recipient_names, paper_forum, paper_title, paper_number):
    subject = "UAI 2017: Accept Notification"

    msg = """
    Dear {0},

    Thank you for submitting the following paper to the 33rd Conference on Uncertainty in Artificial Intelligence (UAI 2017):

    Paper{3} - {2}

    Congratulations!  Your submission has been accepted for plenary presentation. A total of 289 papers were submitted to UAI this year, of which 282 were reviewed (after summary rejections, etc.), and of which 87 were accepted. The acceptance rate is close to 31%.

    The camera-ready version of your paper is due on July 11th,11:59 pm SST (Samoa Standard Time). Instructions, together with a copyright form, will be sent shortly. Please carefully consider the reviews and meta-review of your paper when preparing your final version. These are available at https://openreview.net/forum?id={1} .

    Each plenary presentation is allocated about 20 minutes, including Q&A (we will notify you of the exact time once the schedule is finalized). In addition to the plenary talk, you are encouraged to contribute a poster on your paper to the poster session. Instructions for poster preparation will be sent to you later.

    Please note that at least one author of an accepted paper must register for the conference and present the paper. The conference registration system will be open soon.  A block of rooms have been reserved for UAI 2017 at the
    Hyatt Regency Sydney. See http://auai.org/uai2017/hotel.php for details, a reservation link, as well as other hotels near the conference.

    The conference has a strong program of tutorials, keynote talks, and workshops - see the website http://auai.org/uai2017 for full details.

    We look forward to seeing you at UAI 2017 in Sydney!

    Gal Elidan and Kristian Kersting
    UAI 2017 Program Chairs
    uai2017chairs@gmail.com
    """.format(recipient_names, paper_forum, paper_title, paper_number)

    return subject, msg


def get_poster_accept_message(recipient_names, paper_forum, paper_title, paper_number):
    subject = 'UAI 2017: Accept Notification'

    msg = """
    Dear {0},

    Thank you for submitting the following paper to the 33rd Conference on Uncertainty in Artificial Intelligence (UAI 2017):

    Paper{3} - {2}

    Congratulations!  Your submission has been accepted for poster presentation. A total of 289 papers were submitted to UAI this year, of which 282 were reviewed (after summary rejections, etc.), and of which 87 were accepted. The acceptance rate is close to 31%.

    The camera-ready version of your paper is due on July 11th,11:59 pm SST (Samoa Standard Time). Instructions, together with a copyright form, will be sent shortly. Please carefully consider the reviews and meta-review of your paper when preparing your final version. These are available at https://openreview.net/forum?id={1} .

    Instructions for poster preparation will be sent to you later. You are expected to give a 1 minute oral poster spotlight presentation prior to the poster presentation.

    Please note that at least one author of an accepted paper must register for the conference and present the paper. The conference registration system will be open soon. A block of rooms have been reserved for UAI 2017 at the
    Hyatt Regency Sydney. See http://auai.org/uai2017/hotel.php for details, a reservation link, as well as other hotels near the conference.

    The conference has a strong program of tutorials, keynote talks, and workshops - see the website http://auai.org/uai2017 for full details.

    We look forward to seeing you at UAI 2017 in Sydney!

    Gal Elidan and Kristian Kersting
    UAI 2017 Program Chairs
    uai2017chairs@gmail.com
    """.format(recipient_names, paper_forum, paper_title, paper_number)

    return subject, msg

def get_reject_message(recipient_names, paper_forum, paper_title, paper_number):
    subject = 'UAI 2017: Author Notification'

    msg = """
    Dear {0},

    Thank you for submitting the following paper to the 33rd Conference on Uncertainty in Artificial Intelligence (UAI 2017):

    Paper{3} - {2}

    Unfortunately, your submission has not been accepted for inclusion in the conference. We had a strong set of submitted papers this year and the selection process was very competitive. Each paper was reviewed by at least 3 reviewers and only 87 (31%) of the 282 submissions that were reviewed were accepted.

    We encourage you to log on to https://openreview.net/forum?id={1} We hope you will find these comments useful.

    Although your paper was not accepted we hope nonetheless that you will consider attending the conference in August.  The conference registration system will be open soon.  A block of rooms have been reserved for UAI 2017 at the
    Hyatt Regency Sydney. See http://auai.org/uai2017/hotel.php for details, a reservation link, as well as other hotels near the conference.

    The conference has a strong program of tutorials, keynote talks, and workshops - see the website http://auai.org/uai2017 for full details.

    We look forward to seeing you at UAI 2017 in Sydney!

    Gal Elidan and Kristian Kersting
    UAI 2017 Program Chairs
    uai2017chairs@gmail.com

    """.format(recipient_names, paper_forum, paper_title, paper_number)

    return subject, msg

def prettyId(signature):
    signature = signature.replace('~','')
    signature = signature.replace('_',' ')
    return re.sub('[0-9]','',signature)

for n in submissions:
    decision = client.get_notes(invitation=CONFERENCE + '/-/Paper' + str(n.number) + '/Acceptance/Decision')[0]
    original = client.get_note(n.original)

    if len(original.content['authors']) > 1:
        recipient_names = ', '.join(original.content['authors'][0:len(original.content['authors'])-1])
        recipient_names += (', and ' + original.content['authors'][-1])
        recipient_names = recipient_names.encode('utf-8')
    else:
        recipient_names = original.content['authors'][0].encode('utf-8')

    paper_number = str(n.number)
    paper_forum = n.forum
    paper_title = n.content['title'].encode('utf-8')

    if decision.content['decision'] == 'Accept (Oral)':
        get_message = get_oral_accept_message
    if decision.content['decision'] == 'Accept (Poster)':
        get_message = get_poster_accept_message
    if decision.content['decision'] == 'Reject':
        get_message = get_reject_message

    print "Sending {0} message to: {1}".format(decision.content['decision'], recipient_names)

    try:
        subject, message = get_message(recipient_names, paper_forum, paper_title, paper_number)
    except UnicodeEncodeError as e:
        print recipient_names, paper_forum, paper_title, paper_number
        raise e

    client.send_mail(subject, original.content['authorids'], message)
