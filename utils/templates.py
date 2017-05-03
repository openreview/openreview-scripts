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

    def build_webfield(self, header='', title='', info='', url='', invitation='', html = ''):
        """

        Returns a string of HTML for making a standardized webfield

        :parameters:
        TODO

        :returns: a string with webfield HTML
        """

        webfield = """
        <html>
          <head>
          </head>
          <body>
            <div id='main'>
              <div id='header'></div>
              <div id='invitation'></div>
              <div id='notes'></div>
            </div>
            <script type="text/javascript">
            $(function() {

              $attach('#header', 'mkHostHeader', [
              '%s', '%s', '%s', '%s'
              ], true);

              var sm = mkStateManager();

              var httpGetP = function(url, queryOrBody) {
                var df = $.Deferred();
                httpGet(url, queryOrBody,
                function(result) {
                  df.resolve(result);
                },
                function(result) {
                  df.reject(result);
                });
                return df.promise();
              };

              var invitationP = httpGetP('invitations', {id: '%s'}).then(function(result) {
                var valid_invitations = _.filter(result.invitations, function(inv){
                  return inv.duedate > Date.now();
                })

                return valid_invitations[0];

              },
              function(error){
                return error
              });

              var notesP = httpGetP('notes', {invitation: '%s'}).then(function(result) {
                return result.notes;
              },
              function(error){
                return error
              });


              $.when(invitationP, notesP).done(function(invitation, notes) {
                console.log('invitation',invitation)
                if(invitation){
                  sm.update('invitationTrip', {
                    invitation: invitation
                  });
                }
                sm.update('notes', notes);

                sm.addHandler('conference', {
                  invitationTrip: function(invitationTrip) { if (invitationTrip) {
                    var invitation = invitationTrip.invitation;
                    $attach('#invitation', 'mkInvitationButton', [invitation, function() {
                      if (user && !user.id.startsWith('guest_') && invitation) {
                        view.mkNewNoteEditor(invitation, null, null, user, {
                          onNoteCreated: function(idRecord) {
                            httpGetP('notes', {
                              invitation: '%s'
                            }).then(function(result) {
                              console.log("time to update notes: " + result.notes.length);
                              sm.update('notes', result.notes);
                            },
                            function(error){
                              return error
                            });
                          },
                          onCompleted: function(editor) {
                            $('#notes').prepend(editor);
                          },
                          onError: function(error) {
                            if (error) {
                              var errors = error.responseJSON ? error.responseJSON.errors : null;
                              var message = errors ? errors[0] : 'Something went wrong';
                              if(message == "Invitation has expired") {
                                promptError("The submission is closed");
                              } else {
                                promptError(message);
                             }
                            }
                          }
                        });
                      } else {
                       promptLogin(user);
                      }
                    }], true);
                  }},

                  notes: function(notes) {
                    if (notes) {
                      $('#notes').empty();
                      _.forEach(notes, function(note) {
                        $attach('#notes', 'mkNotePanel', [note, {
                          titleLink: 'HREF',
                          withReplyCount: true
                        }], true);
                      });
                    }
                  }
                });

              })
              .fail(function(){
                console.log("Invitation and/or notes not found")
              });
            });
            </script>
         </body>
        </html>
        """ % (header, title, info, url, invitation, invitation, invitation)
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
