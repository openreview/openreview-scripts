import argparse
import openreview
import datetime
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

    conference.open_decisions(
        options = ['Accept', 'Reject'],
        start_date = datetime.datetime(2019, 5, 12, 11, 59),
        due_date = datetime.datetime(2019, 5, 13, 23, 59))