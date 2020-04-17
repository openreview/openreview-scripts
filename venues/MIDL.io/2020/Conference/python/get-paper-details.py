import openreview
import argparse
from tqdm import tqdm
from collections import defaultdict
import csv

def get_pref_email(profile):
    pref_email = profile.content.get('preferredEmail')
    if not pref_email:
        pref_email = profile.content.get('emailsConfirmed')[0]
    return pref_email

def make_url(forum):
    return 'https://openreview.net/forum?id={}'.format(forum)

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base URL")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print ('connecting to {0}'.format(client.baseurl))

    all_submissions = list(openreview.tools.iterget_notes(
        client, 
        invitation='MIDL.io/2020/Conference/-/Blind_Submission',
        sort='number'
    ))

    map_num_to_sub = {note.number: note for note in all_submissions}
    map_forum_to_sub = {note.forum: note for note in all_submissions}
    
    full_paper_assigned = {'ac': defaultdict(int), 'reviewer': defaultdict(int)}
    short_paper_assigned = {'ac': defaultdict(int), 'reviewer': defaultdict(int)}

    map_member_to_pref_email= {}
    all_acs = client.get_group('MIDL.io/2020/Conference/Area_Chairs')
    ac_profiles = client.search_profiles(ids=all_acs.members)
    for profile in ac_profiles:
        map_member_to_pref_email[profile.id] = get_pref_email(profile)

    map_ac_grp_to_profile = {}
    map_num_to_ac = {}

    ac_grps = openreview.tools.iterget_groups(client, regex='^MIDL.io/2020/Conference/Paper[0-9]*/Area_Chair1$')
    for grp in ac_grps:
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        if paper_num in map_num_to_sub and grp.members:
            ac_member = grp.members[0]
            map_ac_grp_to_profile[grp.id] = ac_member
            map_num_to_ac[paper_num] = ac_member
            if map_num_to_sub[paper_num].content['track'] == 'short paper':
                short_paper_assigned['ac'][ac_member] += 1
            else:
                full_paper_assigned['ac'][ac_member] += 1


    all_reviewers = client.get_group('MIDL.io/2020/Conference/Reviewers').members
    tildes = [i for i in all_reviewers if i.startswith('~')]
    emails = [i for i in all_reviewers if not i.startswith('~')]

    for profile in client.search_profiles(ids=tildes):
        map_member_to_pref_email[profile.id] = get_pref_email(profile)
    for email,profile in client.search_profiles(emails=emails).items():
        map_member_to_pref_email[email] = get_pref_email(profile)

    map_reviewer_grp_to_profile = {}
    map_num_to_reviewers = defaultdict(list)

    reviewers = openreview.tools.iterget_groups(client, regex='^MIDL.io/2020/Conference/Paper[0-9]*/AnonReviewer[0-9]*$')
    for grp in reviewers:
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        if paper_num in map_num_to_sub and grp.members:
            member = grp.members[0]
            map_reviewer_grp_to_profile[grp.id] = member
            map_num_to_reviewers[paper_num].append(member)
            if map_num_to_sub[paper_num].content['track'] == 'short paper':
                short_paper_assigned['reviewer'][member] += 1
            else:
                full_paper_assigned['reviewer'][member] += 1

    map_ac_to_reviewed = defaultdict(dict)
    meta_revs = openreview.tools.iterget_notes(client, invitation = '^MIDL.io/2020/Conference/Paper[0-9]*/-/Meta_Review')
    for meta in tqdm(meta_revs):
        paper_num = int(meta.invitation.split('Paper')[1].split('/')[0])
        if paper_num in map_num_to_sub:
            ac_id = map_ac_grp_to_profile.get(meta.signatures[0], meta.signatures[0])
            map_ac_to_reviewed[ac_id][paper_num] = (meta, map_num_to_sub[paper_num].content['track'])


    map_reviewer_to_reviewed = defaultdict(dict)
    revs = openreview.tools.iterget_notes(client, invitation = '^MIDL.io/2020/Conference/Paper[0-9]*/-/Official_Review')
    for rev in tqdm(revs):
        paper_num = int(rev.invitation.split('Paper')[1].split('/')[0])
        if paper_num in map_num_to_sub:
            review_writer = rev.signatures[0]
            reviewer_id = map_reviewer_grp_to_profile.get(review_writer, review_writer)
            map_reviewer_to_reviewed[reviewer_id][paper_num] = (rev, map_num_to_sub[paper_num].content['track'])

    map_num_to_ranking = defaultdict(dict)
    map_ac_to_ranking = {'short': defaultdict(dict), 'full': defaultdict(dict)}
    ac_tags = list(openreview.tools.iterget_tags(client, invitation='MIDL.io/2020/Conference/Area_Chairs/-/Paper_Ranking'))
    for tag in ac_tags:
        if tag.forum in map_forum_to_sub:
            submission = map_forum_to_sub.get(tag.forum)
            if submission:
                map_num_to_ranking[submission.number][tag.signatures[0]] = tag
                if submission.content['track'] == 'short paper':
                    map_ac_to_ranking['short'][tag.signatures[0]][tag.forum] = tag
                else:
                    map_ac_to_ranking['full'][tag.signatures[0]][tag.forum] = tag
    
    reviewer_tags = list(openreview.tools.iterget_tags(client, invitation='MIDL.io/2020/Conference/Reviewers/-/Paper_Ranking'))
    map_reviewer_to_ranking = {'short': defaultdict(dict), 'full': defaultdict(dict)}
    for tag in reviewer_tags:
        if tag.forum in map_forum_to_sub:
            submission = map_forum_to_sub.get(tag.forum)
            if submission:
                map_num_to_ranking[submission.number][tag.signatures[0]] = tag
                if submission.content['track'] == 'short paper':
                    map_reviewer_to_ranking['short'][tag.signatures[0]][tag.forum] = tag
                else:
                    map_reviewer_to_ranking['full'][tag.signatures[0]][tag.forum] = tag

    quality_notes = openreview.tools.iterget_notes(client, invitation='^MIDL.io/2020/Conference/Paper[0-9]*/AnonReviewer[0-9]*/-/Review_Rating$')
    map_paper_to_reviewer_quality = defaultdict(dict)
    for note in quality_notes:
        anonrev = note.invitation.split('/-/')[0]
        paper_num = int(note.invitation.split('Paper')[1].split('/')[0])
        member = map_reviewer_grp_to_profile.get(anonrev)
        if member:
            map_paper_to_reviewer_quality[paper_num][member] = note.content['review_quality']


    with open('midl-short-paper-details.csv', 'w') as f, open('midl-full-paper-details.csv', 'w') as f2:
        header = ['Paper#', 'Paper Url', 'AC user id', 'AC email', 'Metareview available', 'Rating', 'Metareview comment', 'Paper ranking by AC available', 'Paper rank by AC', 'Review Quality Ratings Count', 'Count of papers ranked by AC', 'Reviewer user id', 'Reviewer email', 'Review available', 'Review rating', 'Review confidence', 'Review comment', 'Paper ranking by reviewer available', 'Paper rank by reviewer', 'Review Quality', 'Count of papers ranked by reviewer', 'Reviewer user id', 'Reviewer email', 'Review available', 'Review rating', 'Review confidence', 'Review comment', 'Paper ranking by reviewer available', 'Paper rank by reviewer', 'Review Quality', 'Count of papers ranked by reviewer', 'Reviewer user id', 'Reviewer email', 'Review available', 'Review rating', 'Review confidence', 'Review comment', 'Paper ranking by reviewer available', 'Paper rank by reviewer', 'Review Quality', 'Count of papers ranked by reviewer', 'Reviewer user id', 'Reviewer email', 'Review available', 'Review rating', 'Review confidence', 'Review comment', 'Paper ranking by reviewer available', 'Paper rank by reviewer', 'Review Quality', 'Count of papers ranked by reviewer', 'Reviewer user id', 'Reviewer email', 'Review available', 'Review rating', 'Review confidence', 'Review comment', 'Paper ranking by reviewer available', 'Paper rank by reviewer', 'Review Quality', 'Count of papers ranked by reviewer']
        csv_writer = csv.writer(f)
        csv_writer2 = csv.writer(f2)
        csv_writer.writerow(header)
        csv_writer2.writerow(header)

        for paper_num, paper in map_num_to_sub.items():
            ac = map_num_to_ac[paper_num]
            ac_email = map_member_to_pref_email.get(ac, '')

            paper_rankings = map_num_to_ranking.get(paper_num, [])
            ac_rank = paper_rankings.get(ac) if paper_rankings else None

            ac_meta_reviews = map_ac_to_reviewed.get(ac, [])
            paper_meta_review = ac_meta_reviews.get(paper_num) if ac_meta_reviews else None
            if paper_meta_review:
                paper_meta_review = paper_meta_review[0]
            metareview_comment_field = 'metareview' if paper.content['track'] == 'short paper' else 'metaReview'

            paper_reviewer_ratings = map_paper_to_reviewer_quality.get(paper_num, [])
            paper_type = 'short' if map_num_to_sub[paper_num].content['track'] == 'short paper' else 'full'

            csv_row = [
                str(paper_num),
                make_url(paper.forum),
                ac,
                ac_email,
                '1' if paper_meta_review else '0',
                paper_meta_review.content['rating'] if paper_meta_review else '',
                paper_meta_review.content[metareview_comment_field] if paper_meta_review else '',
                '1' if ac in paper_rankings else '0',
                ac_rank.tag if ac_rank else '',
                str(len(paper_reviewer_ratings)),
                str(len(map_ac_to_ranking[paper_type].get(ac, [])))
            ]

            paper_reviewers = map_num_to_reviewers.get(paper_num, [])
            for rev in paper_reviewers:
                rev_email = map_member_to_pref_email.get(rev, '')

                reviewer_rank = paper_rankings.get(rev)
                reviewer_ranking_status = '1' if reviewer_rank else '0'

                reviewers_reviews = map_reviewer_to_reviewed.get(rev, [])
                paper_review_tuple = reviewers_reviews.get(paper_num) if reviewers_reviews else None
                paper_review = paper_review_tuple[0] if paper_review_tuple else None

                review_comment_field = 'review' if paper.content['track'] == 'short paper' else 'justification_of_rating'
                review_quality = paper_reviewer_ratings.get(rev, '') if paper_reviewer_ratings else ''

                csv_row.extend([
                    rev,
                    rev_email,
                    '1' if paper_review else '0',
                    paper_review.content['rating'] if paper_review else '',
                    paper_review.content['confidence'] if paper_review else '',
                    paper_review.content[review_comment_field] if paper_review else '',
                    reviewer_ranking_status,
                    reviewer_rank.tag if reviewer_rank else '',
                    review_quality,
                    str(len(map_reviewer_to_ranking[paper_type].get(rev, [])))
                ])
            if paper.content['track'] == 'short paper':
                csv_writer.writerow(csv_row)
            else:
                csv_writer2.writerow(csv_row)