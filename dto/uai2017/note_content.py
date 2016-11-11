import random


class ReviewerMeta():
    """
    Class defining the structure for the content for the note for reviewer meta data
    """

    def __init__(self, minreviewers=0, maxreviewers=0, topics=[], papers=[],reviewers=[]):
        self.minreviewers = minreviewers
        self.maxreviewers = maxreviewers
        self.topics = topics
        self.papers = papers
        self.reviewers=reviewers
        if minreviewers > maxreviewers:
            self.minreviewers = maxreviewers
            self.maxreviewers = minreviewers

    def to_dict(self):
        body = {
            'minreviewers': self.minreviewers,
            'maxreviewers': self.maxreviewers,
            'topics': self.topics,
            'papers': [x.to_dict() for x in self.papers],
            'reviewers' : [x.to_dict() for x in self.reviewers]
        }
        return body

    @staticmethod
    def create_samples(papers,reviewers,num_samples=10):
        samples = []
        sample_min_reviewers = [random.randint(1, num_samples * 10) for i in range(num_samples)]
        sample_max_reviewers = [random.randint(1, num_samples * 10) for i in range(num_samples)]
        sample_topics = ["topic" + str(random.randint(1, num_samples * 10)) for i in range(num_samples * 5)]
        sample_papers = Paper.create_samples(papers,num_samples=num_samples * 5)
        sample_reviewers = Reviewer.create_samples(reviewers,num_samples=num_samples*5,unique=True)
        for i in range(num_samples):
            samples.append(ReviewerMeta(sample_min_reviewers[i], sample_max_reviewers[i], sample_topics[5 * i:5 * i + 5],
                             sample_papers[5 * i:5 * i + 5],sample_reviewers[5 * i:5 * i + 5]))
        return samples


class ReviewerData():
    """
    Class defining the structure for the content for the note for reviewer data
    """

    def __init__(self, name=None,minpapers=0, maxpapers=0, topics=[], papers=[],reviewers=[]):
        self.name = name
        self.minpapers = minpapers
        self.maxpapers = maxpapers
        self.topics = topics
        self.papers = papers
        self.reviewers=reviewers
        if minpapers > maxpapers:
            self.minpapers = maxpapers
            self.maxpapers = minpapers

    def to_dict(self):
        body = {
            'name' : self.name ,
            'minpapers': self.minpapers,
            'maxpapers': self.maxpapers,
            'topics': self.topics,
            'papers': [x.to_dict() for x in self.papers],
            'reviewers' : [x.to_dict() for x in self.reviewers]
        }
        return body

    @staticmethod
    def create_samples(papers,reviewers,num_samples=10):
        samples = []
        if num_samples > len(reviewers):
            num_samples = len(reviewers)
        sample_min_papers = [random.randint(1, num_samples * 10) for i in range(num_samples)]
        sample_max_papers = [random.randint(1, num_samples * 10) for i in range(num_samples)]
        sample_topics = ["topic" + str(random.randint(1, num_samples * 10)) for i in range(num_samples * 5)]
        sample_papers = Paper.create_samples(papers,num_samples=num_samples * 5)
        for i  in range(len(reviewers)):
            sample_min_papers
            samples.append(ReviewerData(reviewers[i],random.sample(sample_min_papers,1), random.sample(sample_max_papers,1), random.sample(sample_topics,num_samples),
                             sample_papers,Reviewer.create_samples(reviewers[0:i]+reviewers[i+1:],5,unique=True)))
        return samples

class Paper():
    """
     Class defining the structure for the paper JSON
     """

    def __init__(self, paper=None, score=0.0, source=None):
        self.paper = paper
        self.score = score
        self.source = source

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def create_samples(paper_numbers,num_samples=10):
        samples = []
        if len(paper_numbers) < num_samples:
            num_samples = len(paper_numbers)
        samples_paper = random.sample(paper_numbers,num_samples)
        samples_score = [random.random() * num_samples for i in range(num_samples)]
        samples_source = ["source" + str(random.randint(1, num_samples * 10)) for i in range(num_samples)]
        for i in range(num_samples):
            samples.append(
                Paper(samples_paper[i], samples_score[i], samples_source[i])
            )
        return samples


class Reviewer():
    """
     Class defining the structure for the reviewer JSON
     """

    def __init__(self, reviewer=None, score=0, source=None):
        self.reviewer = reviewer
        self.score = score
        self.source = source

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def create_samples(reviewers,num_samples=10,unique=False):
        samples = []
        if len(reviewers)< num_samples:
            num_samples = len(reviewers)
        if unique:
            samples_reviewer = random.sample(reviewers,num_samples)
        else:
            samples_reviewer = random.sample(reviewers *random.randint(1,10), num_samples)
        samples_score = [random.random() * num_samples for i in range(num_samples)]
        samples_source = ["source" + str(random.randint(1, num_samples * 10)) for i in range(num_samples)]
        for i in range(num_samples):
            samples.append(
                Reviewer(samples_reviewer[i], samples_score[i], samples_source[i])
            )
        return samples


class PaperMetaData():
    """
    Class defining the structure of the content of the paper meta data
    """

    def __init__(self, minreviewers=0, maxreviewers=0, topics=[], reviewers=[], papers=[]):
        self.minreviewers = minreviewers
        self.maxreviewers = maxreviewers
        self.topics = topics
        self.reviewers = reviewers
        self.papers = papers
        if minreviewers > maxreviewers:
            self.minreviewers = maxreviewers
            self.maxreviewers = minreviewers

    def to_dict(self):
        body = {
            'minreviewers': self.minreviewers,
            'maxreviewers': self.maxreviewers,
            'topics': self.topics,
            'reviewers': [reviewer.to_dict() for reviewer in self.reviewers],
            'papers': [paper.to_dict() for paper in self.papers]
        }
        return body

    @staticmethod
    def create_samples(papers,reviewers,num_samples=10):
        samples = []
        sample_min_reviewers = [random.randint(1, num_samples * 10) for i in range(num_samples)]
        sample_max_reviewers = [random.randint(1, num_samples * 10) for i in range(num_samples)]
        sample_topics = ["topic" + str(random.randint(1, num_samples * 10)) for i in range(num_samples * 5)]
        sample_papers = Paper.create_samples(papers,num_samples * 5)
        sample_reviewers = Reviewer.create_samples(reviewers,num_samples * 5)
        for i in range(num_samples):
            samples.append(
                PaperMetaData(sample_min_reviewers[i], sample_max_reviewers[i], sample_topics[5 * i:5 * i + 5],
                              sample_reviewers[5 * i:5 * i + 5],
                              sample_papers[5 * i:5 * i + 5]))
        return samples
