import colt19
import argparse
import openreview

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    builder = openreview.conference.ConferenceBuilder(client)
    builder.set_conference_id(colt19.CONFERENCE_ID)
    builder.set_conference_name('Computational Learning Theory')
    builder.set_conference_short_name(colt19.SHORT_PHRASE)
    builder.set_homepage_header({
    'title': 'COLT 2019',
    'subtitle': 'Computational Learning Theory',
    'deadline': 'Submission Deadline: 11:00pm Pacific Standard Time, February 1, 2019',
    'date': 'June 25 - June 28, 2019',
    'website': 'http://learningtheory.org/colt2019/',
    'location': 'Phoenix, Arizona, United States'
    })
    builder.set_conference_type(openreview.builder.DoubleBlindConferenceType)
    builder.set_conference_reviewers_name(colt19.PROGRAM_CHAIRS_NAME)
    conference = builder.get_result()
    print('DONE.')
