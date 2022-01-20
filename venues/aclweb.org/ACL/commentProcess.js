function(){
    var or3client = lib.or3client;

    var CONFERENCE_ID = 'aclweb.org/ACL/2022/Conference';
    var SHORT_PHRASE = 'ACL 2022 Conference';
    var AUTHORS_NAME = '';
    var REVIEWERS_NAME = '';
    var AREA_CHAIRS_NAME = '';
    var SENIOR_AREA_CHAIRS_NAME = '';
    var PROGRAM_CHAIRS_ID = '';
    var USE_AREA_CHAIRS = false;
    var EMAIL_PCs = false;
    var sac_name_dictionary = {
        'Ethics in NLP': 'Ethics_NLP',
        'Linguistic theories, Cognitive Modeling and Psycholinguistics': 'LCMP',
        'Linguistic Theories, Cognitive Modeling and Psycholinguistics': 'LCMP',
        'Machine Learning for NLP': 'Machine_Learning_NLP',
        'Phonology, Morphology and Word Segmentation': 'Phonology_Morphology_Word_Segmentation',
        'Resources and Evaluation': 'Resources_Evaluation',
        'Semantics: Lexical': 'Semantics_Lexical',
        'Semantics: Sentence level, Textual Inference and Other areas': 'Semantics_STO',
        'Syntax: Tagging, Chunking and Parsing': 'Syntax_TCP',
        'Information Extraction': 'Information_Extraction',
        'Computational Social Science and Cultural Analytics': 'CSSCA',
        'Information Retrieval and Text Mining': 'Info_Retrieval_Text_Mining',
        'Interpretability and Analysis of Models for NLP': 'IAM_for_NLP',
        'Machine Translation and Multilinguality': 'Machine_Translation_Multilinguality',
        'NLP Applications': 'NLP_Applications',
        'Question Answering': 'Question_Answering',
        'Dialogue and Interactive Systems': 'Dialogue_and_Interactive_Systems',
        'Discourse and Pragmatics': 'Discourse_and_Pragmatics',
        'Generation': 'Generation',
        'Language Grounding to Vision, Robotics, and Beyond': 'LGVRB',
        'Sentiment Analysis, Stylistic Analysis, and Argument Mining': 'SASAAM',
        'Speech and Multimodality': 'Speech_and_Multimodality',
        'Summarization': 'Summarization',
        'Special Theme on Language Diversity: From Low Resource to Endangered Languages': 'Special_Theme',
        'Conflicts': 'Conflicts'
        };
    or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
    .then(function(result) {

      var forumNote = result.notes[0];
      //var AUTHORS_ID = CONFERENCE_ID + '/Paper' + forumNote.number + '/' + AUTHORS_NAME;
      //TODO: use the variable instead, when we have anonymous groups integrated
      var REVIEWERS_ID = CONFERENCE_ID + '/Paper' + forumNote.number + '/Reviewers';
      var AREA_CHAIRS_ID = CONFERENCE_ID + '/Paper' + forumNote.number + '/Area_Chairs';
      var SENIOR_AREA_CHAIRS_ID = CONFERENCE_ID + '/' + sac_name_dictionary[forumNote.content['track']] + '/Senior_Area_Chairs';
      var ignoreGroups = note.nonreaders || [];
      var signature = note.signatures[0].split('/').slice(-1)[0];
      var prettySignature = signature.startsWith('~') ? signature.replace(/~|\d+/g, '').replace(/_/g, ' ') : signature.replace(/_/g, ' ')
      prettySignature = prettySignature == 'Authors' ? 'An author' : prettySignature;
      ignoreGroups.push(note.tauthor);
      var content = `

Paper Number: ${forumNote.number}

Paper Title: "${forumNote.content.title}"

Comment title: ${note.content.title}

Comment: ${note.content.comment}

To view the comment, click here: ${baseUrl}/forum?id=${note.forum}&noteId=${note.id}`
var promises = [];
    var SAC_mail = {
        groups: [SENIOR_AREA_CHAIRS_ID],
        ignoreGroups: ignoreGroups,
        subject: `[${SHORT_PHRASE}] ${prettySignature} commented on a paper in your area. Paper Number: ${forumNote.number}, Paper Title: "${forumNote.content.title}"`,
        message: `${prettySignature} commented on a paper for which you are serving as Senior Area Chair.${content}`
    };
    promises.push(or3client.or3request( or3client.mailUrl, SAC_mail, 'POST', token ));
      
    var pc_mail = {
        groups: [PROGRAM_CHAIRS_ID],
        ignoreGroups: ignoreGroups,
        subject: `[${SHORT_PHRASE}] ${prettySignature} commented on a paper. Paper Number: ${forumNote.number}, Paper Title: "${forumNote.content.title}"`,
        message: `${prettySignature} commented on a paper for which you are serving as Program Chair.${content}`
    };

    promises.push(or3client.or3request(or3client.mailUrl, pc_mail, 'POST', token));
      

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
};
