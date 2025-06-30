import openreview

# initialize a Client
admin_client = openreview.Client(username = 'uai2018admin', password = 'your_password', baseurl = 'https://openreview.net')

# get the group representing the Senior Program Committee
spc = admin_client.get_group('auai.org/UAI/2018/Senior_Program_Committee')
print "Before : ", spc
print "\n"

# add a member to the spc group
spc = admin_client.add_members_to_group(spc, ['~Michael_Spector1'])
print "Adding ~Michael_Spector1: ", spc
print "\n"

# remove a member from the spc group
spc = admin_client.remove_members_from_group(spc, ['~Michael_Spector1'])
print "Removing ~Michael_Spector1: ", spc
