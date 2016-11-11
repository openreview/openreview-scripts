import os
import sys
import json
import argparse
from openreview import *
sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
print sys.path
from note_content import *
from constants import *
from lxml import etree

"""
Parse the arguments for user authentication
"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()
if args.username != None and args.password != None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)


def get_paper_names(notes):
    """
    Getting paper name using the following logic: If note.number is NONE then throw an error else 'Paper' followed by its number
    :param notes:
    :return:
    """
    list_paper_name = []
    for note in notes:
        if (note.number is None):
            raise ValueError("No note number for note id : %s" %(note.id))
        else:
            list_paper_name.append("Paper" + str(note.number))
    return list_paper_name


def get_notes_submitted_papers():
    """
    Get all the submitted papers
    :return:
    """
    notes = openreview.get_notes(invitation=CONFERENCE_SUBMISSION)
    return notes


def get_paper_metadata_notes(paper_names):
    """
    Get all submitted paper meta data notes
    :return:
    """
    notes = [openreview.get_notes(invitation=CONFERENCE + "/" + paper_name + "/-/matching")[0] for paper_name in
             paper_names]
    return notes


def get_submitted_paper_details(submitted_paper_notes):
    """
    Get details of all the papers submitted in a list
    :param submitted_paper_notes:
    :return:
    """
    paper_details_list=[]
    paper_details_list.append(["Paper ID","Paper Title","Abstract","Author Names","Author Emails","Subject Areas","Conflict Reasons",
                               "Files","Supplementary File","Related Submissions","AC suggestions","Toronto Paper Matching System Agreement"])
    for note in submitted_paper_notes:
        paper_id = note.id
        paper_title = note.content["title"]
        paper_abstract = note.content["abstract"]
        author_names= ";".join(note.content["authors"])
        author_emails = ";".join(note.content["authorids"])
        subject_areas = note.content["TL;DR"]
        conflict_reasons = ";".join(note.content["conflicts"])
        files = note.content["pdf"]
        supplementary_files=""
        related_submission=""
        ac_suggestions=""
        toronto_paper_matching_system_agreement=""
        paper_details_list.append([paper_id,paper_title,paper_abstract,author_names,author_emails,
                                            subject_areas,conflict_reasons,files,supplementary_files,related_submission,
                                            ac_suggestions,toronto_paper_matching_system_agreement])
    return  paper_details_list


def get_paper_reviewer_score_tree(submitted_paper_notes,dict_reviewers_email):
    """
    Get an XML tree for paper reviewer score
    :param submitted_paper_notes:
    :param dict_reviewers_email:
    :return:
    """
    root=etree.Element("reviewermatching")
    meta_data_notes=get_paper_metadata_notes(get_paper_names(submitted_paper_notes))
    for index in range(len(submitted_paper_notes)):
        paper_id = submitted_paper_notes[index].id
        paper_element = etree.Element("submission",submissionId=str(paper_id))
        reviewers_score = {x["reviewer"]:x["score"] for x in meta_data_notes[index].content["reviewers"]}
        for reviewer,data in dict_reviewers_email.iteritems():
            score = 0
            if reviewer in reviewers_score:
                score=reviewers_score[reviewer]
            paper_element.append(etree.Element("metareviewer",email = data[3],score=str(score)))
        root.append(paper_element)
    return etree.ElementTree(root)


def get_all_member_ids():
    members = filter(lambda id: id != "~Super_User1" and id != "~",
                     map(lambda x: x.id, openreview.get_groups(regex="~.*")))
    return  members



def get_all_members_data():
    """
    Get a dictionary of each member with its details
    :param members:
    :return:
    """
    members = get_all_member_ids()
    dict_reviewer_data = {}
    for member in members:
        member_note = openreview.get_note(id=member)
        member_first_name= member_note.content["first"]
        member_last_name = member_note.content["last"]
        member_email=member_note.content["institutions"][0]["email"]
        member_organization = member_note.content["institutions"][0]["institution"]
        member_url = openreview.baseurl +"/notes?id=" + member
        dict_reviewer_data[member] = [member_first_name,member_last_name,member_organization,member_email,member,member_url]
    return dict_reviewer_data


if __name__ == '__main__':
    #Get all paper subitted to the conference
    submitted_paper_notes = get_notes_submitted_papers()
    #Get paper details and write in a file
    list_paper_details = get_submitted_paper_details(submitted_paper_notes)
    #Write paper_details to a file
    paper_details_file = open('1-fake-papers.csv', 'w+')
    for paper_details in list_paper_details:
        paper_details_file.write(",".join(paper_details) + "\n")
    paper_details_file.close()
    #Get all the reviewers data
    dict_reviewers_data = get_all_members_data()
    #Get paper score tree
    paper_score_tree = get_paper_reviewer_score_tree(submitted_paper_notes,dict_reviewers_data)
    #Write paper score data to an xml file
    paper_score_file = open("1-tpms_score.xml","w+")
    paper_score_file.write(etree.tostring(paper_score_tree,pretty_print=True))
    paper_score_file.close()
    #Write reviewers data to a file
    reviewer_data_file = open("2-reviewers.csv","w+")
    reviewer_data_file.write(",".join(["First Name","Last Name","Organization","Email","Reviewer","URL"])+ "\n")
    for reviewer, data in dict_reviewers_data.iteritems():
        reviewer_data=",".join(data) + "\n"
        reviewer_data_file.write(reviewer_data)
    reviewer_data_file.close()

