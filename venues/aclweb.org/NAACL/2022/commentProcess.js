function(){
    var or3client = lib.or3client;

    var CONFERENCE_ID = 'aclweb.org/NAACL/2022/Conference';
    var SHORT_PHRASE = 'NAACL 2022 Conference';
    var AUTHORS_NAME = '';
    var REVIEWERS_NAME = '';
    var AREA_CHAIRS_NAME = '';
    var SENIOR_AREA_CHAIRS_NAME = '';
    var PROGRAM_CHAIRS_ID = 'aclweb.org/NAACL/2022/Conference/Program_Chairs';
    var USE_AREA_CHAIRS = false;
    var EMAIL_PCs = true;
    var sac_name_dictionary = {
        'Phonology, Morphology and Word Segmentation': 'Phonology_Morphology_Word_Segmentation',
    'Information Extraction': 'Information_Extraction',
    'Computational Social Science and Cultural Analytics': 'CSSCA',
    'Information Retrieval and Text Mining': 'Info_Retrieval_Text_Mining',
    'Interpretability and Analysis of Models for NLP': 'IAM_for_NLP',
    'NLP Applications': 'NLP_Applications',
    'Question Answering': 'Question_Answering',
    'Discourse and Pragmatics': 'Discourse_and_Pragmatics',
    'Summarization': 'Summarization',
    'Language Generation': 'Language_Generation',
    'Sentiment Analysis and Stylistic Analysis': 'SASA',
    'Machine Learning for NLP: Classification and Structured Prediction Models': 'NLP_CSPM',
    'Machine Learning for NLP: Language Modeling and Sequence to Sequence Models': 'NLP_LMSSM',
    'Syntax: Tagging, Chunking, and Parsing': 'Syntax_TCP',
    'Language Resources and Evaluation': 'Language_Resources_Evaluation',
    'Linguistic Theories, Cognitive Modeling and Psycholinguistics': 'LCMP',
    'Dialogue and Interactive systems': 'Dialogue_Interactive_Systems',
    'Multilinguality': 'Multilinguality',
    'Ethics, Bias, and Fairness': 'Ethics_Bias_Fairness',
    'Semantics: Sentence-level Semantics and Textual Inference': 'Semantics_STI',
    'Semantics: Lexical Semantics': 'Semantics_LS',
    'Machine Translation': 'Machine_Translation',
    'Efficient methods in NLP': "Efficient_NLP",
    'Speech': 'Speech',
    'Language Grounding to Vision, Robotics and Beyond': 'LGVRB',
    'Special theme': 'Special_Theme'
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
