import argparse
import openreview
import openreview_matcher
import config

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true', help = "if present, erases the old assignment note")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

def clear_configs():
    print "clearing assignment notes..."
    configs = client.get_notes(invitation=config.ASSIGNMENT)
    for n in configs:
        client.delete_note(n)


clear_configs()

matching_configuration = {
    "assignment_label": 'reviewers',
    "group": config.PC,
    "submission": config.SUBMISSION,
    "metadata": config.METADATA,
    "minusers": 3,
    "maxusers": 5,
    "minpapers": 1,
    "maxpapers": 15,
    "weights": {
        "primary_subject_overlap": 0,
        "secondary_subject_overlap": 0,
        "bid_score": 0,
        "ac_recommendation": 0,
        "basic_affinity": 1
    }
}

# define note parameters for the configuration note
note_params = {
    'invitation': config.ASSIGNMENT,
    'readers': [config.CONFERENCE],
    'writers': [config.CONFERENCE],
    'signatures': [config.CONFERENCE],
    'content': {
        'configuration': matching_configuration
    }
}

configuration_note = client.post_note(openreview.Note(**note_params))
print "posted assignment note {0}".format(configuration_note.id)
