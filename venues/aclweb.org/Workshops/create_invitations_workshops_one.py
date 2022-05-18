import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv

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
parser.add_argument('--confid')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
confid = args.confid

 
commitment_invitation = client.get_invitation(f"{confid}/-/Submission")
submission_invitation_content = {"title": {
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
        "responsible_NLP_research": {
      "description": "Upload a single PDF of your completed responsible NLP research checklist (see https://aclrollingreview.org/responsibleNLPresearch/).",
      "order": 16,
      "value-file": {
        "fileTypes": [
          "pdf"
        ],
        "size": 80
      },
      "required": False
    },
    "commitment_note":{
                "value-regex":".*",
                "required": True,
                "order": 30
            },
    "paper_link": {
                "description": "Provide the link to your previous ACL submission",
                "value-regex": "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                "required": True,
                "order": 10
                } ,
                "paper_type": {
      "description": "Short or long. See the CFP for the requirements for short and long papers.",
      "value-radio": [
        "long",
        "short"
      ],
      "order": 17,
      "required": False
    },
    }
for key in commitment_invitation.reply['content'].keys(): 
    if key != 'existing_preprints':
        submission_invitation_content[key] = commitment_invitation.reply['content'][key]
# Posting submission invitation 
submission_invitation = openreview.Invitation(
    id = f"{confid}/-/Migrated_Submission",
    signatures = [confid],
    readers = ["everyone"],
    invitees=[confid],
    reply={
        "readers":{
            "values":[
                confid
            ]
            },
        "writers":{
            "values":[
                confid
                ]
            },
        "signatures":{
            "values":[
                confid
                ]
            },
        "content":submission_invitation_content
    }  
)

client.post_invitation(submission_invitation)

# Posting Blind Submission Invitation 
blind = openreview.Invitation(
    id = f'{confid}/-/Migrated_Blind_Submission',
    readers = [
        'everyone'
        ],
    writers = [
        confid
        ],
    invitees = [
        confid
        ],
    signatures = [
        confid
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
                confid
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
    )

client.post_invitation(blind)


official_review = openreview.Invitation(
    id = f'{confid}/-/ARR_Official_Review',
    signatures= [
        confid
    ],
    readers = [
        'everyone'
    ],
    writers = [
        confid
    ],
    reply = {
        "readers" : {
            "values-regex":".*"
            },
        "nonreaders" : {
            "values-regex":".*"
            },
        "writers": {"values": [
                confid
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
                "required": False
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
                "value-radio": [
                    "5 = Positive that my evaluation is correct. I read the paper very carefully and am familiar with related work.",
                    "4 = Quite sure. I tried to check the important points carefully. It's unlikely, though conceivable, that I missed something that should affect my ratings.",
                    "3 =  Pretty sure, but there's a chance I missed something. Although I have a good feel for this area in general, I did not carefully check the paper's details, e.g., the math or experimental design.",
                    "2 =  Willing to defend my evaluation, but it is fairly likely that I missed some details, didn't understand some central points, or can't be sure about the novelty of the work.",
                    "1 = Not my area, or paper is very hard to understand. My evaluation is just an educated guess."
                ],
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
                "comments_suggestions_and_typos": {
                    "order": 8,
                    "value-regex": "[\\S\\s]{0,10000}",
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
                    "required": True
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
                    "value-radio": [
                        "5 = They could easily reproduce the results.",
                        "4 = They could mostly reproduce the results, but there may be some variation because of sample variance or minor variations in their interpretation of the protocol or method.",
                        "3 = They could reproduce the results with some difficulty. The settings of parameters are underspecified or subjectively determined, and/or the training/evaluation data are not widely available.",
                        "2 = They would be hard pressed to reproduce the results: The contribution depends on data that are simply not available outside the author's institution or consortium and/or not enough details are provided.",
                        "1 = They would not be able to reproduce the results here no matter how hard they tried."
                    ],
                    "required": False
                },
                "datasets": {
                    "order": 13,
                    "description": "If the authors state (in anonymous fashion) that datasets will be released, how valuable will they be to others?",
                    "value-radio": [
                        "5 = Enabling: The newly released datasets should affect other people's choice of research or development projects to undertake.",
                        "4 = Useful: I would recommend the new datasets to other researchers or developers for their ongoing work.",
                        "3 = Potentially useful: Someone might find the new datasets useful for their work.",
                        "2 = Documentary: The new datasets will be useful to study or replicate the reported research, although for other purposes they may have limited interest or limited usability. (Still a positive rating)",
                        "1 = No usable datasets submitted."
                    ],
                    "required": False
                    },
                "software": {
                    "order": 14,
                    "description": "If the authors state (in anonymous fashion) that their software will be available, how valuable will it be to others?",
                    "value-radio": [
                        "5 = Enabling: The newly released software should affect other people's choice of research or development projects to undertake.",
                        "4 = Useful: I would recommend the new software to other researchers or developers for their ongoing work.",
                        "3 = Potentially useful: Someone might find the new software useful for their work.",
                        "2 = Documentary: The new software will be useful to study or replicate the reported research, although for other purposes it may have limited interest or limited usability. (Still a positive rating)",
                        "1 = No usable software released."
                    ],
                    "required": False
                },
                "author_identity_guess": {
                    "order": 15,
                    "description": "Do you know the author identity or have an educated guess?",
                    "value-radio": [
                        "5 = From a violation of the anonymity-window or other double-blind-submission rules, I know/can guess at least one author's name.",
                        "4 = From an allowed pre-existing preprint or workshop paper, I know/can guess at least one author's name.",
                        "3 = From the contents of the submission itself, I know/can guess at least one author's name.",
                        "2 = From social media/a talk/other informal communication, I know/can guess at least one author's name.",
                        "1 = I do not have even an educated guess about author identity."
                    ],
                    "required": True
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
                    "required": False,
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
      "value-radio": [
        "5 = They could easily reproduce the results.",
        "4 = They could mostly reproduce the results, but there may be some variation because of sample variance or minor variations in their interpretation of the protocol or method.",
        "3 = They could reproduce the results with some difficulty. The settings of parameters are underspecified or subjectively determined, and/or the training/evaluation data are not widely available.",
        "2 = They would be hard pressed to reproduce the results: The contribution depends on data that are simply not available outside the author's institution or consortium and/or not enough details are provided.",
        "1 = They would not be able to reproduce the results here no matter how hard they tried."
      ],
      "required": False
    },
                }
            }
        )
client.post_invitation(official_review)

metareview = openreview.Invitation(
   id = f'{confid}/-/ARR_Meta_Review',
    signatures = [
        confid
    ],
    readers = [
        'everyone'
    ],
    writers = [
        confid
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
                confid
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
                "required": False
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
                "value-radio": [
                    "5 = The paper is largely complete and there are no clear points of revision",
                    "4 = There are minor points that may be revised",
                    "3 = There are major points that may be revised",
                    "2 = The paper would need significant revisions to reach a publishable state",
                    "1 = Even after revisions, the paper is not likely to be publishable at an *ACL venue"
                ],
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
            "link_to_original_metareview":{
                "value-regex": ".{0,10000}",
                "description": "Link to the metareview on the original ARR submission",
                "required": False,
                "markdown": True
                },
                "ethical_concerns": {
      "order": 6,
      "value-regex": "[\\S\\s]{0,2000}",
      "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
      "required": False,
      "markdown": True
    },
    "needs_ethics_review": {
      "order": 7,
      "value-radio": [
        "Yes"
      ],
      "description": "Should this paper be sent for an in-depth ethics review? We have a small ethics committee that can specially review very challenging papers when it comes to ethical issues. If this seems to be such a paper, then please explain why here, and we will try to ensure that it receives a separate review.",
      "required": False,
      "markdown": True
    },
    "great_reviews": {
      "order": 8,
      "value-regex": "[\\S\\s]{0,2000}",
      "description": "Please list the ids of all reviewers who went beyond expectations in terms of providing informative and constructive reviews and discussion. For example: jAxb, zZac",
      "required": False,
      "markdown": True
    },
    "poor_reviews": {
      "order": 9,
      "value-regex": "[\\S\\s]{0,2000}",
      "description": "Please list the ids of all reviewers whose reviews did not meet expectations. For example: jAxb, zZac",
      "required": False,
      "markdown": True
    }
            }
        } 
    )
client.post_invitation(metareview)