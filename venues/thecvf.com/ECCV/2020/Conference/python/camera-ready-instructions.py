import openreview
import time
from tqdm import tqdm
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help='base url')
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    all_papers = {note.forum: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}
    print('Found {} papers'.format(len(all_papers)))

    decision_notes = {note.forum: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/-/Decision$')}
    print('Found {} decision notes'.format(len(decision_notes)))

    print('Posting camera ready revision invitations')
    for id,s in tqdm(all_papers.items()):
        if s.forum in decision_notes and 'Accept' in decision_notes[s.forum].content['decision']:
            invitation = openreview.Invitation(
                id='thecvf.com/ECCV/2020/Conference/Paper{}/-/Camera_Ready_Revision'.format(s.number),
                readers=['everyone'],
                writers=['thecvf.com/ECCV/2020/Conference'],
                signatures=['thecvf.com/ECCV/2020/Conference'],
                invitees=['thecvf.com/ECCV/2020/Conference/Program_Chairs', "thecvf.com/ECCV/2020/Conference/Paper{}/Authors".format(s.number)],
                multiReply=True,
                duedate=1600214399000,
                reply={
                'forum': s.id,
                'referent': s.id,
                'readers': {
                    'values': [
                            "thecvf.com/ECCV/2020/Conference/Program_Chairs",
                            "thecvf.com/ECCV/2020/Conference/Paper{}/Area_Chairs".format(s.number),
                            "thecvf.com/ECCV/2020/Conference/Paper{}/Reviewers".format(s.number),
                            "thecvf.com/ECCV/2020/Conference/Paper{}/Authors".format(s.number)
                        ]
                },
                'writers': {
                    'values': ["thecvf.com/ECCV/2020/Conference/Program_Chairs", "thecvf.com/ECCV/2020/Conference/Paper{}/Authors".format(s.number)]
                },
                'signatures': {
                    'values': ["thecvf.com/ECCV/2020/Conference/Paper{}/Authors".format(s.number)]
                },
                'content': {
                    "title": {
                        "description": "Title of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                        "order": 1,
                        "value-regex": ".{1,250}",
                        "required": False
                    },
                    "abstract": {
                        "description": "Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                        "order": 2,
                        "value-regex": "[\\S\\s]{1,5000}",
                        "required": False
                    },                          
                    "source": {
                        "description": "All source files (LaTeX, style files, special fonts, figures, bib-files) and the camera ready PDF, in a single ZIP file. See Camera-ready submission instructions for full details. The maximum file size is 100MB",
                        "order": 3,
                        "value-file": {
                            "fileTypes": [
                                "zip"
                            ],
                            "size": 100
                        },
                        "required": True
                    },
                    "copyright": {
                        "description": "The ECCV main and ECCV Workshops copyrights are different, please upload a signed copy of the correct one. See Camera-ready submission instructions for full details. The maximum file size is 10MB",
                        "order": 4,
                        "value-file": {
                            "fileTypes": [
                                "pdf"
                            ],
                            "size": 10
                        },
                        "required": True
                    },
                    "supplementary_material": {
                        "description": "You can upload a single ZIP or a single PDF file. If you have a video, place it inside the ZIP file. Make sure that you do not use specialized codecs and the video runs on all computers. The maximum file size is 100MB.",
                        "value-file": {
                            "size": 100,
                            "fileTypes": [
                                "pdf",
                                "zip"
                            ]
                        },
                        "order": 5,
                        "required": False
                    },
                    "first_author_is_a_student": {
                        "description": "",
                        "order": 6,
                        "value-radio": ['Yes', 'No'],
                        "required": True
                    }
                }
            })
            client.post_invitation(invitation)


    email_subject = '''ECCV 2020: Camera ready paper instructions'''

    email_body = '''Dear Authors,

    The submission of camera-ready papers is now open in OpenReview. When you go to your paper in the Author console, you will find a button “camera-ready” to get to the submission form. 

    Note that this form only asks for the information for publishing the paper with Springer and ECVA. There will be another email with instructions to prepare the pre-recorded video material for the online conference. 

    For the detailed instructions on how to prepare the camera-ready papers, please visit
    https://eccv2020.eu/camera-ready-paper-guidelines/

    For your convenience, you find the same instructions below. Please follow these instructions closely. If you still have questions (after carefully reading the guidelines), please write directly to the publications chairs: eccv20pubs@eccv2020.eu

    ECCV 2020 Program Chairs

    --------------------------


    DEADLINE

    The submission deadline for camera ready material and copyright forms is July 17, 2020 (23:59 UTC-0). This deadline will not be extended. The ECCV 2020 proceedings will be published by Springer, in the LNCS series (Lecture Notes in Computer Science), and a version will be archived at the European Computer Vision Association (ECVA) site (https://www.ecva.net/).

    In order to cover the costs of the conference, while simultaneously promoting broad attendance, there is a Publication Fee of 450 GBP for each accepted paper (this includes one full Delegate Registration to the conference). This paper fee allows us to keep the Delegate Registration fee low (125 GBP for early registration), which will enable many more people to attend live and view your paper presentation during the conference. For your paper to be published, you must pay the Publication fee before the camera-ready deadline. Only one Publication Fee per paper must be paid, regardless of the number of authors. Any additional authors who wish to attend ECCV 2020 should use the normal Delegate Registration.  



    AUTHOR KIT

    The author kit for the camera ready manuscripts is the same for initial submissions. However, the authors need to change a few lines, indicated in the template with "% INITIAL SUBMISSION" and "% CAMERA READY". The code generating the line numbers is removed (there should be NO line numbers on the left and right side of the page), and author information is added. Please check the instructions in the commented areas of the tex file. If in doubt, please check the "eccv2020submissionCR.tex" file added to the kit, which incorporates the changes as an example.
    The camera ready manuscripts have to be prepared using LaTeX2e and the provided author kit:
    - Author kit for camera ready paper (Updated 16-06-2020) (https://eccv2020.eu/wp-content/uploads/2020/07/ECCV-2020-kit_16.06.2020.zip)
    - Springer LNCS author information (http://www.springer.com/computer/lncs?SGWID=0-164-6-793341-0)
    - LNCS author guidelines (http://static.springer.com/sgw/documents/1121537/application/pdf/SPLNPROC+Author+Instructions_June5.pdf)
    - LNCS LaTeX template (https://www.overleaf.com/latex/templates/springer-lecture-notes-in-computer-science/kzwwpvhwnvfj#.WsdHOy5uZpg)
    Author kits may be found on the Springer LNCS site (https://www.springer.com/in/computer-science/lncs/conference-proceedings-guidelines), under “Proceedings and Other Multiauthor Volumes“.



    INSTRUCTIONS AND POLICIES

    Paper length:

    Papers may be up to 14 pages long (excluding references). Important: Springer will edit the provided source files in order to insert running heads etc. and to smooth out any formatting inconsistencies. Hence, do not reduce the paper length, e.g., by reducing vertical spaces between paragraphs or the like, as this will be corrected by Springer, possibly resulting in an increase of the paper length. To avoid any problem, please use the author kit recommended above and follow its formatting instructions.

    Author names:

    Please write out author names in full in the paper, i.e. full given and family names. If any authors have names that can be parsed into FirstName LastName in multiple ways, please include the correct parsing in a comment to the editors, below the \author{} field. The list of authors must be consistent with the author list in OpenReview. 

    Copyright forms:

    Authors must submit a signed Consent to Publish form, through which the copyright of their paper is transferred to Springer. Please download the template of the form here:
    ECCV Copyright form (https://eccv2020.eu/wp-content/uploads/2020/07/ECCV-2020-Copyright-Form.pdf) (Updated 16-06-2020)

    Please fill this form, sign it, and scan it as a single PDF file, named XXXX-copyright.PDF, where XXXX is the four-digit paper ID (zero-padded if necessary). For example, if your paper ID is 24, the filename must be 0024-copyright.pdf. This file will be submitted separately. 

    If you have difficulty of printing and/or signing the pdf, a Word version is here, and you can add the signature as an image, before saving it as a pdf:
    ECCV-2020-Copyright-Form.doc ()

    You will see that the conference name and the names of the volume editors are entered in advance. Please note that the main conference proceedings and the workshop proceedings have different copyright forms, and make sure you use the correct one. One author may sign on behalf of all of the authors of a particular paper, provided that permission to do so has been accorded by the other authors in advance. We do not accept digital signatures. If you have any queries regarding copyright, please contact Springer or the Publication Chairs (eccv20pubs@eccv2020.eu) well in advance of publication. Accepted papers will be published by Springer (with appropriate copyrights) electronically after the main conference, but they will be made online at the ECVA website approximately three weeks after the submission of the camera ready paper. Please make sure to discuss this issue with your legal advisors as it pertains to public disclosure of the contents of the papers submitted, and contact the Publication Chairs if there is any sensitivity on the date of publication.

    For ECCV Workshop papers, use this template instead:
    ECCV Workshops Copyright form (Updated 16-06-2020)

    The corresponding Word version is here:
    ECCV-Workshop-2020-Copyright-Form.doc


    How to submit camera ready papers:

    We need all the source files (LaTeX files, style files, special fonts, figures, bib-files) that are required to compile papers, as well as the camera ready PDF. For each paper, one ZIP-file has to be prepared and submitted via the ECCV 2020 Submission Website (https://openreview.net/group?id=thecvf.com/ECCV/2020/Conference), using the password you received with your initial registration on that site. The size of the ZIP-file may not exceed the limit of 30 MByte. The ZIP-file has to contain the following:

    - All source files, e.g. LaTeX2e files for the text, PS/EPS or PDF/JPG files for all figures
    · Make sure to include any further style files and fonts you may have used.
    · References are to be supplied as BBL files to avoid omission of data while conversion from BIB to BBL.
    · Please do not send any older versions of papers. There should be one set of source files and one XXXX.pdf file per paper. Our typesetters require the author-created pdfs in order to check the proper representation of symbols, figures, etc.
    · You may use sub-directories.
    · Make sure to use relative paths for referencing files.
    · Make sure the source you submit compiles.
    · Please upload all the source files, including the camera ready XXXX.pdf, as a single ZIP file called XXXX.ZIP, where XXXX is the zero-padded, four-digit paper ID. Please upload this file (and optionally a supplemental file (https://www.springer.com/gp/authors-editors/journal-author/journal-author-helpdesk/preparation/1276?countryChanged=true)) in the “File Upload” page.

    - PDF file named “XXXX.pdf” that has been produced by the submitted source, where XXXX is the four-digit paper ID (zero-padded if necessary). For example, if your paper ID is 24, the filename must be 0024.pdf. This PDF will be used as a reference and has to exactly match the output of the compilation.
    
    - A PDF file named “XXXX-copyright.PDF”: a scanned version of the signed copyright form (see above), needs to be uploaded separately.


    If you wish to provide supplementary material, the file name must be in the form XXXX-supp.pdf or XXXX-supp.zip, where XXXX is the zero-padded, four-digit paper ID as used in the previous step. Upload your supplemental file on the “File Upload” page as a single PDF or ZIP file of 1 Gb in size or less.  Only PDF and ZIP files are allowed for supplementary material. You can put anything in this file – movies, code, additional results, accompanying technical reports–anything that may make your paper more useful to readers.  If your supplementary material includes video or image data, you are advised to use common codecs and file formats.  This will make the material viewable by the largest number of readers (a desirable outcome). ECCV encourages authors to submit videos using an MP4 codec such as DivX contained in an AVI. Also, please submit a README text file with each video specifying the exact codec used and a URL where the codec can be downloaded. Authors should refer to the contents of the supplementary material appropriately in the paper.

    Check that the upload of your file (or files) was successful either by matching the file length to that on your computer, or by using the download options that will appear after you have uploaded. Please ensure that you upload the correct camera-ready PDF–renamed to XXXX.pdf as described in the previous step as your camera-ready submission. Every year there is at least one author who accidentally submits the wrong PDF as their camera-ready submission.

    Springer is the first publisher to implement the ORCID identifier for proceedings, ultimately providing authors with a digital identifier that distinguishes them from every other researcher. ORCID (Open Researcher and Contributor ID) hosts a registry of unique researcher identifiers and a transparent method of linking research activities to these identifiers. This is achieved through embedding ORCID identifiers in key workflows, such as research profile maintenance, manuscript submissions, grant applications and patent applications.

    Please see https://www.springer.com/gp/authors-editors/orcid for more details. We encourage all contributing authors to also apply for an individual ORCID-ID at www.orcid.org and include these in their paper with \OrcidID command. (If you get an error with \OrcidID, you probably have an older class file; please download the last version of the Author kit for camera ready paper (https://eccv2020.eu/wp-content/uploads/2020/07/ECCV-2020-kit_16.06.2020-1.zip)).

    For each paper, the paper fee needs to be paid by the camera ready deadline. Without a valid payment by the deadline, your paper will not be published.

    For any question related to the publication process, please do not hesitate to contact the publication chairs (eccv20pubs@eccv2020.eu).


    Please kindly use the checklist below to deal with some of the most frequently encountered issues in ECCV submissions.

    FILES:
    ·  My submission package contains ONE compiled pdf file for the camera-ready version to go on Springerlink.
    ·  I have ensured that the submission package has all the additional files necessary for compiling the pdf on a standard LaTeX distribution.
    ·  The BBL file is included in my submission ZIP.
    ·  I have used the correct copyright form (with editor names pre-printed), and a manually signed and scanned PDF is submitted.
    CONTENT:
    ·  I have removed all \vspace and \hspace commands from my paper.
    ·  I have not used \cite command in the abstract.
    ·  I have read the Springer author guidelines, and complied with them, including the point on providing full information on editors and publishers for each reference in the paper (Author Guidelines – Section 2.8).
    ·  I have entered a correct \titlerunning{} command and selected a meaningful short name for the paper.
    ·  I have entered \index{Lastname, Firstname} commands for names that are longer than two words.
    ·  I have used the same name spelling in all my papers accepted to ECCV and ECCV Workshops.
    ·  I have not decreased the font size of any part of the paper to fit into 14 pages, I understand Springer editors will remove such commands.
    ·  (Optional but Recommended) I have inserted the ORCID identifiers of the authors in the paper header (see http://bit.ly/2H5xBpN for more information).
    SUBMISSION:
    ·  All author names, titles, and contact author information is correctly entered in the submission site.
    ·  The corresponding author e-mail is given.
    ·  Paper fee is paid by the camera ready deadline.
    '''

    batch_size = 100
    accepted_authors = client.get_group('thecvf.com/ECCV/2020/Conference/Authors/Accepted').members
    print('Sending mails to authors of {} papers'.format(len(accepted_authors)))
    for i in tqdm(range((len(accepted_authors)//batch_size) + 1)):
        start = i * 100
        end = start + 100
        curr = accepted_authors[start:end]
        x = client.post_message(subject=email_subject, recipients=curr, message=email_body)
        time.sleep(15)