# For now, run this script from /openreview-scripts

import sys, os, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../utils"))
import utils
import templates
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--test', help="base URL")
args = parser.parse_args()


conference = raw_input("Enter the full path of the conference group you would like to create (e.g. my-conference.org/MYCONF/2017): ")
directory = utils.get_path('../venues/%s' % conference, __file__)
submission_name = raw_input("Enter the name of the submission (press enter for default: \"Submission\"): " )

if submission_name.strip() == '':
	submission_name = "Submission"

# check if due date/time is valid and after current time
duedate_input = raw_input("Enter the duedate (DD/MM/YYYY): ")
try:
	day, month, year = duedate_input.split('/')
	day = int(day)
	month = int(month)
	year = int(year)
	# this will catch invalid values for date
	duedate = utils.get_duedate(year, month, day)
	now = datetime.datetime.now()
	assert duedate > now, "Cannot enter a date in the past"

	# get due time
	duetime_input = raw_input(
		"Enter the time of day that the \"%s\" is due in 24-hour format (e.g. enter 23:59 for 11:59 pm): " % submission_name)
	hour, minute = duetime_input.split(':')
	hour = int(hour)
	minute = int(minute)
	duedate = utils.get_duedate(year, month, day, hour, minute)
	assert duedate > now, "Cannot enter a time in the past"
except Exception, e:
	print "Duedate invalid: ", e
	sys.exit()

duedate_milliseconds = utils.date_to_timestamp(duedate)

assert not os.path.exists(directory), "%s already exists" % conference

print "Creating conference directory at %s" % directory
os.makedirs(directory)
os.makedirs(directory + '/python')
os.makedirs(directory + '/webfield')
os.makedirs(directory + '/process')
os.makedirs(directory + '/data')

print "writing %s/python/config.py" % directory
with open(directory + '/python/config.py', 'w') as new_configfile, open(utils.get_path('./conference-template/python/config.template', __file__)) as template_configfile:
	templatestring = template_configfile.read().replace('<<CONF>>', "\"%s\"" % conference)
	templatestring = templatestring.replace('<<UTILS_DIR>>', "\"%s\"" % utils.get_path('../utils', __file__))
	templatestring = templatestring.replace('<<SUBMISSION_NAME>>',submission_name)
	templatestring = templatestring.replace('<<TIMESTAMP>>',str(duedate_milliseconds))
	new_configfile.write(templatestring)

print "writing %s/webfield/conf.html" % directory
with open(directory + '/webfield/conf.html', 'w') as webfile:
	web_params = {
		"groupId": conference,
		"invitationId": "%s/-/%s" % (conference, submission_name),
		"title": "This is the title",
		"subtitle": "This is the subtitle",
		"location" : "This is the location",
		"date": duedate.strftime('%Y-%m-%d %H:%M:%S'),
		"url": "www.thisistheurl.com"
	}

	webfield = templates.Webfield(web_params)

	webfile.write(webfield.html)

print "writing %s/python/admin-init.py" % directory
with open(directory + '/python/admin-init.py', 'w') as new_initfile, open(utils.get_path('./conference-template/python/admin-init.template', __file__)) as template_initfile:
	templatestring = template_initfile.read().replace('<<UTILS_DIR>>', "\"%s\"" % utils.get_path('../utils', __file__))
	templatestring = templatestring.replace('<<SUBMISSION_DUEDATE>>', "%s" % duedate_milliseconds)
	new_initfile.write(templatestring)

print "writing %s/python/superuser-init.py" % directory
with open(directory + '/python/superuser-init.py', 'w') as new_initfile, open(utils.get_path('./conference-template/python/superuser-init.template', __file__)) as template_initfile:
	templatestring = template_initfile.read().replace('<<UTILS_DIR>>', "\"%s\"" % utils.get_path('../utils', __file__))
	templatestring = templatestring.replace('<<SUBMISSION_DUEDATE>>', "\"%s\"" % duedate_milliseconds)
	new_initfile.write(templatestring)
