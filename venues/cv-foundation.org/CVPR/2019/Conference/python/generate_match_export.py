import openreview
from openreview import tools
from cvpr2019 import *

# Only after running the matcher successfully from within OR does this script get run.
# It goes through the assignment notes that it creates and generates an XML file
# which provides the list of reviewers for each paper submission.  The output file is
# ../data/reviewer_exports.xml

client = openreview.Client(baseurl='http://openreview.localhost', username='OpenReview.net', password='d0ntf33dth3tr0lls')
print(client)


assignment_notes = list(tools.iterget_notes(client, invitation=ASSIGNMENT_ID))
print(len(assignment_notes))
print(assignment_notes[0])


'''
<?xml version="1.0"?>
<assignments>
	<submission submissionId="1166">
		<user email="zhe.gan@microsoft.com"/>
		<user email="zizhao@cise.ufl.edu"/>
		<user email="zzhang3@snap.com"/>
	</submission>
'''
file = open(INPUT_FILES_DIR + "reviewers_export.xml",'w')
file.write("<?xml version=\"1.0\"?>\n<assignments>\n")
assignment_notes = tools.iterget_notes(client,invitation=ASSIGNMENT_ID)
i = 0
for assign_note in assignment_notes:
    i += 1
    paper_note = client.get_note(assign_note.forum)
    paper_num = paper_note.content['number']
    subm = '\t<submission submissionId="{0}">\n'.format(paper_num)
    for rev in assign_note.content['assignedGroups']:
        subm += '\t\t<user email="{0}"/>\n'.format(rev['userId'])
    subm += '\t</submission>\n'
    file.write(subm)
file.write("</assignments>")
file.close()
print("Wrote ",i, "assignments")
