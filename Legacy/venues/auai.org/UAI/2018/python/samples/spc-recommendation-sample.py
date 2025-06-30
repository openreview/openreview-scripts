import openreview
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

papers = client.get_notes(invitation='auai.org/UAI/2018/-/Submission')

recommendations_by_forum = {}

for p in papers:
    recs = client.get_tags(invitation='auai.org/UAI/2018/-/Paper{}/Recommend_Reviewer'.format(p.number))

    '''
    you may want to sort the recommendations by cdate.
    this will let you determine the order in which the SPC member entered their recommendation.
    (this is useful if, for example, you instructed the SPCs to enter recommendations in
    order of preference)
    '''
    recommendations_by_forum[p.id] = sorted(recs, key=lambda x: x.cdate)

# get an example recommendation by its paper forum ID:
example_paper = papers[0]
example_paper_recommendations = recommendations_by_forum[example_paper.id]

# show that the recommendations are ordered
# the "tag" field of a recommendation will contain the recommended reviewer's ID
print "showing recommendations for [{}]: \"{}\"".format(example_paper.id, example_paper.content['title'])
for i in example_paper_recommendations:
    print i.cdate, i.tag

