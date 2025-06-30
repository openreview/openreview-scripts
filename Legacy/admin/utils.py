#!/usr/bin/python

import sys, os, inspect
import openreview
from subprocess import call
import argparse
import time, datetime

"""

utils.py

A collection of utility functions for openreview-scripts.

Scripts can import this file using the following code:

sys.path.insert(0, os.path.join(os.path.dirname(__file__),<relative_path_to_utils_directory>))
import utils

"""

def parse_args():
    """
    Sets up standard command line parameters for scripts.

    :parameters:
        None

    :returns: a tuple containing:
        args - the arguments object containing baseurl, overwrite, username, and password variables
        parser - the parser object (to allow users to add their own parameters)
        overwrite - a boolean representing the result of the overwrite variable
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base URL")
    parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False

    return args, parser, overwrite


def process_to_file(templatefile, outdir, suffix=None):
    """

    Calls the NodeJS script, processToFile.js, and writes .js process functions to the directory of choice.

    :parameters:
        templatefile - a path to the .template file that defines the process function
        outdir - a path to the directory where the resulting .js process functions should be saved
        suffix (default: None) - the suffix to append to the process function filename (TODO: Pam to clarify?)

    :returns:
        None
    """

    params = [
        "node",
        os.path.join(os.path.dirname(__file__), "processToFile.js"),
        templatefile,
        outdir
    ]
    if suffix: params.append(suffix)
    call(params)


def get_path(rel_path, _file):
    """

    Gets the absolute path from a path string relative to the directory containing _file

    :parameters:
        rel_path - a (possibly relative) path to the file of interest
        _file - the filename or directory that rel_path is relative to (__file__ variable is often passed in)

    :returns:
        a string containing the absolute path of rel_path

    """
    return os.path.abspath(os.path.join(os.path.dirname(_file), rel_path))

def get_duedate(year, month, day, hour=23, minute=59):
    """

    Returns the date given by the parameters represented in milliseconds since unix epoch time

    :parameters:
        year - an int representing the year
        month - int representing the month
        day - int representing the day
        hour (default: 23) - int representing the hour, using 24 hour format
        minute (default: 59) - int representing the minute

    :returns:
        an int that represents the date in milliseconds

    """
    return datetime.datetime(year, month, day, hour, minute)

def date_to_timestamp(date):
    return int(time.mktime(date.timetuple())) * 1000
