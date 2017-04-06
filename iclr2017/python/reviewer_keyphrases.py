'''
This script populates all keyphrases of the reviewers of ICLR 2016
'''
import os
import re
import openreview
import codecs
import sys

def initclient():
    your_username = 'OpenReview.net'  # fill in your email address that you use to log in to OpenReview
    your_password = 'OpenReview_beta'  # fill in your password
    your_baseurl = 'http://dev.openreview.net'  # fill in your desired baseurl (e.g. 'http://localhost:3000', or 'http://dev.openreview.net', etc.)

    openreview_client = openreview.Client(username=your_username, password=your_password, baseurl=your_baseurl)
    return openreview_client

def posttoopenreview(addedExpertise, client):
    errorIds = []
    noProfile = []
    succesfullyPosted = 0
    c = 0

    for emailId, expertise in addedExpertise.items():
        try:
            group = client.get_group(id=emailId)
            profileId = group.members[0]
            profile_note = client.get_note(profileId)
        except:
            noProfile.append([emailId, expertise])
            continue

        initlength = len(profile_note.content['expertise'])
        expertiseRows = addedExpertise[emailId]
        additionallength = len(expertiseRows)

        for expertiseRow in expertiseRows:
            profile_note.content['expertise'].append(expertiseRow)

        if profile_note.content['homepage'] is None:
            profile_note.content['homepage'] = ''
        if profile_note.content['linkedin'] is None:
            profile_note.content['linkedin'] = ''

        assert initlength + additionallength == len(profile_note.content['expertise'])
        try:
            client.post_note(profile_note)
            succesfullyPosted += 1
        except:
            errorIds.append([emailId, expertise, sys.exc_info()[0]])
            continue

    print "Number of notes successfully posted: ", succesfullyPosted
    print "Number of notes with no profiles: ", len(noProfile)
    print "Number of notes with errors in posting: ", len(errorIds)

    return noProfile, errorIds

def readkeyphrases(reviewersList):
    fp = codecs.open(reviewersList)
    noName = 0
    noKey = 0
    noKeyphrasesList = []
    noNameList = []
    totalNoReviewers = 0
    reviewerExpertise = {}
    for eachLine in fp.readlines():
        totalNoReviewers += 1
        emailId, firstName, lastName = eachLine.split(',')
        if firstName != '':
            #Handing Middlename Cases
            firstName = firstName.split()
            firstName = firstName[0]
        name = firstName + "_" + lastName.strip()
        fileName = firstName + "_" + lastName.strip() +".kp"
        if name == '_' or name == ' _ ':
            noName += 1
            noNameList.append(emailId)
            continue
#Include all keyphrase files in firstname_lastname.kp format in folder ./Reviewer_Keyphrases in working directory
        if os.path.isfile("./Reviewer_Keyphrases/"+fileName):
            reviewer_keyfiles = codecs.open("./Reviewer_Keyphrases/"+fileName)
            expertise = []

            for eachLine in reviewer_keyfiles.readlines():
                if eachLine == '' or eachLine == ' ' or eachLine == '\n':
                    continue
                expertiseElement = {}
                expertiseList = []
                expertiseElement[u'start'] = None
                expertiseElement[u'end'] = None

                keyphrases = re.split('<(.*?)>', eachLine)[1:-1]
                for keyphrase in keyphrases:
                    if keyphrase != '' and keyphrase != ' ' and keyphrase != '\n':
                        expertiseList.append(keyphrase)

                expertiseElement[u'keywords'] = expertiseList

                expertise.append(expertiseElement)

            reviewerExpertise[emailId] = expertise
        else:
            noKey += 1
            noKeyphrasesList.append(name)
    print "Stats: "
    print "Total number of reviewers: ", totalNoReviewers, "Number of reviewers with no name: ", noName, "Number of reviewers with no phrase file: ",noKey
    file1 = open('no_name.txt', 'w')
    for email in noNameList:
        file1.write(email+'\n')
    file1.close()
    file2 = open('no_keys.txt', 'w')
    for name in noKeyphrasesList:
        file2.write(name+'\n')
    file2.close()
    return reviewerExpertise

if __name__== '__main__':
    client = initclient()
#Include iclr_accepted_reviewers.csv in home folder
    reviewerExpertiseDict = readkeyphrases("./iclr_accepted_reviewers.csv")
    print "Number of reviewers with expertises added: ", len(reviewerExpertiseDict)
    noProfile, errorIds = posttoopenreview(reviewerExpertiseDict, client)
    file3 = open('no_profiles.txt', 'w')
    for profile in noProfile:
        file3.write(profile+'\n')
    file3.close()
    file4 = open('error_ids.txt', 'w')

    for error in errorIds:
        file4.write(error+'\n')
    file4.close()
