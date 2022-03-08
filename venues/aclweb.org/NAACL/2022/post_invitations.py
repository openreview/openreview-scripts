import argparse
from re import sub
from sys import set_asyncgen_hooks
import openreview
from tqdm import tqdm
import csv
import tracks
import countries

"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password

"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

sac_name_dictionary = tracks.sac_name_dictionary
track_names = list(sac_name_dictionary.keys())
countries = countries.countries
# Post commitment invitation 
preprocess = None
with open('./commitmentPreProcess.py') as f:
    preprocess = f.read()

commitment = openreview.Invitation(
    id = 'aclweb.org/NAACL/2022/Conference/-/Commitment_Submission',
    signatures = [
        "aclweb.org/NAACL/2022/Conference"
        ],
    readers = [
        "everyone"
        ],
    invitees=[
        "~",
        "OpenReview.net/Support"
        ],
    process= './commitmentProcess.js',
    preprocess=preprocess,
    reply={
        "readers":{
            "values-copied":[
                "aclweb.org/NAACL/2022/Conference",
                "{content.authorids}",
                "{signatures}"
            ]
        },
        "writers": {
            "values-copied": [
                "aclweb.org/NAACL/2022/Conference",
                "{content.authorids}",
                "{signatures}"
            ]
        },
        "signatures": { "values-regex": "~.*" },
        "content":{
            "title": {
                "description": "Enter the title of the ARR submission that you want to commit to NAACL 2022",
                "value-regex": ".{1,250}",
                "required": True,
                "order": 10
            },
            "authors": {
                "description": "The author information entered in this field is only for communication purposes. Please remember that the list of authors and their order cannot be changed and should be the same as what was submitted to ARR. Comma separated list of author names.",
                "order": 11,
                "values-regex": "[^;,\\n]+(,[^,\\n]+)*",
                "required": True,
                "hidden": True
            },
            "authorids": {
                "description": "The author information entered in this field is only for communication purposes. Please remember that the list of authors and their order cannot be changed and should be the same as what was submitted to ARR. Search author profile by first, middle and last name or email address. If the profile is not found, you can add the author by completing first, middle, and last names as well as author email address.",
                "order": 12,
                "values-regex": "~.*|([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,},){0,}([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,})",
                "required": True
            },
            "paper_link": {
                "description": "The link to the paper on ARR (including id). You need to put a link to the page that shows the reviews and the meta-review (it should end with forum= a random string of letters, like https://openreview.net/forum?id=abCD-EFgHI). Please, do NOT put a link to the PDF or to the list of your papers.",
                "value-regex": "https://openreview.net/forum\\?id=.*",
                "required": True,
                "markdown": False,
                "order": 13
            },
            "paper_type": {
                "description": "Indicate whether this is a short (a small, focused contribution; a negative result; an opinion piece; or an interesting application nugget) or a long paper.",
                "value-radio": [
                    "Long paper (up to eight pages of content + unlimited references and appendices)",
                    "Short paper (up to four pages of content + unlimited references and appendices)"
                    ],
                "required": True,
                "order": 14
            },
            "track": {
                "description": "Please enter the subject area under which the submission should be considered. ",
                "value-radio": track_names,
                "required": True,
                "order": 15
            },
            "naacl_preprint": {
                "description": "Would the authors like to have a public anonymous pre-print of the submission? This includes PDF, abstract and all supplemental material.",
                "value-radio": [
                    "yes",
                    "no"
                    ],
                "required": True,
                "order": 17
            },
            "existing_preprints": {
                "values-regex": ".{1,500}",
                "description": "If there are any publicly available non-anonymous preprints of this paper, please list them here (provide the URLs please).",
                "required": False,
                "order": 18
            },
            "authorship": {
                "values-checkbox": [
                    "I confirm that I am one of the authors of this paper"
                    ],
                "required": True,
                "order": 19
            },
            "author_profiles": {
                "description": "Please confirm that the OpenReview profiles of all authors are up-to-date (with current email address, institution name, institution domain) by selecting 'Yes'.",
                "value-checkbox": "Yes",
                "required": True,
                "order": 22
            },
            "paper_version": {
                "values-checkbox": [
                    "I confirm that this link is for the latest version of the paper in ARR that has reviews and a meta-review"
                    ],
                "required": True,
                "order": 20
            },
            "anonymity_period": {
                "values-checkbox": [
                    "I confirm that this submission complies with the anonymity period"
                    ],
                "required": True,
                "order": 21
            },
            "anonymity_period": {
                "values-checkbox": [
                    "I confirm that this submission complies with the anonymity period"
                    ],
                "required": True,
                "order": 21
            },
            "comment": {
                "description": "In rare cases where there are important factual errors in a review or meta-review, please use this field to point the Senior Area Chair(s) to the discrepancy between the review and the content of the paper (use line numbers to identify relevant passages in your submission). Note that SACs cannot communicate with ARR reviewers and action editors for discussion after the paper is committed to NAACL. To directly respond to reviewer comments, please resubmit to the ACL Rolling Review instead. (200 words)",
                "order": 13,
                "value-regex": "[\\S\\s]{0,800}",
                "required": False
                },
            "country_of_affiliation_of_corresponding_author": {
                "order" : 16,
                "description" : "Help us understand the geographic diversity of authors by indicating the country where you (the corresponding author) work",
                "values-dropdown": countries,
                "required": True
                },
            "reproducibility_track_survey":{
                "values-checkbox": [
                ],
                "description": "Authors of accepted papers will have the opportunity to apply for badges recognizing practices that facilitate reproducibility. Please take a moment to fill out this short survey to help us plan resources for this track: https://forms.office.com/r/sq8dNp91qA",
                "required": False,
                "order": 19
            }
        }
    }
)


# Posting submission invitation 
submission_invitation = client.post_invitation(openreview.Invitation(
    id = "aclweb.org/NAACL/2022/Conference/-/Submission",
    signatures = ["aclweb.org/NAACL/2022/Conference"],
    readers = ["everyone"],
    invitees=["aclweb.org/NAACL/2022/Conference"],
    reply={
        "readers":{
            "values":[
                "aclweb.org/NAACL/2022/Conference"
            ]
            },
        "writers":{
            "values":[
                "aclweb.org/NAACL/2022/Conference"
                ]
            },
        "signatures":{
            "values":[
                "aclweb.org/NAACL/2022/Conference"
                ]
            },
        "content":{
            "title": {
                "description": "Title of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 1,
                "value-regex": ".{1,250}",
                "required": True
            },
            "authors": {
                "description": "Comma separated list of author names.",
                "order": 2,
                "values-regex": "[^;,\\n]+(,[^,\\n]+)*",
                "required": True,
                "hidden": True
            },
            "authorids": {
                "description": "Search author profile by first, middle and last name or email address. If the profile is not found, you can add the author by completing first, middle, and last names as well as author email address.",
                "order": 3,
                "values-regex": "~.*|([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,},){0,}([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,})",
                "required": True
            },
            "abstract": {
                "description": "Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 4,
                "value-regex": "[\\S\\s]{1,5000}",
                "required": True
            },
            "pdf": {
                "description": "Upload a single PDF containing the paper, references and any appendices",
                "order": 15,
                "value-file": {
                "fileTypes": [
                    "pdf"
                ],
                "size": 80
                },
                "required": True
            },
            "software": {
                "description": "Each ARR submission can be accompanied by one .tgz or .zip archive containing software (max. 200MB).",
                "order": 21,
                "value-file": {
                    "fileTypes": [
                        "tgz",
                        "zip"
                    ],
                    "size": 200
                },
                "required": False
                },
            "data": {
                "description": "Each ARR submission can be accompanied by one .tgz or .zip archive containing data (max. 200MB).",
                "order": 22,
                "value-file": {
                    "fileTypes": [
                        "tgz",
                        "zip"
                    ],
                    "size": 200
                },
                "required": False
                },
            "paper_link": {
                "description": "Provide the link to your previous ACL submission",
                "value-regex": "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                "required": True,
                "order": 10
                },
            "paper_type": {
                "description": "Select if your paper is short or long",
                "value-radio": [
                    "Short paper (up to four pages of content + unlimited references and appendices)",
                    "Long paper (up to eight pages of content + unlimited references and appendices)"
                ],
                "required": True,
                "order": 11
                },
            "track": {
                "description": "Select the track that best fits your submission.",
                "value-radio": track_names,
                "required": True,
                "order": 12
                },
            "comment": {
                "description": "In rare cases where there are important factual errors in a review or meta-review, please use this field to point the Senior Area Chair(s) to the discrepancy between the review and the content of the paper (use line numbers to identify relevant passages in your submission). Note that SACs cannot communicate with ARR reviewers and action editors for discussion after the paper is committed to NAACL. To directly respond to reviewer comments, please resubmit to the ACL Rolling Review instead. (200 words)",
                "order": 13,
                "value-regex": "[\\S\\s]{0,800}",
                "required": False
                },
            "authorship": {
                "values-checkbox": [
                    "I confirm that I am one of the authors of this paper."
                ],
                "required": True,
                "order": 19
            },
            "paper_version": {
                "values-checkbox": [
                    "I confirm that this link is for the latest version of the paper in ARR that has reviews and a meta-review."
                ],
                "required": True,
                "order": 20
            },
            "anonymity_period": {
                "values-checkbox": [
                "I confirm that this submission complies with the anonymity period."
                ],
                "required": True,
                "order": 21
            },
            "commitment_note":{
                "value-regex":".*",
                "required": True,
                "order": 30
            },
            "naacl_preprint": {
            "description": "Would the authors like to have a public anonymous pre-print of the submission? This includes PDF, abstract and all supplemental material.",
            "value-radio": [
                "yes",
                "no"
            ],
            "required": False,
            "order": 16
            },
            "preprint": {
            "description": "Would the authors like to have a public anonymous pre-print of the submission? This includes PDF, abstract and all supplemental material.",
            "value-radio": [
                "yes",
                "no"
            ],
            "required": False,
            "order":31
            },
            "existing_preprints": {
            "value-regex": ".*",
            "description": "If there are any publicly available non-anonymous preprints of this paper, please list them here (provide the URLs please).",
            "required": False,
            "order": 17
            },
            "previous_URL": {
            "description": "Provide the URL of your previous submission to ACL Rolling Review if this is a resubmission",
            "order": 16,
            "value-regex": ".{0,500}",
            "required": False
            },
            "TL;DR": {
            "description": "\"Too Long; Didn't Read\": a short sentence describing your paper",
            "order": 13,
            "value-regex": "[^\\n]{0,250}",
            "required": False
        },
                "author_profiles": {
            "values-checkbox": [
                "I confirm that the OpenReview profiles of all authors are up-to-date (with current email address, institution name, institution domain)."
            ],
            "required": True,
            "order": 14
            },
        "country_of_affiliation_of_corresponding_author": {
                "order" : 16,
                "description" : "Help us understand the geographic diversity of authors by indicating the country where you (the corresponding author) work",
                "values-dropdown": countries,
                "required": True
                }
        }
    }  
))

# Posting Blind Submission Invitation 
blind = client.post_invitation(openreview.Invitation(
    id = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission',
    readers = [
        'everyone'
        ],
    writers = [
        'aclweb.org/NAACL/2022/Conference'
        ],
    invitees = [
        'aclweb.org/NAACL/2022/Conference'
        ],
    signatures = [
        'aclweb.org/NAACL/2022/Conference'
        ],
    reply ={
        "readers" : {
            "values-regex":".*"
            },
        "nonreaders" : {
            "values-regex":".*"
            },
        "writers" : {
            "values-regex":".*"
            },
        "signatures" : {
            "values":[
                'aclweb.org/NAACL/2022/Conference'
                ]
            },
        "content" : {
            "authorids" : { 
                "values-regex": ".*" 
                },
            "authors": {
                "values-regex": ".*" 
                }
            }   
        }
    ))
official_review = openreview.Invitation(
    id = 'aclweb.org/NAACL/2022/Conference/-/ARR_Official_Review',
    signatures= [
        'aclweb.org/NAACL/2022/Conference'
    ],
    readers = [
        'everyone'
    ],
    writers = [
        'aclweb.org/NAACL/2022/Conference'
    ],
    reply = {
        "readers" : {
            "values-regex":".*"
            },
        "nonreaders" : {
            "values-regex":".*"
            },
        "writers": {"values": [
                'aclweb.org/NAACL/2022/Conference'
        ]},
        "signatures": 
            {
                "values-regex": ".*"
                
        },
        "content":{
            "title": {
                "order": 1,
                "value-regex": ".{0,500}",
                "description": "Brief summary of your review.",
                "required": False
            },
            "reviewer_id":{
                "order": 2,
                "value-regex": ".*",
                "required": True
            },
            "review": {
                "order": 3,
                "value-regex": "[\\S\\s]{1,200000}",
                "description": "Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons (max 200000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
                "required": False,
                "markdown": True
            },
            "rating": {
                "order": 4,
                "value-regex": ".*",
                "required": False
            },
            "confidence": {
                "value-regex": '.*',
                "required": False
            },
            "paper_summary": {
                "order": 5,
                "description": "Describe what this paper is about. This should help action editors and area chairs to understand the topic of the work and highlight any possible misunderstandings. Maximum length 1000 characters.",
                "value-regex": "[\\S\\s]{0,10000}",
                "required": False,
                "markdown": True
                },
                "summary_of_strengths": {
                    "order": 6,
                    "value-regex": "[\\S\\s]{0,10000}",
                    "description": "What are the major reasons to publish this paper at a selective *ACL venue? These could include novel and useful methodology, insightful empirical results or theoretical analysis, clear organization of related literature, or any other reason why interested readers of *ACL papers may find the paper useful. Maximum length 5000 characters.",
                    "required": False,
                    "markdown": True
                },
                "summary_of_weaknesses": {
                    "order": 7,
                    "value-regex": "[\\S\\s]{0,10000}",
                    "description": "What are the concerns that you have about the paper that would cause you to favor prioritizing other high-quality papers that are also under consideration for publication? These could include concerns about correctness of the results or argumentation, limited perceived impact of the methods or findings (note that impact can be significant both in broad or in narrow sub-fields), lack of clarity in exposition, or any other reason why interested readers of *ACL papers may gain less from this paper than they would from other papers under consideration. Where possible, please number your concerns so authors may respond to them individually. Maximum length 5000 characters.",
                    "required": False,
                    "markdown": True
                },
                "comments,_suggestions_and_typos": {
                    "order": 8,
                    "value-regex": "[\\S\\s]{0,20000}",
                    "description": "If you have any comments to the authors about how they may improve their paper, other than addressing the concerns above, please list them here.\n Maximum length 5000 characters.",
                    "required": False,
                    "markdown": True
                },
                "overall_assessment": {
                    "order": 9,
                    "value-regex": '.*',
                    "required": False
                },
                "best_paper": {
                    "order": 10,
                    "description": "Could this be a best paper in a top-tier *ACL venue?",
                    "value-radio": [
                        "Yes",
                        "Maybe",
                        "No"
                    ],
                    "required": False
                },
                "best_paper_justification": {
                    "order": 11,
                    "description": "If the answer on best paper potential is Yes or Maybe, please justify your decision.",
                    "value-regex": "[\\S\\s]{0,10000}",
                    "required": False,
                    "markdown": True
                    },
                "replicability": {
                    "order": 12,
                    "description": "Will members of the ACL community be able to reproduce or verify the results in this paper?",
                    "value-regex": '.*',
                    "required": False
                },
                "datasets": {
                    "order": 13,
                    "description": "If the authors state (in anonymous fashion) that datasets will be released, how valuable will they be to others?",
                    "value-regex": '.*',
                    "required": False
                    },
                "software": {
                    "order": 14,
                    "description": "If the authors state (in anonymous fashion) that their software will be available, how valuable will it be to others?",
                    "value-regex": '.*',
                    "required": False
                },
                "author_identity_guess": {
                    "order": 15,
                    "description": "Do you know the author identity or have an educated guess?",
                    "value-regex": '.*',
                    "required": False
                },
                "ethical_concerns": {
                    "order": 16,
                    "value-regex": "[\\S\\s]{0,10000}",
                    "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
                    "required": False,
                    "markdown": True
                    },
                "ethical_concernes": {
                    "order": 17,
                    "value-regex": "[\\S\\s]{0,10000}",
                    "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
                    "required": False,
                    "markdown": True
                    },
                "link_to_original_review":{
                    "value-regex": ".{0,10000}",
                    "description": "Link to the review on the original ARR submission",
                    "required": True,
                    "markdown": True
                    },
                "limitations_and_societal_impact": {
                    "order": 9,
                    "value-regex": "[\\S\\s]{0,10000}",
                    "description": "Have the authors adequately discussed the limitations and potential positive and negative societal impacts of their work? If not, please include constructive suggestions for improvement. Authors should be rewarded rather than punished for being up front about the limitations of their work and any potential negative societal impact. You are encouraged to think through whether any critical points are missing and provide these as feedback for the authors. Consider, for example, cases of exclusion of user groups, overgeneralization of findings, unfair impacts on traditionally marginalized populations, bias confirmation, under- and overexposure of languages or approaches, and dual use (see Hovy and Spruit, 2016, for examples of those). Consider who benefits from the technology if it is functioning as intended, as well as who might be harmed, and how. Consider the failure modes, and in case of failure, who might be harmed and how.",
                    "required": False,
                    "markdown": True
                    },
                "needs_ethics_review": {
                    "order": 11,
                    "value-radio": [
                        "Yes",
                        "No"
                    ],
                    "description": "Should this paper be sent for an in-depth ethics review? We have a small ethics committee that can specially review very challenging papers when it comes to ethical issues. If this seems to be such a paper, then please explain why here, and we will try to ensure that it receives a separate review.",
                    "required": False,
                    "markdown": True
                    },
                "reproducibility": {
                    "order": 12,
                    "description": "Is there enough information in this paper for a reader to reproduce the main results, use results presented in this paper in future work (e.g., as a baseline), or build upon this work?",
                    "value-regex": '.*',
                    "required": False
                    },
                }
            }
        )
client.post_invitation(official_review)

metareview = openreview.Invitation(
   id = 'aclweb.org/NAACL/2022/Conference/-/ARR_Meta_Review',
    signatures = [
        'aclweb.org/NAACL/2022/Conference'
    ],
    readers = [
        'everyone'
    ],
    writers = [
        'aclweb.org/NAACL/2022/Conference'
    ],
    reply = {
        "readers" : {
            "values-regex":".*"
            },
        "nonreaders" : {
            "values-regex":".*"
            },
        "writers": {
            "values": [
                'aclweb.org/NAACL/2022/Conference'
        ]},
        "signatures": {
             "values-regex": '.*'
        },
        "content":{
            "title": {
                "description": "Title of your meta review",
                "order": 1,
                "value-regex": ".{1,250}",
                "required": False
            },
            "action_editor_id":{
                "order": 2,
                "value-regex": ".*",
                "required": True
            },
            "metareview": {
                "order": 3,
                "value-regex": "[\\S\\s]{1,10000}",
                "description": "Describe what this paper is about. This should help SACs at publication venues understand what sessions the paper might fit in. Maximum 5000 characters. Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
                "required": False,
                "markdown": True
                },
            "summary_of_reasons_to_publish": {
                "order": 4,
                "value-regex": "[\\S\\s]{1,10000}",
                "description": "What are the major reasons to publish this paper at a *ACL venue? This should help SACs at publication venues understand why they might want to accept the paper. Maximum 5000 characters.",
                "required": False,
                "markdown": True
                },
            "summary_of_suggested_revisions": {
                "order": 5,
                "value-regex": "[\\S\\s]{1,10000}",
                "description": "What revisions could the authors make to the research and the paper that would improve it? This should help authors understand the reviews in context, and help them plan any future resubmission. Maximum 5000 characters.",
                "required": False,
                "markdown": True
                },
            "overall_assessment": {
                "order": 6,
                "value-regex": "[\\S\\s]{1,10000}",
                "required": False
                },
            "suggested_venues": {
                "order": 7,
                "description": "You are encouraged to suggest conferences or workshops that would be suitable for this paper.",
                "value-regex": "[\\S\\s]{1,10000}",
                "markdown": True,
                "required": False
                },
            "ethical_concernes": {
                "order": 8,
                "value-regex": "[\\S\\s]{0,10000}",
                "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
                "required": False,
                "markdown": True
                },
                "ethical_concerns": {
                "order": 8,
                "value-regex": "[\\S\\s]{0,10000}",
                "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
                "required": False,
                "markdown": True
                },
            "link_to_original_metareview":{
                "value-regex": ".{0,10000}",
                "description": "Link to the metareview on the original ARR submission",
                "required": True,
                "markdown": True
                }
            }
        } 
    )
client.post_invitation(metareview)
