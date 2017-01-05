import openreview
import requests
import sys, getopt

class PaperStatus:
    Unassigned, Assigned, Commented, Reviewed, FullyReviewed = range(5)


PaperStatusString = ["Unassigned", "Assigned", "Commented", "Reviewed", "FullyReviewed"]


# get the info from the review, return NA if not there
def get_score(content_type):
    string_var = note.content.get(content_type, "NA")
    string_var = string_var.split(':')[0]
    return string_var


# output_type: 1 text
#               2 cvs
#               3 html
output_type = 2
file_name = "output.txt"
# parse optional arguments
try:
  opts, args = getopt.getopt(sys.argv[1:],"ho:t:",["ofile=","type="])
except getopt.GetoptError:
  print 'temp.py -o <outputfile> -t <type> 1: text, 2: csv'
  sys.exit(2)

for opt, arg in opts:
  if opt == '-h':
    print 'temp.py -o <outputfile> -t <type>'
    sys.exit()
  elif opt in ("-t", "--type"):
    try:
        output_type = int(arg)
    except ValueError:
        print 'Type must be 1 (for text) or 2 (for csv).'
        sys.exit()
    if (output_type is not 1) and (output_type is not 2):
        print 'Type must be 1 (for text) or 2 (for csv).'
        sys.exit()
  elif opt in ("-o", "--ofile"):
    file_name = arg
my_file = open(file_name, "w")


client = openreview.Client(username='OpenReview.net', password='OpenReview_beta', baseurl='https://openreview.net')
# client = openreview.Client(username='OpenReview.net', password='OpenReview_beta', baseurl='http://localhost:3000')
submissions = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')

invitation = "official/review"
headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + client.token}
anon_reviewers = requests.get(client.baseurl + '/groups?id=ICLR.cc/2017/conference/paper.*/AnonReviewer.*',
                              headers=headers)
current_reviewers = requests.get(client.baseurl + '/groups?id=ICLR.cc/2017/conference/paper.*/reviewers',
                                 headers=headers)
notes = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/' + invitation)

# The following are dictionaries to connect the papers, reviewers and reviews
# 	the signature is the whole directory struct leading up to the Anonymized name
# 	ex ICLR.cc/2017/conference/-/paper203/AnonReviewer1
# reviews[signature] = the review note
reviews = {}
# reviewers[signature] = reviewer_name
reviewers = {}
# reviewers_by_paper[paper_num][reviewer_name] = review
reviewers_by_paper = {}
# paper_status[paper_num] dictionary w/ 'title' (paper title),'count'(number of reviewers),
#													 'reviewed',  'percent'(percentage reviewed)
paper_status = {}

# initialize paper_status for each submission and attach title to paper number
for paper in submissions:
    paper_status[paper.number] = {}
    paper_status[paper.number]['title'] = paper.content['title']
    paper_status[paper.number]['count'] = 0
    paper_status[paper.number]['reviewed'] = 0
    paper_status[paper.number]['percent'] = 0
    reviewers_by_paper[paper.number] = {}

# attach review note to the anonymized name
for n in notes:
    signature = n.signatures[0]
    reviews[signature] = n

# attach real name to the anonymized name
for r in anon_reviewers.json():
    reviewer_id = r['id']
    members = r['members']
    if members:
        reviewers[reviewer_id] = members[0]
    else:
        paper_num = int(reviewer_id.split('paper')[1].split('/Anon')[0])
        if paper_num in paper_status:
            # check if paper wasn't deleted then why is reviewer missing?
            if output_type == 1:
                my_file.write('Reviewer ' + reviewer_id + ' is anonymous\n')
            else:
                print('Reviewer ' + reviewer_id + ' is anonymous')

# attach reviewers to paper_num
# add review status paper_status
for r in current_reviewers.json():
    reviewer_id = r['id']
    members = r['members']
    if members:
        paper_num = int(reviewer_id.split('paper')[1].split('/reviewers')[0])
        if paper_num in paper_status:
            # if the number isn't in paper_status it means the submission was deleted
            for m in members:
                # add reviewers
                reviewer_name = reviewers.get(m, m)
                reviewers_by_paper[paper_num][reviewer_name] = reviews.get(m, None)
                paper_status[paper_num]['count'] += 1
                if reviewers_by_paper[paper_num][reviewer_name] != None:
                    paper_status[paper_num]['reviewed'] += 1

# now that all reviewers have been added to the paper_status
# for each paper determine how many reviewers have completed reviewing
for paper_num in paper_status:
    paper_status[paper_num]['percent'] = 100 * paper_status[paper_num]['reviewed'] / paper_status[paper_num][
        'count']

# sort on % complete (doesn't like being sorted in place)
paper_status_sorted = sorted(paper_status, key=lambda x: (paper_status[x]['percent'], x))


# print results
if output_type == 1:
    # text
    for paper_num in paper_status_sorted:
            my_file.write("%s: %s%% %s\n" % (
                paper_num, paper_status[paper_num]['percent'], paper_status[paper_num]['title']))
            reviewers = reviewers_by_paper[paper_num]
            for reviewer, note in reviewers.iteritems():
                if note:
                    my_file.write("   reviewer: %s  " % (reviewer.encode('utf-8')))
                    my_file.write("  rating: %s  confidence: %s\n" % (get_score('rating'), get_score('confidence')))
                else:
                    my_file.write("   reviewer: %s  UNREVIEWED\n" % reviewer)

elif output_type == 2:
    # csv
    my_file.write("Paper Number, %Review Complete, Reviewer Name, Review Rating, Review Confidence\n")
    for paper_num in paper_status_sorted:
        reviewers = reviewers_by_paper[paper_num]
        for reviewer, note in reviewers.iteritems():
            my_file.write("%s, %s%%, " % (paper_num, paper_status[paper_num]['percent']))
            my_file.write(reviewer.encode('utf-8'))
            if note:
                my_file.write(", %s, %s\n" % (get_score('rating'), get_score('confidence')))
            else:
                my_file.write(", 0, 0\n")


my_file.close()
