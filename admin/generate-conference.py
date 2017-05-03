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

valid_duedate = False
while not valid_duedate:
	duedate_input = raw_input("Enter the duedate (DD/MM/YYYY): ")
	try:
		day, month, year = duedate_input.split('/')
		day = int(day)
		month = int(month)
		year = int(year)
		assert day <= 31, "Day must be less than or equal to 31"
		assert month <= 12, "Month must be less than or equal to 12"
		assert year >= datetime.datetime.now().year, "Cannot enter a year in the past"
		valid_duedate = True
	except AssertionError as e:
		print "Duedate invalid: ", e

valid_duetime = False
while not valid_duetime:
	duetime_input = raw_input("Enter the time of day that the \"%s\" is due in 24-hour format (e.g. enter 23:59 for 11:59 pm): " % submission_name)

	try:
		hour, minute = duetime_input.split(':')
		hour = int(hour)
		minute = int(minute)
		valid_duetime = True
	except:
		print "Time invalid."

duedate = utils.get_duedate(year, month, day, hour, minute)

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
	new_configfile.write(templatestring)

print "writing %s/webfield/conf.html" % directory
with open(directory + '/webfield/conf.html', 'w') as webfile:
	web_params = {
		"header": "This is the header",
		"title": "This is the title",
		"info": "This is the info",
		"url": "www.thisistheurl.com",
		"invitation": "%s/-/%s" % (conference, submission_name)
	}

	webfield = templates.Webfield(web_params)

	webfile.write(webfield.html)

print "writing %s/python/admin-init.py" % directory
with open(directory + '/python/admin-init.py', 'w') as new_initfile, open(utils.get_path('./conference-template/python/admin-init.template', __file__)) as template_initfile:
	templatestring = template_initfile.read().replace('<<UTILS_DIR>>', "\"%s\"" % utils.get_path('../utils', __file__))
	templatestring = templatestring.replace('<<SUBMISSION_DUEDATE>>', "%s" % duedate)
	new_initfile.write(templatestring)

print "writing %s/python/superuser-init.py" % directory
with open(directory + '/python/superuser-init.py', 'w') as new_initfile, open(utils.get_path('./conference-template/python/superuser-init.template', __file__)) as template_initfile:
	templatestring = template_initfile.read().replace('<<UTILS_DIR>>', "\"%s\"" % utils.get_path('../utils', __file__))
	templatestring = templatestring.replace('<<SUBMISSION_DUEDATE>>', "\"%s\"" % duedate)
	new_initfile.write(templatestring)
