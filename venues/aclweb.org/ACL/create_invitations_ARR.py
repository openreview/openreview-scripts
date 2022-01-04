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
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


# Posting submission invitation 
submission_invitation = openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/-/Submission",
    signatures = ["aclweb.org/ACL/2022/Conference"],
    readers = ["everyone"],
    invitees=["aclweb.org/ACL/2022/Conference"],
    reply={
        "readers":{
            "values":[
                "aclweb.org/ACL/2022/Conference"
            ]
            },
        "writers":{
            "values":[
                "aclweb.org/ACL/2022/Conference"
                ]
            },
        "signatures":{
            "values":[
                "aclweb.org/ACL/2022/Conference"
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
                "value-radio": [
                    "Ethics in NLP",
                    "Linguistic Theories, Cognitive Modeling and Psycholinguistics",
                    "Machine Learning for NLP",
                    "Phonology, Morphology and Word Segmentation",
                    "Resources and Evaluation",
                    "Semantics: Lexical",
                    "Semantics: Sentence level, Textual Inference and Other areas",
                    "Syntax: Tagging, Chunking and Parsing",
                    "Information Extraction",
                    "Computational Social Science and Cultural Analytics",
                    "Information Retrieval and Text Mining",
                    "Interpretability and Analysis of Models for NLP",
                    "Machine Translation and Multilinguality",
                    "NLP Applications",
                    "Question Answering",
                    "Dialogue and Interactive Systems",
                    "Discourse and Pragmatics",
                    "Generation",
                    "Language Grounding to Vision, Robotics, and Beyond",
                    "Sentiment Analysis, Stylistic Analysis, and Argument Mining",
                    "Speech and Multimodality",
                    "Summarization",
                    "Special Theme on Language Diversity: From Low Resource to Endangered Languages"
                    ],
                "required": True,
                "order": 12
                },
            "comments_to_the_senior_area_chairs": {
                "description": "Comment to Senior Area Chairs (500 words)",
                "order": 50,
                "value-regex": "[\\S\\s]{0,3000}",
                "required": False
                },
            "authorship": {
                "values-checkbox": [
                    "I confirm that I am one of the authors of this paper"
                ],
                "required": True,
                "order": 19
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
            "commitment_note":{
                "value-regex":".*",
                "required": True,
                "order": 30
            },
            "acl_preprint": {
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
            "values-regex": ".{1,500}",
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
        }
        }
    }  
)

client.post_invitation(submission_invitation)

# Posting Blind Submission Invitation 
blind = openreview.Invitation(
    id = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission',
    readers = [
        'everyone'
        ],
    writers = [
        'aclweb.org/ACL/2022/Conference'
        ],
    invitees = [
        'aclweb.org/ACL/2022/Conference'
        ],
    signatures = [
        'aclweb.org/ACL/2022/Conference'
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
                'aclweb.org/ACL/2022/Conference'
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

commitment = openreview.Invitation(
    id = 'aclweb.org/ACL/2022/Conference/-/Commitment_Submission',
    signatures = [
        "aclweb.org/ACL/2022/Conference"
        ],
    readers = [
        "everyone"
        ],
    invitees=[
        "everyone"
        ],
    reply={
        "readers":{
            "values-copied":[
                "aclweb.org/ACL/2022/Conference",
                "{content.authorids}",
                "{signatures}"
            ]
        },
        "writers": {
            "values-copied": [
                "aclweb.org/ACL/2022/Conference",
                "{content.authorids}",
                "{signatures}"
            ]
        },
        "signatures": { "values-regex": "~.*" },
        "content":{
            "title": {
            "description": "Enter the title of the ARR submission that you want to commit to ACL 2022",
            "order": 1,
            "value-regex": ".{1,250}",
            "required": True
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
        "ACL_preprint": {
            "description": "Would the authors like to have a public anonymous pre-print of the submission? This includes PDF, abstract and all supplemental material.",
            "value-radio": [
                "yes",
                "no"
            ],
            "required": True,
            "order": 16
        },
        "existing_preprints": {
            "values-regex": ".{1,500}",
            "description": "If there are any publicly available non-anonymous preprints of this paper, please list them here (provide the URLs please).",
            "required": False,
            "order": 17
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
                    "short",
                    "long"
                ],
                "required": True,
                "order": 11
                },
            "track": {
                "description": "Select the track that best fits your submission.",
                "value-radio": [
                    "Ethics in NLP",
                    "Linguistic Theories, Cognitive Modeling and Psycholinguistics",
                    "Machine Learning for NLP",
                    "Phonology, Morphology and Word Segmentation",
                    "Resources and Evaluation",
                    "Semantics: Lexical",
                    "Semantics: Sentence-level Semantics, Textual Inference and Other areas",
                    "Syntax: Tagging, Chunking and Parsing",
                    "Information Extraction",
                    "Computational Social Science and Cultural Analytics",
                    "Information Retrieval and Text Mining",
                    "Interpretability and Analysis of Models for NLP",
                    "Machine Translation and Multilinguality",
                    "NLP Applications",
                    "Question Answering",
                    "Dialogue and Interactive Systems",
                    "Discourse and Pragmatics",
                    "Generation",
                    "Language Grounding to Vision, Robotics, and Beyond",
                    "Sentiment Analysis, Stylistic Analysis, and Argument Mining",
                    "Speech and Multimodality",
                    "Summarization",
                    "Special Theme on Language Diversity: From Low Resource to Endangered Languages"
                ],
                "required": True,
                "order": 12
                },
            "comment": {
                "description": "Comment to Senior Area Chairs (500 words)",
                "order": 13,
                "value-regex": "[\\S\\s]{0,500}",
                "required": False
                },
            "authorship": {
            "values-checkbox": [
                "I confirm that I am one of the authors of this paper"
            ],
            "required": True,
            "order": 19
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
        }
        }
    }
)

official_review = openreview.Invitation(
    id = 'aclweb.org/ACL/2022/Conference/-/Official_Review',
    signatures= [
        'aclweb.org/ACL/2022/Conference'
    ],
    readers = [
        'everyone'
    ],
    writers = [
        'aclweb.org/ACL/2022/Conference'
    ],
    reply = {
        "readers" : {
            "values-regex":".*"
            },
        "nonreaders" : {
            "values-regex":".*"
            },
        "writers": {"values": [
                'aclweb.org/ACL/2022/Conference'
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
                "required": True,
                "markdown": True
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
                "comments,_suggestions_and_typos": {
                    "order": 8,
                    "value-regex": "[\\S\\s]{0,10000}",
                    "description": "If you have any comments to the authors about how they may improve their paper, other than addressing the concerns above, please list them here.\n Maximum length 5000 characters.",
                    "required": False,
                    "markdown": True
                },
                "overall_assessment": {
                    "order": 9,
                    "value-radio": [
                        "5 = Top-Notch: This paper has great merit, and easily warrants acceptance in a *ACL top-tier venue.",
                        "4.5 ",
                        "4 = Strong: This paper is of significant interest (for broad or narrow sub-communities), and warrants acceptance in a top-tier *ACL venue if space allows.",
                        "3.5 ",
                        "3 = Good: This paper is of interest to the *ACL audience and could be published, but might not be appropriate for a top-tier publication venue. It would likely be a strong paper in a suitable workshop.",
                        "2.5 ",
                        "2 = Borderline: This paper has some merit, but also significant flaws. It does not warrant publication at top-tier venues, but might still be a good pick for workshops.",
                        "1.5 ",
                        "1 = Poor: This paper has significant flaws, and I would argue against publishing it at any *ACL venue."
                    ],
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
                    "required": True,
                    "markdown": True
                    }
                }
            }
        )
client.post_invitation(official_review)

metareview = openreview.Invitation(
   id = 'aclweb.org/ACL/2022/Conference/-/Meta_Review',
    signatures = [
        'aclweb.org/ACL/2022/Conference'
    ],
    readers = [
        'everyone'
    ],
    writers = [
        'aclweb.org/ACL/2022/Conference'
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
                'aclweb.org/ACL/2022/Conference'
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
                "required": True,
                "markdown":True
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
                "required": True,
                "markdown": True
                }
            }
        } 
    )
client.post_invitation(metareview)