from collections import defaultdict
import csv
import sys, os
import re
import json

import openreview

from openreview_matcher.models import tfidf
from openreview_matcher import utils

client = openreview.Client()

# collect data from OpenReview.net
papers = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
reviewers = client.get_group('auai.org/UAI/2017/Program_Committee')
reviewer_expertise_notes = client.get_notes(invitation ='auai.org/UAI/2017/-/Reviewer_Expertise')
bids = client.get_tags(invitation = "auai.org/UAI/2017/-/Add/Bid")

def write_to_json(records, outfile):
    with open(outfile,'w') as f:
        for r in records:
            f.write(json.dumps(r) + '\n')

train_data = [utils.openreview_to_record(n) for n in papers]
test_data = [utils.openreview_to_record(n) for n in papers]

# For every reviewer, search for the reviewer's authored papers.
# For every authored paper, extract the title (and abstract, if available) and create a dictionary.
regex_strip = re.compile('~|[0-9]')

archive = []

for reviewer in reviewers.members:
    search_term = regex_strip.sub('', reviewer.replace('_',' '))
    search_results = client.search_notes(search_term, content='authors', source='forum') # add limit and offset
    if search_results:
        archive += [utils.openreview_to_record(n, reviewer=reviewer) for n in search_results]
    else:
        archive += [{'reviewer_id': reviewer, 'content': {'archive':""}}]

write_to_json(train_data, "../data/uai_train.json")
write_to_json(test_data, "../data/uai_test.json")
write_to_json(archive, "../data/uai_archive.json")

print "training TFIDF model..."
tfidf_model = tfidf.Model()
tfidf_model.fit(train_data=utils.SerializedData("../data/uai_train.json"), archive_data=utils.SerializedData("../data/uai_archive.json"))
print "saving to ../data/tfidf.pkl"
utils.save_obj(tfidf_model,'../data/tfidf.pkl')
