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
client = openreview.api.OpenReviewClient(baseurl=args.baseurl, username=args.username, password=args.password)
confid = args.confid

 
commitment_invitation = client.get_invitation(f"{confid}/-/Submission")
submission_invitation_content = {
            "title": {
                "order": 1,
                "description": "Title of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$.",
                "value": {
                    "param": {
                        "type": "string",
                        "regex": "^.{1,250}$"
                    }
                }
            },
            "authors": {
                "order": 2,
                "value": {
                    "param": {
                        "type": "string[]",
                        "regex": "[^;,\\n]+(,[^,\\n]+)*",
                        "hidden": True
                    }
                },
                "readers": {
                    "param": {
                        "regex": ".*",
                        "optional": True
                    }
                }
            },
            "authorids": {
                "order": 3,
                "description": "Search author profile by first, middle and last name or email address",
                "value": {
                    "param": {
                        "type": "group[]",
                        "regex": ".*"
                    }
                },
                "readers": {
                    "param": {
                        "regex": ".*",
                        "optional": True
                    }
                }
            },
            "keywords": {
                "description": "Comma separated list of keywords.",
                "order": 4,
                "value": {
                "param": {
                    "type": "string[]",
                    "regex": "(^$)|[^;,\\n]+(,[^,\\n]+)*",
                    "optional": True
                }
                }
            },
            "TLDR": {
                "order": 5,
                "description": "\"Too Long; Didn't Read\": a short sentence describing your paper",
                "value": {
                    "param": {
                        "fieldName": "TL;DR",
                        "type": "string",
                        "minLength": 1,
                        "optional": True
                    }
                }
            },
            "abstract": {
                "order": 6,
                "description": "Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$.",
                "value": {
                    "param": {
                        "type": "string",
                        "minLength": 1,
                        "markdown": True,
                        "input": "textarea"
                    }
                }
            },
            "pdf": {
                "order": 7,
                "description": "Upload a PDF file that ends with .pdf.",
                "value": {
                    "param": {
                        "type": "file",
                        "maxSize": 50,
                        "extensions": [
                            "pdf"
                        ]
                    }
                }
            },
            "software": {
                "order": 21,
                "description": "Each ARR submission can be accompanied by one .tgz or .zip archive containing software (max. 200MB).",
                "value": {
                    "param": {
                        "type": "file",
                        "maxSize": 50,
                        "extensions": [
                            "tgz",
                            "zip"
                        ],
                        "optional": True
                    }
                }
            },
            "data": {
                "order": 22,
                "description": "Each ARR submission can be accompanied by one .tgz or .zip archive containing data (max. 200MB).",
                "value": {
                    "param": {
                        "type": "file",
                        "maxSize": 50,
                        "extensions": [
                            "tgz",
                            "zip"
                        ],
                        "optional": True
                    }
                }
            },
            "preprint": {
                "description": "Would the authors like to have a public anonymous pre-print of the submission? This includes PDF, abstract and all supplemental material.",
                "value": {
                    "param": {
                        "type": "string",
                        "enum": [
                            "yes",
                            "no"
                        ],
                        "input": "radio",
                        "optional": True
                    }
                },
                "order": 12
            },
            "existing_preprints": {
                "order": 17,
                "description": "If there are any publicly available non-anonymous preprints of this paper, please list them here (provide the URLs please).",
                "value": {
                    "param": {
                        "type": "string",
                        "minLength": 1,
                        "optional": True
                    }
                }
            },
            "previous_URL": {
                "order": 17,
                "description": "Provide the URL of your previous submission to ACL Rolling Review if this is a resubmission",
                "value": {
                    "param": {
                        "type": "string",
                        "minLength": 1,
                        "optional": True
                    }
                }
            },
            "responsible_NLP_research": {
                "order": 21,
                "description": "Upload a single PDF of your completed responsible NLP research checklist (see https://aclrollingreview.org/responsibleNLPresearch/).",
                "value": {
                    "param": {
                        "type": "file",
                        "maxSize": 50,
                        "extensions": [
                            "pdf"
                        ],
                        "optional": True
                    }
                }
            },
            "commitment_note": {
                "order": 30,
                "value": {
                    "param": {
                        "type": "string",
                        "minLength": 1,
                    }
                }
            },
            "paper_link": {
                "order": 10,
                "value": {
                    "param": {
                        "type": "string",
                        "regex": "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
                    }
                }
            },
            "paper_type": {
                "description": "Short or long. See the CFP for the requirements for short and long papers.",
                "value": {
                    "param": {
                        "type": "string",
                        "enum": [
                            "long",
                            "short"
                        ],
                        "input": "radio",
                        "optional": True
                    }
                },
                "order": 17
            },
            "paperhash": {
                "order": 17,
                "value": {
                    "param": {
                        "type": "string",
                        "optional": True
                    }
                },
                "readers": {
                    "param": {
                        "regex": ".*",
                        "optional": True
                    }
                }
            },
            "_bibtex": {
                "order": 17,
                "value": {
                    "param": {
                        "type": "string",
                        "optional": True
                    }
                }
            },
    }

# Also overwrite authorids to allow emails
# Older ARR submissions have optional keywords
for key in commitment_invitation.edit['note']['content'].keys(): 
    if key not in ['existing_preprints', 'authors', 'authorids', 'keywords']:
        submission_invitation_content[key] = commitment_invitation.edit['note']['content'][key]

submission_invitation = openreview.api.Invitation(
        id=f"{confid}/-/Migrated_Submission",
        invitees = ['~'],
        signatures = [confid],
        readers = ['everyone'],
        writers = [confid],
        edit = {
            'signatures': [confid],
            'readers': { 'param': { 'regex': '.*' } },
            'nonreaders': { 'param': { 'regex': '.*' } },
            'writers': [confid],
            'ddate': {
                'param': {
                    'range': [ 0, 9999999999999 ],
                    'optional': True,
                    'deletable': True
                }
            },                
            'note': {
                'id': {
                    'param': {
                        'withInvitation': f"{confid}/-/Migrated_Submission",
                        'optional': True
                    }
                },
                'ddate': {
                    'param': {
                        'range': [ 0, 9999999999999 ],
                        'optional': True,
                        'deletable': True
                    }
                },
                'signatures': [confid],
                'readers': { 'param': { 'regex': '.*' } },
                'nonreaders': { 'param': { 'regex': '.*' } },
                'writers': [confid],
                'content': submission_invitation_content
            }
        }
    )

client.post_invitation_edit(invitations=f"{confid}/-/Edit",
    readers=[confid],
    writers=[confid],
    signatures=[confid],
    invitation=submission_invitation
)

official_review_content = {
    "title": {
        "order": 1,
        "description": "Brief summary of your review.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "optional": True
            }
        }
    },
    "reviewer_id": {
        "order": 2,
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "optional": True
            }
        }
    },
    "review": {
        "order": 3,
        "description": "Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons (max 200000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "rating": {
        "order": 4,
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "optional": True
            }
        }
    },
    "confidence": {
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = Positive that my evaluation is correct. I read the paper very carefully and am familiar with related work.",
                    "4 = Quite sure. I tried to check the important points carefully. It's unlikely, though conceivable, that I missed something that should affect my ratings.",
                    "3 =  Pretty sure, but there's a chance I missed something. Although I have a good feel for this area in general, I did not carefully check the paper's details, e.g., the math or experimental design.",
                    "2 =  Willing to defend my evaluation, but it is fairly likely that I missed some details, didn't understand some central points, or can't be sure about the novelty of the work.",
                    "1 = Not my area, or paper is very hard to understand. My evaluation is just an educated guess."
                ],
                "input": "radio",
                "optional": True
            }
        }
    },
    "paper_summary": {
        "order": 3,
        "description": "Describe what this paper is about. This should help action editors and area chairs to understand the topic of the work and highlight any possible misunderstandings. Maximum length 1000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "summary_of_strength": {
        "order": 4,
        "description": "What are the major reasons to publish this paper at a selective *ACL venue? These could include novel and useful methodology, insightful empirical results or theoretical analysis, clear organization of related literature, or any other reason why interested readers of *ACL papers may find the paper useful. Maximum length 5000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "summary_of_strengths": {
        "order": 5,
        "description": "What are the major reasons to publish this paper at a selective *ACL venue? These could include novel and useful methodology, insightful empirical results or theoretical analysis, clear organization of related literature, or any other reason why interested readers of *ACL papers may find the paper useful. Maximum length 5000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "summary_of_weaknesses": {
        "order": 6,
        "description": "What are the concerns that you have about the paper that would cause you to favor prioritizing other high-quality papers that are also under consideration for publication? These could include concerns about correctness of the results or argumentation, limited perceived impact of the methods or findings (note that impact can be significant both in broad or in narrow sub-fields), lack of clarity in exposition, or any other reason why interested readers of *ACL papers may gain less from this paper than they would from other papers under consideration. Where possible, please number your concerns so authors may respond to them individually. Maximum length 5000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "comments_suggestions_and_typos": {
        "order": 7,
        "description": "If you have any comments to the authors about how they may improve their paper, other than addressing the concerns above, please list them here.\n Maximum length 5000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "soundness": {
        "order": 8,
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = Excellent: This study is one of the most thorough I have seen, given its type.",
                    "4.5 ",
                    "4 = Strong: This study provides sufficient support for all of its claims/arguments. Some extra experiments could be nice, but not essential.",
                    "3.5 ",
                    "3 = Acceptable: This study provides sufficient support for its major claims/arguments. Some minor points may need extra support or details.",
                    "2.5 ",
                    "2 = Poor: Some of the main claims/arguments are not sufficiently supported. There are major technical/methodological problems.",
                    "1.5 ",
                    "1 = Major Issues: This study is not yet sufficiently thorough to warrant publication or is not relevant to ACL."
                    ],
                    "input": "radio",
                    "optional": True
                }
            },
        "description": "How sound and thorough is this study? Does the paper clearly state scientific claims and provide adequate support for them? For experimental papers: consider the depth and/or breadth of the research questions investigated, technical soundness of experiments, methodological validity of evaluation. For position papers, surveys: consider the current state of the field is adequately represented, and main counter-arguments acknowledged. For resource papers: consider the data collection methodology, resulting data & the difference from existing resources are described in sufficient detail. Please adjust your baseline to account for the length of the paper."
    },
    "overall_assessment": {
        "order": 9,
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "optional": True
            }
        }
    },
    "best_paper": {
        "order": 10,
        "description": "Could this be a best paper in a top-tier *ACL venue?",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "Yes",
                    "Maybe",
                    "No"
                ],
                "input": "radio"
            }
        }
    },
    "best_paper_justification": {
        "order": 11,
        "description": "If the answer on best paper potential is Yes or Maybe, please justify your decision.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "replicability": {
        "order": 12,
        "description": "Will members of the ACL community be able to reproduce or verify the results in this paper?",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = They could easily reproduce the results.",
                    "4 = They could mostly reproduce the results, but there may be some variation because of sample variance or minor variations in their interpretation of the protocol or method.",
                    "3 = They could reproduce the results with some difficulty. The settings of parameters are underspecified or subjectively determined, and/or the training/evaluation data are not widely available.",
                    "2 = They would be hard pressed to reproduce the results: The contribution depends on data that are simply not available outside the author's institution or consortium and/or not enough details are provided.",
                    "1 = They would not be able to reproduce the results here no matter how hard they tried."
                ],
                "input": "radio",
                "optional": True
            }
        }
    },
    "datasets": {
        "order": 13,
        "description": "If the authors state (in anonymous fashion) that datasets will be released, how valuable will they be to others?",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = Enabling: The newly released datasets should affect other people's choice of research or development projects to undertake.",
                    "4 = Useful: I would recommend the new datasets to other researchers or developers for their ongoing work.",
                    "3 = Potentially useful: Someone might find the new datasets useful for their work.",
                    "2 = Documentary: The new datasets will be useful to study or replicate the reported research, although for other purposes they may have limited interest or limited usability. (Still a positive rating)",
                    "1 = No usable datasets submitted."
                ],
                "input": "radio",
                "optional": True
            }
        }
    },
    "software": {
        "order": 14,
        "description": "If the authors state (in anonymous fashion) that their software will be available, how valuable will it be to others?",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = Enabling: The newly released software should affect other people's choice of research or development projects to undertake.",
                    "4 = Useful: I would recommend the new software to other researchers or developers for their ongoing work.",
                    "3 = Potentially useful: Someone might find the new software useful for their work.",
                    "2 = Documentary: The new software will be useful to study or replicate the reported research, although for other purposes it may have limited interest or limited usability. (Still a positive rating)",
                    "1 = No usable software released."
                ],
                "input": "radio",
                "optional": True
            }
        }
    },
    "author_identity_guess": {
        "order": 15,
        "description": "Do you know the author identity or have an educated guess?",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = From a violation of the anonymity-window or other double-blind-submission rules, I know/can guess at least one author's name.",
                    "4 = From an allowed pre-existing preprint or workshop paper, I know/can guess at least one author's name.",
                    "3 = From the contents of the submission itself, I know/can guess at least one author's name.",
                    "2 = From social media/a talk/other informal communication, I know/can guess at least one author's name.",
                    "1 = I do not have even an educated guess about author identity."
                ],
                "input": "radio",
                "optional": True
            }
        }
    },
    "ethical_concerns": {
        "order": 16,
        "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "ethical_concernes": {
        "order": 17,
        "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "link_to_original_review": {
        "description": "Link to the review on the original ARR submission",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True
            }
        }
    },
    "limitations_and_societal_impact": {
        "order": 9,
        "description": "Have the authors adequately discussed the limitations and potential positive and negative societal impacts of their work? If not, please include constructive suggestions for improvement. Authors should be rewarded rather than punished for being up front about the limitations of their work and any potential negative societal impact. You are encouraged to think through whether any critical points are missing and provide these as feedback for the authors. Consider, for example, cases of exclusion of user groups, overgeneralization of findings, unfair impacts on traditionally marginalized populations, bias confirmation, under- and overexposure of languages or approaches, and dual use (see Hovy and Spruit, 2016, for examples of those). Consider who benefits from the technology if it is functioning as intended, as well as who might be harmed, and how. Consider the failure modes, and in case of failure, who might be harmed and how.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "needs_ethics_review": {
        "order": 11,
        "description": "Should this paper be sent for an in-depth ethics review? We have a small ethics committee that can specially review very challenging papers when it comes to ethical issues. If this seems to be such a paper, then please explain why here, and we will try to ensure that it receives a separate review.",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "Yes",
                    "No"
                ],
                "optional": True,
                "markdown": True,
                "input": "radio"
            }
        }
    },
    "reproducibility": {
        "order": 12,
        "description": "Is there enough information in this paper for a reader to reproduce the main results, use results presented in this paper in future work (e.g., as a baseline), or build upon this work?",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = They could easily reproduce the results.",
                    "4 = They could mostly reproduce the results, but there may be some variation because of sample variance or minor variations in their interpretation of the protocol or method.",
                    "3 = They could reproduce the results with some difficulty. The settings of parameters are underspecified or subjectively determined, and/or the training/evaluation data are not widely available.",
                    "2 = They would be hard pressed to reproduce the results: The contribution depends on data that are simply not available outside the author's institution or consortium and/or not enough details are provided.",
                    "1 = They would not be able to reproduce the results here no matter how hard they tried."
                ],
                "input": "radio",
                "optional": True
            }
        }
    }
}

official_review = openreview.api.Invitation(
    id=f"{confid}/-/ARR_Official_Review",
    invitees=[confid],
    signatures = [confid],
    readers = ['everyone'],
    writers = [confid],
    edit = {
        'signatures': [confid],
        'readers': [confid],
        'writers': [confid],
        'content': {
            'noteNumber': { 
                'value': {
                    'param': {
                        'regex': '.*', 'type': 'integer' 
                    }
                }
            },
            'noteId': {
                'value': {
                    'param': {
                        'regex': '.*', 'type': 'string' 
                    }
                }
            }
        },
        'replacement': True,
        'invitation': {
            'id': confid + '/Submission${2/content/noteNumber/value}/-/ARR_Official_Review',
            'signatures': [confid],
            'readers': [confid],
            'writers': [confid],
            'invitees': [confid],
            'edit': {     
                'signatures': { 'param': { 'regex': '.*' } },
                'readers': { 'param': { 'regex': '.*' } },
                'nonreaders': { 'param': { 'regex': '.*' } },
                'writers': [confid],
                'note': {
                    'ddate': {
                        'param': {
                            'range': [ 0, 9999999999999 ],
                            'optional': True,
                            'deletable': True
                        }
                    },
                    'id': {
                        'param': {
                            'withInvitation': confid + '/Submission${6/content/noteNumber/value}/-/ARR_Official_Review',
                            'optional': True
                        }
                    },
                    'forum': '${4/content/noteId/value}',
                    'replyto': '${4/content/noteId/value}',
                    'ddate': {
                        'param': {
                            'range': [ 0, 9999999999999 ],
                            'optional': True,
                            'deletable': True
                        }
                    },
                    'signatures': { 'param': { 'regex': '.*' } },
                    'readers': { 'param': { 'regex': '.*' } },
                    'nonreaders': { 'param': { 'regex': '.*' } },
                    'writers': [confid],
                    'content': official_review_content
                }
            }
        }
    }
)

client.post_invitation_edit(invitations=f"{confid}/-/Edit",
    readers=[confid],
    writers=[confid],
    signatures=[confid],
    invitation=official_review
)

meta_review_content = {
    "title": {
        "order": 1,
        "description": "Brief summary of your review.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "optional": True
            }
        }
    },
    "action_editor_id":{
        "order": 2,
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "optional": True
            }
        }
    },
    "metareview": {
        "order": 3,
        "description": "Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons (max 200000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "summary_of_reasons_to_publish": {
        "order": 4,
        "description": "What are the major reasons to publish this paper at a *ACL venue? This should help SACs at publication venues understand why they might want to accept the paper. Maximum 5000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "summary_of_suggested_revisions": {
        "order": 5,
        "description": "What revisions could the authors make to the research and the paper that would improve it? This should help authors understand the reviews in context, and help them plan any future resubmission. Maximum 5000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "overall_assessment": {
        "order": 6,
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = The paper is largely complete and there are no clear points of revision",
                    "4 = There are minor points that may be revised",
                    "3 = There are major points that may be revised",
                    "2 = The paper would need significant revisions to reach a publishable state",
                    "1 = Even after revisions, the paper is not likely to be publishable at an *ACL venue"
                ],
                "input": "radio",
                "optional": True
            }
        }
    },
    "suggested_venues": {
        "order": 7,
        "description": "You are encouraged to suggest conferences or workshops that would be suitable for this paper.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "ethical_concernes": {
        "order": 8,
        "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "link_to_original_metareview": {
        "description": "Link to the metareview on the original ARR submission",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "ethical_concerns": {
        "order": 6,
        "description": "Independent of your judgement of the quality of the work, please review the ACL code of ethics (https://www.aclweb.org/portal/content/acl-code-ethics) and list any ethical concerns related to this paper. Maximum length 2000 characters.",
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "needs_ethics_review": {
        "order": 11,
        "description": "Should this paper be sent for an in-depth ethics review? We have a small ethics committee that can specially review very challenging papers when it comes to ethical issues. If this seems to be such a paper, then please explain why here, and we will try to ensure that it receives a separate review.",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "Yes",
                    "No"
                ],
                "optional": True,
                "markdown": True,
                "input": "radio"
            }
        }
    },
    "best_paper_ae": {
      "order": 6,
      "description": "Could the camera-ready version of this paper merit consideration for an 'outstanding paper' award (up to 2.5% of accepted papers at *ACL conferences will be recognized in this way)? Outstanding papers should be either fascinating, controversial, surprising, impressive, or potentially field-changing. Awards will be decided based on the camera-ready version of the paper.",
      "value": {
            "param": {
                "type": "string",
                "enum": [
                    "Yes",
                    "Maybe",
                    "No"
                ],
                "input": "radio",
                "optional": True
            }
        },
    },
    "best_paper_ae_justification": {
      "order": 7,
      "description": "If you answered Yes or Maybe to the question about consideration for an award, please briefly describe why.",
      "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "great_reviews": {
      "order": 10,
      "description": "Please list the ids of all reviewers who went beyond expectations in terms of providing informative and constructive reviews and discussion. For example: jAxb, zZac",
      "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "poor_reviews": {
      "order": 11,
      "description": "Please list the ids of all reviewers whose reviews did not meet expectations. For example: jAxb, zZac",
      "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "markdown": True,
                "optional": True,
                "input": "textarea"
            }
        }
    },
    "author_identity_guess": {
        "order": 15,
        "description": "Do you know the author identity or have an educated guess?",
        "value": {
            "param": {
                "type": "string",
                "enum": [
                    "5 = From a violation of the anonymity-window or other double-blind-submission rules, I know/can guess at least one author's name.",
                    "4 = From an allowed pre-existing preprint or workshop paper, I know/can guess at least one author's name.",
                    "3 = From the contents of the submission itself, I know/can guess at least one author's name.",
                    "2 = From social media/a talk/other informal communication, I know/can guess at least one author's name.",
                    "1 = I do not have even an educated guess about author identity."
                ],
                "input": "radio",
                "optional": True
            }
        }
    }
}

metareview = openreview.api.Invitation(
    id=f"{confid}/-/ARR_Meta_Review",
    invitees=[confid],
    signatures = [confid],
    readers = ['everyone'],
    writers = [confid],
    edit = {
        'signatures': [confid],
        'readers': [confid],
        'writers': [confid],
        'content': {
            'noteNumber': { 
                'value': {
                    'param': {
                        'regex': '.*', 'type': 'integer' 
                    }
                }
            },
            'noteId': {
                'value': {
                    'param': {
                        'regex': '.*', 'type': 'string' 
                    }
                }
            }
        },
        'replacement': True,
        'invitation': {
            'id': confid + '/Submission${2/content/noteNumber/value}/-/ARR_Meta_Review',
            'signatures': [confid],
            'readers': [confid],
            'writers': [confid],
            'invitees': [confid],
            'edit': {     
                'signatures': { 'param': { 'regex': '.*' } },
                'readers': { 'param': { 'regex': '.*' } },
                'nonreaders': { 'param': { 'regex': '.*' } },
                'writers': [confid],
                'note': {
                    'ddate': {
                        'param': {
                            'range': [ 0, 9999999999999 ],
                            'optional': True,
                            'deletable': True
                        }
                    },
                    'id': {
                        'param': {
                            'withInvitation': confid + '/Submission${6/content/noteNumber/value}/-/ARR_Meta_Review',
                            'optional': True
                        }
                    },
                    'forum': '${4/content/noteId/value}',
                    'replyto': '${4/content/noteId/value}',
                    'ddate': {
                        'param': {
                            'range': [ 0, 9999999999999 ],
                            'optional': True,
                            'deletable': True
                        }
                    },
                    'signatures': { 'param': { 'regex': '.*' } },
                    'readers': { 'param': { 'regex': '.*' } },
                    'nonreaders': { 'param': { 'regex': '.*' } },
                    'writers': [confid],
                    'content': meta_review_content
                }
            }
        }
    }
)

client.post_invitation_edit(invitations=f"{confid}/-/Edit",
    readers=[confid],
    writers=[confid],
    signatures=[confid],
    invitation=metareview
)