import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv
from typing import *

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
                        "input": "textarea",
                        "optional": True
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
                        ],
                        "optional": True
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
            "migrated_paper_link": {
                "order": 30,
                "value": {
                    "param": {
                        "type": "string",
                        "minLength": 1,
                        "optional": True
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
                "type": "integer",
                "enum": [
                    { 'value': 5, 'description': '5 = Positive that my evaluation is correct. I read the paper very carefully and am familiar with related work.'},
                    { 'value': 4, 'description': "4 = Quite sure. I tried to check the important points carefully. It's unlikely, though conceivable, that I missed something that should affect my ratings."},
                    { 'value': 3, 'description': "3 = Pretty sure, but there's a chance I missed something. Although I have a good feel for this area in general, I did not carefully check the paper's details, e.g., the math or experimental design."},
                    { 'value': 2, 'description': "2 = Willing to defend my evaluation, but it is fairly likely that I missed some details, didn't understand some central points, or can't be sure about the novelty of the work."},
                    { 'value': 1, 'description': "1 = Not my area, or paper is very hard to understand. My evaluation is just an educated guess."}
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
                "type": "float",
                "enum": [
                    { 'value': 5, 'description': "5 = Excellent: This study is one of the most thorough I have seen, given its type."},
                    { 'value': 4.5, 'description': '4.5'},
                    { 'value': 4, 'description': "4 = Strong: This study provides sufficient support for all of its claims/arguments. Some extra experiments could be nice, but not essential."},
                    { 'value': 3.5, 'description': '3.5'},
                    { 'value': 3, 'description': "3 = Acceptable: This study provides sufficient support for its major claims/arguments. Some minor points may need extra support or details."},
                    { 'value': 2.5, 'description': '2.5'},
                    { 'value': 2, 'description': "2 = Poor: Some of the main claims/arguments are not sufficiently supported. There are major technical/methodological problems."},
                    { 'value': 1.5, 'description': '1.5'},
                    { 'value': 1, 'description': "1 = Major Issues: This study is not yet sufficiently thorough to warrant publication or is not relevant to ACL."}
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
                "type": "float",
                "enum": [
                    { 'value': 5, 'description': "5 = Top-Notch: This is one of the best papers I read recently, of great interest for the (broad or narrow) sub-communities that might build on it."},
                    { 'value': 4.5, 'description': '4.5'},
                    { 'value': 4, 'description': "4 = This paper represents solid work, and is of significant interest for the (broad or narrow) sub-communities that might build on it."},
                    { 'value': 3.5, 'description': '3.5'},
                    { 'value': 3, 'description': "3 = Good: This paper makes a reasonable contribution, and might be of interest for some (broad or narrow) sub-communities, possibly with minor revisions."},
                    { 'value': 2.5, 'description': '2.5'},
                    { 'value': 2, 'description': "2 = Revisions Needed: This paper has some merit, but also significant flaws, and needs work before it would be of interest to the community."},
                    { 'value': 1.5, 'description': '1.5'},
                    { 'value': 1, 'description': "1 = Major Revisions Needed: This paper has significant flaws, and needs substantial work before it would be of interest to the community."},
                    { 'value': 0.5, 'description': "0.5 = This paper is not relevant to the *ACL community (for example, is in no way related to natural language processing)."}
                ],
                    "input": "radio",
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
                "type": "integer",
                "enum": [
                    { 'value': 5, 'description': "5 = They could easily reproduce the results."},
                    { 'value': 4, 'description': "4 = They could mostly reproduce the results, but there may be some variation because of sample variance or minor variations in their interpretation of the protocol or method."},
                    { 'value': 3, 'description': "3 = They could reproduce the results with some difficulty. The settings of parameters are underspecified or subjectively determined, and/or the training/evaluation data are not widely available."},
                    { 'value': 2, 'description': "2 = They would be hard pressed to reproduce the results: The contribution depends on data that are simply not available outside the author's institution or consortium and/or not enough details are provided."},
                    { 'value': 1, 'description': "1 = They would not be able to reproduce the results here no matter how hard they tried."}
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
                "type": "integer",
                "enum": [
                    { 'value': 5, 'description': "5 = Enabling: The newly released datasets should affect other people's choice of research or development projects to undertake."},
                    { 'value': 4, 'description': "4 = Useful: I would recommend the new datasets to other researchers or developers for their ongoing work."},
                    { 'value': 3, 'description': "3 = Potentially useful: Someone might find the new datasets useful for their work."},
                    { 'value': 2, 'description': "2 = Documentary: The new datasets will be useful to study or replicate the reported research, although for other purposes they may have limited interest or limited usability. (Still a positive rating)"},
                    { 'value': 1, 'description': "1 = No usable datasets submitted."}
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
                "type": "integer",
                "enum": [
                    { 'value': 5, 'description': "5 = Enabling: The newly released software should affect other people's choice of research or development projects to undertake."},
                    { 'value': 4, 'description': "4 = Useful: I would recommend the new software to other researchers or developers for their ongoing work."},
                    { 'value': 3, 'description': "3 = Potentially useful: Someone might find the new software useful for their work."},
                    { 'value': 2, 'description': "2 = Documentary: The new software will be useful to study or replicate the reported research, although for other purposes it may have limited interest or limited usability. (Still a positive rating)"},
                    { 'value': 1, 'description': "1 = No usable software released."}
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
                "type": "integer",
                "enum": [
                    { 'value': 5, 'description': "5 = From a violation of the anonymity-window or other double-blind-submission rules, I know/can guess at least one author's name."},
                    { 'value': 4, 'description': "4 = From an allowed pre-existing preprint or workshop paper, I know/can guess at least one author's name."},
                    { 'value': 3, 'description': "3 = From the contents of the submission itself, I know/can guess at least one author's name."},
                    { 'value': 2, 'description': "2 = From social media/a talk/other informal communication, I know/can guess at least one author's name."},
                    { 'value': 1, 'description': "1 = I do not have even an educated guess about author identity."}
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
                "type": "integer",
                "enum": [
                    { 'value': 5, 'description': "5 = They could easily reproduce the results."},
                    { 'value': 4, 'description': "4 = They could mostly reproduce the results, but there may be some variation because of sample variance or minor variations in their interpretation of the protocol or method."},
                    { 'value': 3, 'description': "3 = They could reproduce the results with some difficulty. The settings of parameters are underspecified or subjectively determined, and/or the training/evaluation data are not widely available."},
                    { 'value': 2, 'description': "2 = They would be hard pressed to reproduce the results: The contribution depends on data that are simply not available outside the author's institution or consortium and/or not enough details are provided."},
                    { 'value': 1, 'description': "1 = They would not be able to reproduce the results here no matter how hard they tried."}
                ],
                "input": "radio",
                "optional": True
            }
        }
    }
}

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
                "type": "integer",
                "enum": [
                    { 'value': 5, 'description': "5 = The paper is largely complete and there are no clear points of revision"},
                    { 'value': 4, 'description': "4 = There are minor points that may be revised"},
                    { 'value': 3, 'description': "3 = There are major points that may be revised"},
                    { 'value': 2, 'description': "2 = The paper would need significant revisions to reach a publishable state"},
                    { 'value': 1, 'description': "1 = Even after revisions, the paper is not likely to be publishable at an *ACL venue"}
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
                "type": "integer",
                "enum": [
                    { 'value': 5, 'description': "5 = From a violation of the anonymity-window or other double-blind-submission rules, I know/can guess at least one author's name."},
                    { 'value': 4, 'description': "4 = From an allowed pre-existing preprint or workshop paper, I know/can guess at least one author's name."},
                    { 'value': 3, 'description': "3 = From the contents of the submission itself, I know/can guess at least one author's name."},
                    { 'value': 2, 'description': "2 = From social media/a talk/other informal communication, I know/can guess at least one author's name."},
                    { 'value': 1, 'description': "1 = I do not have even an educated guess about author identity."}
                ],
                "input": "radio",
                "optional": True
            }
        }
    }
}

ethics_review_content = {
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
    "recommendation": {
        "order": 9,
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "optional": True
            }
        }
    },
    "issues": {
        "order": 9,
        "value": {
            "param": {
                "type": "string[]",
                "enum": [
                    "1.1 Contribute to society and to human well-being, acknowledging that all people are stakeholders in computing",
                    "1.2 Avoid harm",
                    "1.3 Be honest and trustworthy",
                    "1.4 Be fair and take action not to discriminate",
                    "1.5 Respect the work required to produce new ideas, inventions, creative works, and computing artifacts",
                    "1.6 Respect privacy",
                    "1.7 Honor confidentiality",
                    "2.1 Strive to achieve high quality in both the processes and products of professional work",
                    "2.2 Maintain high standards of professional competence, conduct, and ethical practice",
                    "2.3 Know and respect existing rules pertaining to professional work",
                    "2.4 Accept and provide appropriate professional review",
                    "2.5 Give comprehensive and thorough evaluations of computer systems and their impacts, including analysis of possible risks",
                    "2.6 Perform work only in areas of competence",
                    "2.7 Foster public awareness and understanding of computing, related technologies, and their consequences",
                    "2.8 Access computing and communication resources only when authorized or when compelled by the public good",
                    "2.9 Design and implement systems that are robustly and usably secure",
                    "3.1 Ensure that the public good is the central concern during all professional computing work",
                    "3.2 Articulate, encourage acceptance of, and evaluate fulfillment of social responsibilities by members of the organization or group",
                    "3.3 Manage personnel and resources to enhance the quality of working life",
                    "3.4 Articulate, apply, and support policies and processes that reflect the principles of the Code",
                    "3.5 Create opportunities for members of the organization or group to grow as professionals",
                    "3.6 Use care when modifying or retiring systems",
                    "3.7 Recognize and take special care of systems that become integrated into the infrastructure of society",
                    "4.1 Uphold, promote, and respect the principles of the Code",
                    "4.2 Treat violations of the Code as inconsistent with membership in the ACM",
                    "None"
                ],
                "optional": True
            }
        }
    },
    "explanation": {
        "order": 9,
        "value": {
            "param": {
                "type": "string",
                "minLength": 1,
                "optional": True
            }
        }
    }
}

official_comment_content = {
    'title': {
        'order': 1,
        'description': '(Optional) Brief summary of your comment.',
        'value': {
            'param': {
                'type': 'string',
                'minLength': 1,
                'optional': True,
                'deletable': True
            }
        }
    },
    'comment': {
        'order': 2,
        'description': 'Your comment or reply (max 5000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq',
        'value': {
            'param': {
                'type': 'string',
                'minLength': 1,
                'markdown': True,
                'input': 'textarea'
            }
        }
    }
}

def migrate_notes(venue_id: str, submissions: list[Union[openreview.Note, openreview.api.Note]], commitment_dict: dict, previous_dict: dict, invitation_info: dict, migrated_prefix: str = 'ARR'):
    """
    Posts replies from the original submissions to the new venue

    venue_id (str): The destination conference that the data is being imported into
    submissions (list[Union[openreview.Note, openreview.api.Note]]): A list of submission notes
    commitment_dict (dict): Maps the commitment submission IDs to the ID of the migrated submission
    previous_dict (dict): Maps the commitment submission IDs to the previous note
    invitation_info (dict): Mapping from invitation suffixes to content dicts - used to keep track of which submission invitations to make
    migrated_prefix (str): Used to indicate the venue that these replies are coming from
    """
    # Get previous notes
    for submission in tqdm(submissions, total=len(submissions)):
        prev = previous_dict[submission.id]
        print(f"building replies for {submission.id} to migrated note {commitment_dict[submission.id]} using note {prev.id}")

        paper_prefix = f"{venue_id}/Submission{submission.number}"
        authors = f"{paper_prefix}/Authors"
        acs = f"{paper_prefix}/Area_Chairs"
        sacs = f"{paper_prefix}/Senior_Area_Chairs"
        pcs = f"{venue_id}/Program_Chairs"

        reply_queue = [prev.id]
        replyto_map = {prev.id: commitment_dict[submission.id]} ## Used to properly post comments
        while len(reply_queue) > 0:
            # Use BFS to parse reply tree and include author-reviewer responses
            prev.details['replies'].sort(key = lambda x: x['cdate']) ## Post older notes first
            curr_replyto = reply_queue.pop(0)
            filtered_replies = [reply for reply in prev.details['replies'] if reply['replyto'] == curr_replyto]

            for reply in filtered_replies:
                for suffix in invitation_info.keys(): ## Find what kind of reply this is
                    if suffix in reply['invitation']:
                        # Copy content fields and set title
                        new_content = {}
                        content = reply['content']
                        for key in content.keys():
                            if key not in new_content.keys():
                                new_content[key] = {}
                            new_content[key]['value'] = content[key]

                        new_content['title'] = {}
                        new_content['title']['value'] = f"{suffix.replace('_', ' ')} of Submission{submission.number} by {reply['invitation'].split('/')[4]} {reply['signatures'][0].split('/')[-1].replace('_', ' ')}"

                        # Special cases for content fields
                        ## TODO: Move this to content parsing
                        if 'Official_Review' in suffix:
                            for key in content.keys():
                                if key == 'comments,_suggestions_and_typos':
                                    continue
                                if 'type' in official_review_content[key]['value']['param'] and official_review_content[key]['value']['param']['type'] in ['integer', 'float'] and 'enum' in official_review_content[key]['value']['param']:
                                    if official_review_content[key]['value']['param']['type'] == 'integer':
                                        new_content[key]['value'] = int(content[key].split(' = ')[0])
                                    elif official_review_content[key]['value']['param']['type'] == 'float':
                                        val = float(content[key].split(' = ')[0])
                                        if val == 0:
                                            val = 0.5
                                        new_content[key]['value'] = val
                            if 'comments,_suggestions_and_typos' in reply['content'].keys():
                                new_content['comments_suggestions_and_typos'] = {'value': reply['content'].get('comments,_suggestions_and_typos')}
                                del new_content['comments,_suggestions_and_typos']
                        if 'Meta_Review' in suffix:
                            for key in content.keys():
                                if 'type' in meta_review_content[key]['value']['param'] and meta_review_content[key]['value']['param']['type'] in ['integer', 'float'] and 'enum' in meta_review_content[key]['value']['param']:
                                    if meta_review_content[key]['value']['param']['type'] == 'integer':
                                        new_content[key]['value'] = int(content[key].split(' = ')[0])
                                    elif meta_review_content[key]['value']['param']['type'] == 'float':
                                        val = float(content[key].split(' = ')[0])
                                        if val == 0:
                                            val = 0.5
                                        new_content[key]['value'] = val 
                        if 'Official_Comment' in suffix:

                            ## Only include comments between reviewers and authors
                            if not (any('Authors' in reader for reader in reply['readers']) and any('Reviewers' in reader for reader in reply['readers'])):
                                continue

                            if 'Author' in reply['signatures'][0]:
                                new_content['title']['value'] = new_content['title']['value'].replace('Comment', 'Rebuttal')
                            elif 'Reviewer' in reply['signatures'][0]:
                                new_content['title']['value'] = new_content['title']['value'].replace('Comment', 'Response')

                        # Set replyto
                        replyTo = commitment_dict[submission.id] if invitation_info[suffix]['type'] != 'comment' else replyto_map[curr_replyto]

                        rev = client.post_note_edit(
                            invitation=f"{paper_prefix}/-/{migrated_prefix}_{suffix}",
                            readers=[pcs, sacs, acs, venue_id],
                            writers=[venue_id],
                            signatures=[venue_id],
                            nonreaders = [f"{venue_id}/Submission{submission.number}/Conflicts"],
                            note=openreview.api.Note(
                                forum=commitment_dict[submission.id],
                                replyto=replyTo,
                                signatures=[venue_id],
                                readers=[pcs, sacs, acs, venue_id],
                                writers=[venue_id],
                                nonreaders = [f"{venue_id}/Submission{submission.number}/Conflicts"],
                                content=new_content
                            )
                        )
                        replyto_map[reply['id']] = rev['note']['id']
                        reply_queue.append(reply['id'])
                    ## TODO: Handle this better
                    if reply['invitation'].endswith('Rebuttal'): ## Special cases for non 1-1 mappings between invitations
                        suffix = 'Official_Comment'

                        new_content = {}
                        content = reply['content']
                        for key in content.keys():
                            if key == 'rebuttal':
                                new_content['comment'] = {}
                                new_content['comment']['value'] = content[key]
                            else:
                                if key not in new_content.keys():
                                    new_content[key] = {}

                        new_content['title'] = {}
                        new_content['title']['value'] = f"Rebuttal of Submission{submission.number} by {reply['invitation'].split('/')[4]} {reply['signatures'][0].split('/')[-1].replace('_', ' ')}"

                        rev = client.post_note_edit(
                            invitation=f"{paper_prefix}/-/{migrated_prefix}_{suffix}",
                            readers=[pcs, sacs, acs, venue_id],
                            writers=[venue_id],
                            signatures=[venue_id],
                            nonreaders = [f"{venue_id}/Submission{submission.number}/Conflicts"],
                            note=openreview.api.Note(
                                forum=commitment_dict[submission.id],
                                replyto=replyto_map[curr_replyto],
                                signatures=[pcs],
                                readers=[pcs, sacs],
                                writers=[venue_id],
                                nonreaders = [f"{venue_id}/Submission{submission.number}/Conflicts"],
                                content=new_content
                            )
                        )
                        replyto_map[reply['id']] = rev['note']['id']
                        reply_queue.append(reply['id'])

def post_submission_invitations(venue_id: str, forums: dict, invitation_info: dict, migrated_prefix: str = 'ARR'):
    """
    Creates new submission invitations for posting notes to the destination forums

    Args:
        venue_id (str): The destination conference that the data is being imported into
        forums (dict): Maps commitment paper number to migrated forum ID
        invitation_info (dict): Mapping from super invitation IDs to content dicts - used to keep track of which submission invitations to make
        migrated_prefix (str): Used to indicate the venue that these replies are coming from
    """
    for commitment_paper_number, migrated_forum in forums.items():
        for invitation_suffix, metadata in invitation_info.items():
            print(f"creating submission invitations for {venue_id}/-/{migrated_prefix}_{invitation_suffix}")
            if metadata['type'] != 'submission':
                client.post_invitation_edit(
                    invitations=f"{venue_id}/-/{migrated_prefix}_{invitation_suffix}",
                    readers=[venue_id],
                    writers=[venue_id],
                    signatures=[venue_id],
                    content={
                        'noteId': {
                            'value': migrated_forum
                        },
                        'noteNumber': {
                            'value': commitment_paper_number
                        }
                    },
                    invitation=openreview.api.Invitation()
                )

def post_super_invitations(venue_id: str, invitation_info: dict, migrated_prefix: str = 'ARR'):
    """
    Creates new invitations for posting child invitations to the destination forums

    Args:
        venue_id (str): The destination conference that the data is being imported into
        invitation_info (dict): Mapping from super invitation IDs to content dicts for the note
        migrated_prefix (str): Used to indicate the venue that these replies are coming from
    """
    def _set_submission_invitation (invitation_name: str, content: dict):
        # Change venueid to match new invitation
        content['venueid']['value']['param']['const'] = content['venueid']['value']['param']['const'].replace('Submission', invitation_name)
        content['venue']['value']['param']['const'] = content['venue']['value']['param']['const'].replace('Submission', invitation_name.replace('_', ' '))

        submission_invitation = openreview.api.Invitation(
            id=f"{venue_id}/-/{migrated_prefix}_{invitation_name}",
            invitees = ['~'],
            signatures = [venue_id],
            readers = ['everyone'],
            writers = [venue_id],
            edit = {
                'signatures': [venue_id],
                'readers': { 'param': { 'regex': '.*' } },
                'nonreaders': { 'param': { 'regex': '.*' } },
                'writers': [venue_id],
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
                            'withInvitation': f"{migrated_prefix}_{invitation_name}",
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
                    'signatures': [venue_id],
                    'readers': { 'param': { 'regex': '.*' } },
                    'nonreaders': { 'param': { 'regex': '.*' } },
                    'writers': [venue_id],
                    'content': content
                }
            }
        )
        client.post_invitation_edit(
            invitations=f"{venue_id}/-/Edit",
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=submission_invitation
        )
        print(f'posting {venue_id}/-/{invitation_name}')
    def _set_forum_reply_invitation (invitation_name: str, content: dict, is_comment: bool = False):
        forum_reply_invitation = openreview.api.Invitation(
            id=f"{venue_id}/-/{migrated_prefix}_{invitation_name}",
            invitees=[venue_id],
            signatures = [venue_id],
            readers = ['everyone'],
            writers = [venue_id],
            edit = {
                'signatures': [venue_id],
                'readers': [venue_id],
                'writers': [venue_id],
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
                    'id': venue_id + '/Submission${2/content/noteNumber/value}/-/' + f"{migrated_prefix}_{invitation_name}",
                    'signatures': [venue_id],
                    'readers': [venue_id],
                    'writers': [venue_id],
                    'invitees': [venue_id],
                    'edit': {     
                        'signatures': { 'param': { 'regex': '.*' } },
                        'readers': { 'param': { 'regex': '.*' } },
                        'nonreaders': { 'param': { 'regex': '.*' } },
                        'writers': [venue_id],
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
                                    'withInvitation': venue_id + '/Submission${6/content/noteNumber/value}/-/' + f"{migrated_prefix}_{invitation_name}",
                                    'optional': True
                                }
                            },
                            'forum': '${4/content/noteId/value}',
                            'replyto': '${4/content/noteId/value}' if not is_comment else
                                { 
                                    'param': {
                                        'withForum': '${6/content/noteId/value}', 
                                    }
                                },
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
                            'writers': [venue_id],
                            'content': content
                        }
                    }
                }
            }
        )
        client.post_invitation_edit(
            invitations=f"{venue_id}/-/Edit",
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=forum_reply_invitation
        )
        print(f'posting {venue_id}/-/{migrated_prefix}_{invitation_name}')
    for invitation_suffix, metadata in invitation_info.items():
        inv_type, content = metadata.get('type'), metadata.get('content', {})
        if inv_type == 'submission':
            _set_submission_invitation(invitation_suffix, content)
        elif inv_type == 'forum_reply':
            _set_forum_reply_invitation(invitation_suffix, content)
        elif inv_type == 'comment':
            _set_forum_reply_invitation(invitation_suffix, content, is_comment=True)


def update_existing_invitations(invitation_info: dict):
    """
    Updates the existing invitations with new inferred content

    Args:
        invitation_info (dict): Mapping from super invitation IDs to content dicts for the note
    """
    def __update_invitation():
        pass
    pass

def post_migrated_submissions(venue_id: str, submissions: list[Union[openreview.Note, openreview.api.Note]], migrated_prefix: str = 'ARR', submission_name: str = 'Submission'):
    """
    Creates new submission invitations for posting notes to the destination forums

    Args:
        venue_id (str): The destination conference that the data is being imported into
        submissions (list[Union[openreview.Note, openreview.api.Note]]): A list of submission notes
        migrated_prefix (str): Used to indicate the venue that these replies are coming from
        submission_name (str): The invitation name for submissions
    Returns:
        dict: Maps the commitment submission IDs to the ID of the migrated submission and the commitment paper number
    """

    commitment_dict = {}
    for submission in submissions:
        # Manual changes to content fields
        submission.content['commitment_note'] = {}
        submission.content['commitment_note']['value'] = f"https://openreview.net/forum?id={submission.id}"
        submission.content['authors']['readers'] = [
            venue_id,
            f"{venue_id}/Submission{submission.number}/Authors"
        ]
        submission.content['authorids']['readers'] = [
            venue_id,
            f"{venue_id}/Submission{submission.number}/Authors"
        ]
        submission.content['venueid']['value'] = submission.content['venueid']['value'].replace('Submission', f"{submission_name}")
        submission.content['venue']['value'] = submission.content['venue']['value'].replace('Submission', f"{submission_name.replace('_', ' ')}")

        # Build and post note
        blinded_note = openreview.api.Note(
            readers = [
                f"{venue_id}/Program_Chairs",
                venue_id,
                f"{venue_id}/Submission{submission.number}/Reviewers", f"{venue_id}/Submission{submission.number}/Area_Chairs", f"{venue_id}/Submission{submission.number}/Senior_Area_Chairs"
            ],
            nonreaders = [
                f"{venue_id}/Submission{submission.number}/Conflicts"
            ],
            writers = [
                venue_id
            ],
            signatures = [
                venue_id
            ],
            content = submission.content
        )
        blinded_note_posted = client.post_note_edit(
            invitation = f"{venue_id}/-/{migrated_prefix}_{submission_name}",
            signatures=[venue_id],
            readers = [
                f"{venue_id}/Program_Chairs",
                venue_id,
                f"{venue_id}/Submission{submission.number}/Reviewers", f"{venue_id}/Submission{submission.number}/Area_Chairs", f"{venue_id}/Submission{submission.number}/Senior_Area_Chairs"
            ],
            nonreaders = [
                f"{venue_id}/Submission{submission.number}/Conflicts"
            ],
            writers = [
                venue_id
            ],
            note=blinded_note
        )
        print(f"posted {blinded_note_posted['note']['id']} for commitment {submission.id}")
        commitment_dict[submission.id] = {'migrated_id': blinded_note_posted['note']['id'], 'commitment_number': submission.number}

        # Update commitment note with link
        client.post_note_edit(
            invitation = f"{venue_id}/-/Edit",
            signatures=[venue_id],
            readers = [venue_id],
            nonreaders = [f"{venue_id}/Submission{submission.number}/Conflicts"],
            writers = [venue_id],
            note=openreview.api.Note(
                id=submission.id,
                content={'migrated_paper_link': {'value': f"https://openreview.net/forum?id={blinded_note_posted['note']['id']}"}}
            )
        )

    return commitment_dict


def infer_content_from_invitations(venue_id: str, venue_ids: List[str], invitation_suffixes: List[str]):
    """
    Fetches the reply content for each venue for each invitation and returns a content dict
    that allows for all previously submitted fields

    Args:
        venue_id (str): The destination conference that the data is being imported into
        venue_ids (List[str]): A list of valid venue IDs
        invitation_suffixes (List[str]): Extracted from the invitation IDs - the string following /-/

    Returns:
        dict: Maps the invitation IDs to the final content dicts

    Raises:
        OpenReviewException: If a venue or invitation does not exist
    """
    def _get_content(invitation: openreview.api.Invitation):
        pass
    if any('ACL/ARR' in venue for venue in venue_ids):
        # Do some additional filtering on submission content
        ## TODO: Parameterize Submission and Official_Comment invitation names
        commitment_invitation = client.get_invitation(f"{venue_id}/-/Submission")
        for key in commitment_invitation.edit['note']['content'].keys(): 
            if key not in ['existing_preprints', 'authors', 'authorids', 'keywords']:
                submission_invitation_content[key] = commitment_invitation.edit['note']['content'][key]
        return {
            'Official_Review': {
                'type': 'forum_reply',
                'content': official_review_content
            },
            'Meta_Review': {
                'type': 'forum_reply',
                'content': meta_review_content
            },
            'Ethics_Review': {
                'type': 'forum_reply',
                'content': ethics_review_content
            },
            'Migrated_Submission': {
                'type': 'submission',
                'content': submission_invitation_content
            },
            'Official_Comment': {
                'type': 'comment',
                'content': official_comment_content
            }
        }

"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password

"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl_v1', help="base URL pointing to API2", default='http://localhost:3000')
parser.add_argument('--baseurl_v2', help="base URL pointing to API1", default='http://localhost:3001')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--confid')
parser.add_argument('--paper_link_field', default='paper_link')
parser.add_argument('--post_to_commitment', action='store_true')
args = parser.parse_args()
client = openreview.api.OpenReviewClient(baseurl=args.baseurl_v2, username=args.username, password=args.password)
client_v1 = openreview.Client(baseurl=args.baseurl_v1, username=args.username, password=args.password)
confid = args.confid
paper_link_field = args.paper_link_field
post_to_commitment = args.post_to_commitment

# TODO: Build content dicts from invitations so they never go out of date
# TODO: Add support for migration_prefix = None -> removes _
# TODO: Add better support for posting other invitations as comments (Rebuttal -> Official_Comment)
# TODO: Move content parsing from migrate_notes to infer_content
# TODO: Post comment to commitment submissions with migrated paper link
# TODO: Add support for posting directly to the official/meta review invitations for venues that don't require reviewers/ACs so correct information is shown in the consoles
# TODO: Migrate conflict logic

# Load migration invitation contents
submission_invitation_name = ''
invitation_info = infer_content_from_invitations(confid, ['ACL/ARR'], [])
for name, info in invitation_info.items():
    if info['type'] == 'submission':
        submission_invitation_name = name
print(f"Migrating replies from {invitation_info.keys()}")

# Post/update super invitations
post_super_invitations(confid, invitation_info)

# Get all submissions + map submission IDs to previous paper (if not blind copy, get blind copy)
previous_dict = {}
submissions = client.get_all_notes(content={ 'venueid': f"{confid}/Submission" }, details='replies', sort='cdate:desc')
for submission in submissions:
    previous_id = submission.content[paper_link_field]['value'].split('?id=')[1].split('&')[0]
    previous_dict[submission.id] = client_v1.get_all_notes(id=previous_id, details='replies')[0]

# Post migrated submissions
if not post_to_commitment:
    migration = post_migrated_submissions(confid, submissions, 'ARR', submission_invitation_name)
    forums = {v['commitment_number']: v['migrated_id'] for v in migration.values()}
    commitment_dict = {k: v['migrated_id'] for k, v in migration.items()}
else:
    forums = {submission.number: submission.forum for submission in submissions}
    commitment_dict = {submission.id: submission.id for submission in submissions}

# Post/update submission invitations
post_submission_invitations(confid, forums, invitation_info, migrated_prefix='ARR')

# Migrate replies to migrated submissions
migrate_notes(confid, submissions, commitment_dict, previous_dict, invitation_info)
