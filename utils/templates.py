import copy

class Webfield(object):
    """
    Class representing a standard webfield.

    :constructor parameters:
        params - a dictionary of parameters that may include:
            header: a string containing the header text for the webfield
            title: a string with the full title of the venue
            info: a string containing information such as dates, deadlines, and locations
            url: a url string, typically for the venue's external webpage
            invitation: a string matching the submission invitation's full ID
            html: TODO

        EXAMPLE:
            my_webfield = Webfield({
                'header': 'MCFNC 2017',
                "title": "MyConference 2017",
                "info": "Held on February 29, 2017, in Amherst, MA",
                "url": "www.myconference2017.org",
                "invitation": "my.conference/2017/-/Submission"
            })


    :attributes:
        html - the html string representing the webfield

    """

    def __init__(self, params):
        self.html = self.build_webfield(**params)

    def build_webfield(self, groupId='', invitationId='', title='', subtitle='', location='', date='', url=''):
        """

        Returns a string of HTML for making a standardized webfield

        :parameters:
        TODO

        :returns: a string with webfield HTML
        """

        webfield = """
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE = '%s';
var INVITATION = '%s';
var SUBJECT_AREAS = [
  // Add conference specific subject areas here
];
var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 50;

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required

  renderConferenceHeader();

  load().then(render).then(function() {
    Webfield.setupAutoLoading(INVITATION, PAGE_SIZE, paperDisplayOptions);
  });
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: '%s',
    subtitle: '%s',
    location: '%s',
    date: '%s',
    website: '%s',
    instructions: null,  // Add any custom instructions here. Accepts HTML
    deadline: ''
  });

  Webfield.ui.spinner('#notes');
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.api.getSubmissionInvitation(INVITATION, {deadlineBuffer: BUFFER});
  var notesP = Webfield.api.getSubmissions(INVITATION, {pageSize: PAGE_SIZE});

  return $.when(invitationP, notesP);
}

// Render is called when all the data is finished being loaded from the server
// It should also be called when the page needs to be refreshed, for example after a user
// submits a new paper.
function render(invitation, notes) {
  // Display submission button and form
  $('#invitation').empty();
  Webfield.ui.submissionButton(invitation, user, {
    onNoteCreated: function() {
      // Callback funtion to be run when a paper has successfully been submitted (required)
      load().then(render).then(function() {
        Webfield.setupAutoLoading(INVITATION, PAGE_SIZE, paperDisplayOptions);
      });
    }
  });

  // Display the list of all submitted papers
  $('#notes').empty();
  Webfield.ui.submissionList(notes, {
    heading: 'Submitted Papers',
    displayOptions: paperDisplayOptions,
    search: {
      enabled: true,
      subjectAreas: SUBJECT_AREAS,
      onResults: function(searchResults) {
        Webfield.ui.searchResults(searchResults, paperDisplayOptions);
        Webfield.disableAutoLoading();
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, paperDisplayOptions);
        Webfield.setupAutoLoading(INVITATION, PAGE_SIZE, paperDisplayOptions);
      }
    }
  });
}

// Go!
main();
        """ % (groupId, invitationId, title, subtitle, location, date, url)
        return webfield

class InvitationReply(object):
    """
    Base class representing an empty "reply" field of an Invitation

    :attributes:
        params - a dictionary containing the reply parameters.

    """
    def __init__(self, params=None):
        self.params = {
            'forum': None,
            'replyto': None,
            'invitation': None,
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values': ['everyone']
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': '~.*'
            },
            'writers': {
                'values-regex': '~.*'
            },
            'content': {}
        }

        if params:
            self.params.update(params)

class SubmissionReply(InvitationReply):
    """
    Class that extends InvitationReply. Provides default values for the "content" field.

    :attributes:
        content - a dictionary containing the content specification for the SubmissionInvitation
    """
    def __init__(self, params=None, content=None):
        InvitationReply.__init__(self, params)

        self.content = {
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.{1,250}',
                'required':True
            },
            'authors': {
                'description': 'Comma separated list of author names.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile.',
                'order': 3,
                'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required':True
            },
            'keywords': {
                'description': 'Comma separated list of keywords.',
                'order': 6,
                'values-regex': "(^$)|[^;,\\n]+(,[^,\\n]+)*"
            },
            'TL;DR': {
                'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
                'order': 7,
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 8,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'pdf': {
                'description': 'Upload a PDF file that ends with .pdf',
                'order': 9,
                'value-regex': 'upload',
                'required':True
            }
        }

        if content:
            self.content.update(content)

        self.body = copy.deepcopy(self.params)
        self.body.update({'content': self.content})

class CommentReply(InvitationReply):
    """
    Class that extends InvitationReply. Provides default values for the "content" field.

    :attributes:
        content - a dictionary containing the content specification for the SubmissionInvitation
    """
    def __init__(self, params=None, content=None):
        InvitationReply.__init__(self, params)

        self.content = {
              'title': {
                  'order': 0,
                  'value-regex': '.{1,500}',
                  'description': 'Brief summary of your comment.',
                  'required': True
              },
              'comment': {
                  'order': 1,
                  'value-regex': '[\\S\\s]{1,5000}',
                  'description': 'Your comment or reply.',
                  'required': True
              }
          }

        if content:
            self.content.update(content)

        self.body = copy.deepcopy(self.params)
        self.body.update({'content': self.content})
