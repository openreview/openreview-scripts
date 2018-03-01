import importlib
import openreview
import argparse
import csv
assign = importlib.import_module('assign-reviewer').assign

if __name__ == "__main__":

    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', required=True)
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print "connecting to ", client.baseurl

    failed_assignments = []

    with open(args.file) as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            paper_number = row[0]
            email = row[1]
            status = assign(client, paper_number, reviewer_to_add=email)
            if status == False:
                failed_assignments.append((paper_number, email))

    print "the following assignments were aborted: "
    for number, email in failed_assignments:
        print number, email
