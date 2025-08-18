import openreview
import argparse
import datetime
import logging

'''
Requirements:

openreview-py

Usage:

Use the --paper (or -p) flag to specify the paper number.
Use the --type (or -t) flag to specify the role of the user which can be 'pc' or 'spc'.
Use the --add (or -a) flag to specify a username or email address to assign.
Use the --remove (or -r) flag to specify a username or email address to remove.

The script processes removals before additions, and assigns the user to the
lowest AnonReviewer# group that is empty.

For example, after running the following:

python reassign.py -p 123 -r ~Oriol_Vinyals1 -a ~MarcAurelio_Ranzato1 --baseurl https://openreview.net --username <> --password <>


Paper123/Reviewers = {
    AnonReviewer1: ~Tara_Sainath1
    AnonReviewer2: ~Oriol_Vinyals1
    AnonReviewer3: ~Iain_Murray1
}

becomes

Paper123/Reviewers = {
    AnonReviewer1: ~Tara_Sainath1
    AnonReviewer2: ~MarcAurelio_Ranzato1
    AnonReviewer3: ~Iain_Murray1
}
'''

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename = 'log.out', format='%(asctime)s - %(message)s')
    logging.info('Begin Logging')

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--paper', required=True)
    parser.add_argument('-t', '--type', required=True, )
    parser.add_argument('-a', '--add')
    parser.add_argument('-r', '--remove')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    client = openreview.Client(
        baseurl=args.baseurl, username=args.username, password=args.password)
    logging.info('{0} logged in on {1}'.format(args.username, client.baseurl))

    paper_number = args.paper
    member_type = args.type
    member_to_remove = args.remove
    member_to_add = args.add

    logging.info('Arguments provided: Paper Number:{paper_number}'.format(paper_number=paper_number))
    logging.info('Arguments provided: Member Type:{member_type}'.format(member_type=member_type))
    logging.info('Arguments provided: Member to remove:{member_to_remove}'.format(member_to_remove=member_to_remove))
    logging.info('Arguments provided: Member to add:{member_to_add}'.format(member_to_add=member_to_add))

    conference_id = 'auai.org/UAI/2019/Conference'
    result = []

    if member_type not in ['spc', 'pc']:
        logging.error('Invalid member type! Member type can only be "spc" or "pc"')

    elif (member_type == 'pc'):
        try:
            result = openreview.tools.assign(
                client=client,
                conference=conference_id,
                paper_number=paper_number,
                reviewer_to_add=member_to_add,
                reviewer_to_remove=member_to_remove,
                parent_label='Reviewers',
                individual_label='AnonReviewer',
                individual_group_params={
                    'readers': [
                        conference_id,
                        conference_id + '/Program_Chairs',
                        conference_id + '/Paper{0}/Area_Chairs'.format(
                            paper_number)
                    ]},
                parent_group_params={
                    'readers': [
                        conference_id,
                        conference_id + '/Program_Chairs',
                        conference_id + '/Paper{0}/Area_Chairs'.format(
                            paper_number)
                    ],
                    'signatories': [conference_id + '/Paper{0}/Reviewers'.format(paper_number)]
                }
            )
        except Exception as e:
             logging.error("Exception occurred", exc_info=True)

    else:
        try:
            result = openreview.tools.assign(
                client=client,
                conference=conference_id,
                paper_number=paper_number,
                reviewer_to_add=member_to_add,
                reviewer_to_remove=member_to_remove,
                parent_label='Area_Chairs',
                individual_label='Area_Chair',
                individual_group_params={
                    'readers': [
                        conference_id,
                        conference_id + '/Program_Chairs'
                    ]},
                parent_group_params={
                    'readers': [
                        conference_id,
                        conference_id + '/Program_Chairs',
                    ]
                }
            )
        except Exception as e:
             logging.error("Exception occurred", exc_info=True)

    if result:
        print('result: ', result)
        logging.info('result: {}'.format(result))

    logging.info('End Logging')