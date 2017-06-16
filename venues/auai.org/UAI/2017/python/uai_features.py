from collections import defaultdict
from openreview_matcher import metadata


###############################################################################
## Paper-Reviewer features
###############################################################################

class SubjectAreaOverlap(metadata.OpenReviewFeature):
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
            max_denominator = max([len(user_subjects), len(forum_subjects)])

            if max_denominator > 0:
                return float(intersection) / float(max_denominator)
            else:
                return 0.0
        except KeyError:
            return 0.0

class PrimarySubjectOverlap(SubjectAreaOverlap):
    def __init__(self, name, data):
        SubjectAreaOverlap.__init__(self, name, data)
        self.subjectareas_by_signature = {n.signatures[0]: [n.content['primary area']] for n in self.data['subject_areas']}

class SecondarySubjectOverlap(SubjectAreaOverlap):
    def __init__(self, name, data):
        SubjectAreaOverlap.__init__(self, name, data)
        self.subjectareas_by_signature = {n.signatures[0]: n.content['additional areas'] for n in self.data['subject_areas']}


class BidScore(metadata.OpenReviewFeature):
    def __init__(self, name, data):
        """
        @data - a dict which has the following attributes:
            'bids': a dictionary of openreview.Tag objects that represent bids, keyed by user signature
            'bid_score_map': a dictionary of numerical scores, keyed by strings that represent possible bid responses
        """
        self.name = name
        self.data = data
        self.bids_by_signature = {bid.signatures[0]: bid for bid in self.data}

        self.bid_score_map ={
            "I want to review": 1.0,
            "I can review": 0.75,
            "I can probably review but am not an expert": 0.5,
            "I cannot review": 0.25,
            "No bid": 0.0
        }


    def score(self, signature, forum):
        """
        @signature - tilde ID of user
        @forum - forum of paper

        """

        try:
            bid = self.bids_by_signature[signature]
            score = self.bid_score_map[bid.tag]

            return score
        except:
            return 0.0


class ACRecommendation(metadata.OpenReviewFeature):
    def __init__(self, name, data):
        """
        @data - dict which has the following attributes:
            'recs': a list containing openreview.Tag objects that represent recommendations
        """
        self.name = name
        self.data = data
        self.recs_by_forum = defaultdict(list)
        for rec in self.data:
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

###############################################################################
## Reviewer-Reviewer features
###############################################################################

class UserAffinity(metadata.OpenReviewFeature):
    def __init__(self, name, data):
        """
        @data - dict which has the following attributes:
            'subject_areas': a dictionary of lists containing subject area keywords, keyed by user signature
            'papers': a list of openreview.Note objects
        """
        self.name = name
        self.data = data
        self.subjectareas_by_signature = {n.signatures[0]: n.content for n in self.data['subject_areas']}

    def score(self, signature, forum):
        """
        @signature - tilde ID of user
        @forum - forum of paper

        """
        try:
            user_subject_list = self.subjectareas_by_signature[signature]
            forum_subject_list = self.subjectareas_by_signature[forum]
            user_subjects = set(user_subject_list)
            forum_subjects = set(forum_subject_list)
            intersection = int(len(user_subjects & forum_subjects))
            max_denominator = max([len(user_subjects), len(forum_subjects)])

            if max_denominator > 0:
                return float(intersection) / float(max_denominator)
            else:
                return 0.0
        except KeyError:
            return 0.0

class PrimaryUserAffinity(UserAffinity):
    def __init__(self, name, data):
        UserAffinity.__init__(self, name, data)
        self.subjectareas_by_signature = {n.signatures[0]: [n.content['primary area']] for n in self.data['subject_areas']}

class SecondaryUserAffinity(UserAffinity):
    def __init__(self, name, data):
        UserAffinity.__init__(self, name, data)
        self.subjectareas_by_signature = {n.signatures[0]: n.content['additional areas'] for n in self.data['subject_areas']}


class ElasticSearchModel(metadata.OpenReviewFeature):
    def __init__(self, name, data):
        self.name = name
        self.model = data['model']
        self.papers_by_forum = {paper.to_json()['forum']:paper.to_json() for paper in data['papers']}

    def score(self, signature, forum):
        note_record = self.papers_by_forum[forum]
        return self.model.score(signature, note_record)

