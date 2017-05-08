from collections import defaultdict
from openreview_matcher import features

class SubjectAreaOverlap(features.OpenReviewFeature):
    def __init__(self, name, data):
        """
        @data - dict which has the following attributes:
            'subject_areas': a dictionary of lists containing subject area keywords, keyed by user signature
            'papers': a list of openreview.Note objects
        """
        self.name = name
        self.data = data
        self.subjectareas_by_signature = {n.signatures[0]: n.content for n in self.data['subject_areas']}
        self.papers_by_forum = {p.forum: p for p in self.data['papers']}

    def score(self, signature, forum):
        """
        @signature - tilde ID of user
        @forum - forum of paper

        """


        try:
            user_subject_list = self.subjectareas_by_signature[signature]
            paper_subject_list = self.papers_by_forum[forum].content['subject areas']

            user_subjects = set(user_subject_list)
            forum_subjects = set(paper_subject_list)
            intersection = int(len(user_subjects & forum_subjects))
            max_denominator = max([int(len(s)) for s in [user_subjects, forum_subjects]])

            if max_denominator > 0:
                return intersection / max_denominator
            else:
                return 0.0
        except:
            return 0.0


class BidScore(features.OpenReviewFeature):
    def __init__(self, name, data):
        """
        @data - a dict which has the following attributes:
            'bids': a dictionary of openreview.Tag objects that represent bids, keyed by user signature
            'bid_score_map': a dictionary of numerical scores, keyed by strings that represent possible bid responses
        """
        self.name = name
        self.data = data
        self.bids_by_signature = {bid.signatures[0]: bid for bid in self.data['bids']},

    def score(self, signature, forum):
        """
        @signature - tilde ID of user
        @forum - forum of paper

        """

        bid_score_map = self.data['bid_score_map']
        try:
            bid = self.bids_by_signature[signature]
            score = bid_score_map[bid.tag]

            return score
        except:
            return 0.0


class ACRecommendation(features.OpenReviewFeature):
    def __init__(self, name, data):
        """
        @data - dict which has the following attributes:
            'recs': a list containing openreview.Tag objects that represent recommendations
        """
        self.name = name
        self.data = data
        self.recs_by_forum = defaultdict(list)
        for rec in self.data['recs']:
            self.recs_by_forum[rec.forum] += [rec]

    def score(self, signature, forum):
        """
        @signature - tilde ID of user
        @forum - forum of paper

        """


        recs = self.recs_by_forum[forum]
        recommended_users = [rec.tag for rec in recs]

        if signature in recommended_users:
            return 1.0
        else:
            return 0.0
