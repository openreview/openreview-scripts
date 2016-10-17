import json


class Content():
    """Class defining the structure for the content for the note"""
    def __init__(self,minreviewers=0,maxreviewers=0,topics=None,reviewers=None,papers=None):
        self.minreviewers = minreviewers
        self.maxrevieweres=maxreviewers
        self.topics=topics
        self.reviewers=reviewers
        self.papers=papers



class Reviewer():
    """Class defining the structure of the reviewer"""
    def __init__(self,reviewer=None,score=0.0,source=None):
        self.reviewer=reviewer
        self.score=score
        self.source=source



class Paper(json.JSONEncoder):
    def __init__(self,paper=None,score=0.0,source=None):
        self.paper=paper
        self.score=score
        self.source =source


class NoteMetaData():
    def __init__(self,id,forum,replyto,invitation,signatures,nonreaders,content):
        self.id = id
        self.forum=forum
        self.replyto=replyto
        self.invitation=invitation
        self.content=content


class NoteReviewer():
    def __init__(self,id,members,writers,readers,nonreaders,content):
        self.id=id
        self.members=members
        self.writers=writers
        self.readers=readers
        self.nonreaders=nonreaders
        self.content=content



if __name__ == '__main__':
    paper = Paper("test1",0.2,"source1")
    content =Content(papers=list(paper))

    print json.dumps(content.__dict__)
