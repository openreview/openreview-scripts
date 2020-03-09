import openreview
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    builder = openreview.helpers.get_conference_builder(client, 'Skx6tVahYB')

    builder.set_homepage_header({
        'title': '2020 European Conference on Computer Vision',
        'subtitle': 'ECCV 2020',
        #'deadline': 'Submission Start: Feb 01 2020 00:00 UTC-0, End: Mar 05 2020 23:59 UTC-0',
        'deadline': '',
        'date': 'Aug 23 2020',
        'website': 'https://eccv2020.eu/',
        'location': 'SEC, Glasgow',
        #'instructions': '<b>Instructions:</b> <a href="https://eccv2020.eu/author-instructions/" target="_blank">https://eccv2020.eu/author-instructions/</a>. You can update the information on this form at any time before the deadline.',
        'instructions': '''<p class="dark">
        <strong>New: Extended paper pre-registration</strong>
        <br> Please note that during the extended pre-registration period all registration problems will have to be resolved by the deadline of 5 March 2020 (23:59 UTC-0) (identical to the paper submission deadline). We will not be able to make any exceptions after this deadline.
        <br>We are looking forward to your submissions.
        </p>
        <p class="dark">
        <strong>Instructions:</strong> <a href="https://eccv2020.eu/author-instructions/" target="_blank">https://eccv2020.eu/author-instructions/</a>.
        You can update the information on this form at any time before the deadline.</p>
        <p class="dark">Deadline: 5 March 2020 (23:59 UTC-0)</p>''',
        'contact': 'eccv20program@gmail.com'
    })

    conference = builder.get_result()

    conference.default_reviewer_load = 7
    conference.set_reviewers()

    conference.set_submission_stage(openreview.builder.SubmissionStage(
        due_date = datetime.datetime(2020, 3, 5, 23, 59),
        public = False,
        double_blind = True,
        additional_fields = {
            'title': {
                'description': 'Title of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$',
                'order': 1,
                'value-regex': '.{1,250}',
                'required':True
            },
            "authors": {
                "description": "Comma separated list of author names.",
                "order": 2,
                "values-regex": "[^;,\\n]+(,[^,\\n]+)*",
                "required":True,
                "hidden":True
            },
            "authorids": {
                "description": "Search for authors by first and last name or by email address. Authors cannot be added after the deadline, so be sure to add all the authors of the paper. Take care to confirm that everyone added is actually a co-author, as there may be multiple OpenReview profiles with the same name.",
                "order": 3,
                "values-regex": "~.*",
                "required":True
            },
            'abstract': {
                'description': 'Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$',
                'order': 4,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':False
            },
            'TL;DR': {
                'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },
            'subject_areas': {
                'description': 'Select up to three subject areas.',
                'order': 6,
                'values-dropdown': [
                    "3D from Multi-view and Sensors",
                    "3D Point Clouds",
                    "3D from Single Images",
                    "3D Reconstruction",
                    "Action Recognition, Understanding",
                    "Adversarial Learning",
                    "Biologically Inspired Vision",
                    "Biomedical Image Processing",
                    "Biometrics",
                    "Computational Photography",
                    "Computer Vision for General Medical,  Biological and Cell Microscopy",
                    "Computer Vision Theory",
                    "Datasets and Evaluation",
                    "Deep Learning: Applications, Methodology, and Theory",
                    "Document Analysis",
                    "Driving Scene Analysis",
                    "Face, Gesture, and Body Pose",
                    "Human Computer Interaction",
                    "Image and Video Synthesis",
                    "Large Scale Methods",
                    "Low-level Vision",
                    "Machine Learning",
                    "Motion and Tracking",
                    "Optimization Methods",
                    "Physics-based Vision and Shape-from-X",
                    "Pose Estimation",
                    "Recognition: Detection, Categorization, Retrieval and Matching",
                    "Remote Sensing and Hyperspectral Imaging",
                    "Representation Learning",
                    "RGBD Sensors and Analytics",
                    "Scene Understanding",
                    "Security/Surveillance",
                    "Semi- and weakly-supervised Learning",
                    "Segmentation, Grouping and Shape",
                    "Statistical Learning",
                    "Stereo/Depth Estimation",
                    "Tracking",
                    "Transfer Learning",
                    "Unsupervised Learning",
                    "Video Analytics",
                    "Virtual and Augmented Reality",
                    "Vision and Graphics",
                    "Vision and Language",
                    "Vision Applications and Systems",
                    "Vision for Robotics",
                    "Visual Reasoning"
                                ],
                'required':False
            },
            'pdf': {
                'description': 'Upload a PDF file that ends with .pdf',
                'order': 9,
                'value-file': {
                    'fileTypes': ['pdf'],
                    'size': 50000000
                },
                'required':False
            },
            "author_agreement": {
                "value-checkbox": "All authors agree with the author guidelines of ECCV 2020.",
                'order': 10,
                "required": True
            },
            "TPMS_agreement": {
                "value-checkbox": "All authors agree that the manuscript can be processed by TPMS for paper matching.",
                'order': 11,
                "required": True
            }
        },
        remove_fields = ['keywords']
    ))


    conference.close_submissions()

    conference.create_blind_submissions(force=True, hide_fields=['pdf', 'supplementary_material'])

    ## Create withdraw invitations
    conference.create_withdraw_invitations()

    ## Create desk reject invitations
    conference.create_desk_reject_invitations()

    ## Create reference invitation to upload video/appendix pdf
    submissions = conference.get_submissions()
    for submission in submissions:

        id = conference.get_invitation_id('Supplementary_Material', submission.number)
        invitation = openreview.Invitation(
            id = id,
            duedate = openreview.tools.datetime_millis(datetime.datetime(2020, 3, 13, 14, 59)),
            readers = ['everyone'],
            writers = [conference.id],
            signatures = [conference.id],
            invitees = [conference.get_authors_id(number=submission.number)],
            multiReply = False, #only one revision?
            reply = {
                'forum': submission.original,
                'referent': submission.original,
                'readers': {
                    'values': [
                        conference.id, conference.get_authors_id(number=submission.number)
                    ]
                },
                'writers': {
                    'values': [
                        conference.id, conference.get_authors_id(number=submission.number)
                    ]
                },
                'signatures': {
                    'values-regex': '~.*'
                },
                'content': {
                    'supplementary_material': {
                        'order': 1,
                        'required': True,
                        'description': 'You can upload a single ZIP or a single PDF or a single MP4 file. Make sure that you do not use specialized codecs and the video runs on all computers. The maximum file size is 100MB.',
                        'value-file': {
                            'fileTypes': [
                                'pdf',
                                'zip',
                                'mp4'
                            ],
                            'size': 100
                        }
                    }
                }
            }
        )
        client.post_invitation(invitation)


    conference.setup_matching(affinity_score_file='./eccv-reviewer-scores.csv', tpms_score_file='./eccv-reviewer-tpms-scores.csv')

    conference.setup_matching(affinity_score_file='./eccv-area-chair-scores.csv', tpms_score_file='./eccv-area-chair-tpms-scores.csv', is_area_chair=True)

    instructions = '''<p class="dark"><strong>Instructions:</strong></p>
        <ul>
            <li>
                Please indicate your <strong>level of interest</strong> in
                reviewing the submitted papers below,
                on a scale from "Very Low" interest to "Very High" interest. Papers were automatically pre-ranked using the expertise information in your profile.
            </li>
            <li>
                Bid on as many papers as possible to correct errors of this automatic procedure.
            </li>
            <li>
                Bidding on the top ranked papers removes false positives.
            </li>
            <li>
                You can use the search field to find papers by keywords from the title or abstract to reduce false negatives.
            </li>
            <li>
                Ensure that you have at least <strong>{request_count} bids</strong>, which are "Very High" or "High".
            </li>
            <li>
                Papers for which you have a conflict of interest are not shown.
            </li>
        </ul>
        <br>'''
    conference.set_bid_stage(openreview.BidStage(#start_date = datetime.datetime(2020, 3, 6, 0, 0),
        due_date = datetime.datetime(2020, 3, 12, 23, 59), request_count = 40, use_affinity_score=True, instructions = instructions, ac_request_count=60))


    conference.open_recommendations(assignment_title='areachairs-1', due_date=datetime.datetime(2020, 3, 31, 14, 59))





