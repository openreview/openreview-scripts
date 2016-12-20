function () {
  console.log('spc_registrationProcess function run');
  var or3client = lib.or3client;

  var spc_expertise = {
    'id': 'UAI.org/2017/conference/-/SPC_Expertise',
    'signatures': ['UAI.org/2017/conference'],
    'writers': ['UAI.org/2017/conference'],
    'invitees': ['UAI.org/2017/conference/Sr_Program_Committee'],
    'noninvitees':[],
    'readers': ['UAI.org/2017/conference','UAI.org/2017/conference/Sr_Program_Committee'],
    'process': "function(){done();return true;};",
    'duedate': 1485813353000,
    'reply': {
      'forum': note.id,
      'replyto': note.id,
      'writers': {'values-regex':'~.*'},
      'signatures': {'values-regex':'~.*'},
      'readers': {
        'values': ['UAI.org/2017/conference/Program_Chairs'],
        'description': 'The users who will be allowed to read the above content.'
      },
      'content': {
        'title':{
          'value':'Senior Program Committee Form Response',
          'order':1,
        },
        'areas': {
          'description': 'Comma separated list of areas of expertise.',
          'order': 2,
          'values-dropdown': [
              "Algorithms: Approximate Inference",
              'Algorithms: Belief Propagation',
              'Algorithms: Distributed and Parallel',
              'Algorithms: Exact Inference',
              'Algorithms: Graph Theory',
              'Algorithms: Heuristics',
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
          ]
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
