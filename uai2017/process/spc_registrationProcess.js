function () {
  console.log('spc_registrationProcess function run');
  var or3client = lib.or3client;

  var process = function(){
    var or3client = lib.or3client;
    or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token)
    .then(result => done())
    .catch(error => done(error));
    return true;
  };

  var expertises = [
    "Algorithms: Approximate Inference",
    'Algorithms: Belief Propagation',
    'Algorithms: Distributed and Parallel',
    'Algorithms: Exact Inference',
    'Algorithms: Graph Theory',
    'Algorithms: Heuristics',
    'Algorithms: Lifted Inference',
    'Algorithms: MCMC methods',
    'Algorithms: Optimization',
    'Algorithms: Other',
    'Algorithms: Software and Tools',
    'Applications: Biology',
    'Applications: Databases',
    'Applications: Decision Support',
    "Applications: Diagnosis and Reliability",
    'Applications: Economics',
    'Applications: Education',
    'Applications: General',
    'Applications: Medicine',
    'Applications: Planning and Control',
    'Applications: Privacy and Security',
    'Applications: Robotics',
    'Applications: Sensor Data',
    'Applications: Social Network Analysis',
    'Applications: Speech',
    'Applications: Sustainability and Climate',
    'Applications: Text and Web Data',
    'Applications: User Models',
    'Applications: Vision',
    'Data: Big Data',
    'Data: Multivariate',
    'Data: Other',
    'Data: Relational',
    'Data: Spatial',
    'Data: Temporal or Sequential',
    'Learning: Active Learning',
    'Learning: Classification',
    'Learning: Clustering',
    'Learning: Deep Learning',
    'Learning: General',
    'Learning: Nonparametric Bayes',
    'Learning: Online and Anytime Learning',
    'Learning: Other',
    'Learning: Parameter Estimation',
    'Learning: Probabilistic Generative Models',
    'Learning: Ranking',
    'Learning: Recommender Systems',
    'Learning: Regression',
    'Learning: Reinforcement Learning',
    'Learning: Relational Learning',
    'Learning: Relational Models',
    'Learning: Scalability',
    'Learning: Semi-Supervised Learning',
    'Learning: Structure Learning',
    'Learning: Structured Prediction',
    'Learning: Theory',
    'Learning: Unsupervised',
    'Methodology: Bayesian Methods',
    'Methodology: Calibration',
    'Methodology: Elicitation',
    'Methodology: Evaluation',
    'Methodology: Human Expertise and Judgement',
    'Methodology: Other',
    'Methodology: Probabilistic Programming',
    'Models: Bayesian Networks',
    'Models: Directed Graphical Models',
    'Models: Dynamic Bayesian Networks',
    'Models: Markov Decision Processes',
    'Models: Mixed Graphical Models',
    'Models: Other',
    'Models: Relational Models',
    'Models: Topic Models',
    'Models: Undirected Graphical Models',
    'None of the above',
    'Principles: Causality',
    'Principles: Cognitive Models',
    'Principles: Decision Theory',
    'Principles: Game Theory',
    'Principles: Information Theory',
    'Principles: Other',
    'Principles: Probability Theory',
    'Principles: Statistical Theory',
    'Representation: Constraints',
    'Representation: Dempster-Shafer',
    'Representation: Fuzzy Logic',
    'Representation: Influence Diagrams',
    'Representation: Non-Probabilistic Frameworks',
    'Representation: Probabilistic'
  ];

  var spc_expertise = {
    'id': 'auai.org/UAI/2017/-/SPC_Expertise',
    'signatures': ['auai.org/UAI/2017'],
    'writers': ['auai.org/UAI/2017'],
    'invitees': ['auai.org/UAI/2017/Senior_Program_Committee'],
    'noninvitees':[],
    'readers': ['auai.org/UAI/2017','auai.org/UAI/2017/Senior_Program_Committee'],
    'process': process + "",
    'duedate': 1485813353000,
    'reply': {
      'forum': note.id,
      'replyto': note.id,
      'writers': {'values-regex':'~.*'},
      'signatures': {'values-regex':'~.*'},
      'readers': {
        'values': ['auai.org/UAI/2017/Program_Co-Chairs'],
        'description': 'The users who will be allowed to read the above content.'
      },
      'content': {
        'title':{
          'value':'Senior Program Committee Form Response',
          'order':1,
        },
        'primary area': {
          'description': 'Primary area of expertise.',
          'order': 2,
          'value-dropdown': expertises,
          'required': true
        },
        'aditional areas': {
          'description': 'Aditional list of areas of expertise.',
          'order': 3,
          'values-dropdown': expertises
        }
      }
    }
  };


  or3client.or3request(or3client.inviteUrl, spc_expertise, 'POST', token)
  .then(result=>{
    done();
  })
  .catch(error=>done(error));

  return true;
};
