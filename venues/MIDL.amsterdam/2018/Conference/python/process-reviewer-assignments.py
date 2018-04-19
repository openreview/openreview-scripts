'''
processes the file "midl_assigned_reviews.csv", sent to us by Geert on April 16, 2018.

This script reformats the information in the above file in a format that
the assign-reviewers.py script can accept.
'''

import csv
new_rows = []
with open('../data/midl_assigned_reviews.csv') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        papernum = row[3]
        rev1 = row[7].lower()
        rev2 = row[8].lower()
        rev3 = row[9].lower()
        new_rows.append([rev1, papernum])
        new_rows.append([rev2, papernum])
        new_rows.append([rev3, papernum])

with open('../data/2018-04-17-midl-reviewer-assignments.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)
