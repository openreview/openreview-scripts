#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');
var stringify = require('csv-stringify');
var _ = require('lodash');
var p = require('node-promise');

var urlPrefix = 'http://localhost:8529/_db/_system/openreview/'; 

var cmtAcceptedPapers = [
  "q7kEZL1W2U8LEkD3tgnV", "q7kEN7WoXU8LEkD3t7BQ", "3QxX9NwWgIp7y9wlt5L7", 
  "wVqq536NJiG0qV7mtBNp", "71BmK0m6qfAE8VvKUQWB", "oVgBRXX9nsrlgPMRsrP4", 
  "oVgo4M4RRIrlgPMRsBz5", "oVgo4p8O1CrlgPMRsBzE", "GvVJNQZM5f1WDOmRiMKy", 
  "BNYMo3QRxh7PwR1riEDL", "oVgoWgzpZSrlgPMRsB19", "91Eo10XnqckRlNvXUVkL", 
  "5QzkZ8LvJFZgXpo7i3OQ", "r8lrkABJ7H8wknpYt5KB", "3Qxgwzv3ZCp7y9wltPg2", 
  "vlpy96kV2C7OYLG5inQw", "BNYAGG8r9F7PwR1riXz8", "6XAl95Pz4IrVp0EvsEpp", 
  "Qn8x8rGr5CkB2l8pUY8P", "q7kqBKMN2U8LEkD3t7Xy", "gZ9Oq3ZGVCAPowrRUANz", 
  "oVgBVKDQmCrlgPMRsrPQ", "Jy9kxYV3ziqp6ARvtWXZ", "L7VOPGYLgCRNGwArs4Bm", 
  "oVgo9jD93urlgPMRsB1B", "GvVr3PmmGC1WDOmRiEo6", "NL6ggGZ5wI0VOPA8ixm2", 
  "0YrNVxKMAUGJ7gK5tR5K", "ZY9xwl3PDS5Pk8ELfEzP", "91EEnoZX0HkRlNvXUKLA", 
  "E8Vg037q7f31v0m2iqn3", "WL9EYwkKyI5zMX2Kf2V2", "4QyyQzGjptBYD9yOF80y", 
  "nx9Av7Am9T7lP3z2ioYK", "ROVAEyEoPHvnM0J1IpPO", "ANYzz8LXgINrwlgXCqGj", 
  "71BmDZPEluAE8VvKUQ80", "ROVmO430RTvnM0J1Ip9z", "k80x272vDcOYKX7jiYKw", 
  "1WvovwjA7UMnPB1oinBL", "mO9mx9y48ij1gPZ3UlOk", "D1VVBv7BKS5jEJ1zfxJg", 
  "1WvkoMpX3FMnPB1oiq8Z", "3QxqXoJEyfp7y9wltP11", "k80kvBj55IOYKX7ji4V4", 
  "vlprXrN35c7OYLG5irDB", "2xwp4Zwr3TpKBZvXtWoj", "WL9AjgWvPf5zMX2Kfoj5", 
  "91EvmZNlwtkRlNvXUKL9", "r8lrEqPpYF8wknpYt57j", "ZY9xxQDMMu5Pk8ELfEz4", "P7q1lVQQvSKvjNORtJZL"
];

var noncAcceptedPapers = [
  "k80kv3zjGtOYKX7ji4V7", "91EowxONgIkRlNvXUVog", "XL9vKJ98DCXB8D1RUGV0", 
  "BNYYGWVA1F7PwR1riED4", "81DnLL9OEI6O2Pl0UV1w", "ZY9xQwqKZh5Pk8ELfEzD", 
  "wVqzjWP0JfG0qV7mtLvp", "OM0jKROjrFp57ZJjtNkv", "ZY9x1mJ3zS5Pk8ELfEjD", 
  "ANYzpXg3LcNrwlgXCq9G", "xnrAg7jmLF1m7RyVi3vG", "ROVmN8wyOSvnM0J1IpNm", 
  "yovBjmpo1ur682gwszM7", "xnrA4qzmPu1m7RyVi38Z", "r8lrDJ89Pf8wknpYt5zq", 
  "ROVmA279BsvnM0J1IpNn", "VAVqG11WmSx0Wk76TAzp", "1WvOZJ0yDTMnPB1oinGN", 
  "k80kn82ywfOYKX7ji42O", "L7VOrG6lVsRNGwArs4qo", "wVqzLo88YsG0qV7mtLq7", 
  "D1VDjyJjXF5jEJ1zfE53", "mO9mQWp8Rij1gPZ3Ul5q", "wVqzL1ypocG0qV7mtLqm", 
  "q7kqBkL33f8LEkD3t7X9", "D1VDZ5kMAu5jEJ1zfEWL", "MwVPvKwRvsqxwkg1t7kY", 
  "E8VEozRYyi31v0m2iDwy", "ZY9xMOwxPf5Pk8ELfEjV", "L7VOOy8B6hRNGwArs4Bn", 
  "Qn8lE8x17fkB2l8pUYPk", "lx9l4r36gU2OVPy8Cv9g", "zvwDjZ3GDfM8kw3ZinXB", 
  "p8jp5lzPWSnQVOGWfpDD", "BNYAGZZj5S7PwR1riXzA", "mO9m42yWgSj1gPZ3UlGA", 
  "2xwPmERVBtpKBZvXtQnD", "XL9v5ZZ2qtXB8D1RUG6V", "OM0jjYW3BHp57ZJjtNEO", 
  "6XAwLR8gysrVp0EvsEW3", "BNYAA7gNBi7PwR1riXzR", "Qn8lxPngJFkB2l8pUYxg", 
  "OM0jvwB8jIp57ZJjtNEZ", "oVgoWpz5LsrlgPMRsB1v", "gZ9OMgQWoIAPowrRUAN6", 
  "OM0vWYM7Eup57ZJjtNql", "XL92M93mzhXB8D1RUWBz", "L7VOzGWB5hRNGwArs4BJ", 
  "lx9lNjDDvU2OVPy8CvGJ", "3QxgvRAolhp7y9wltPg8", "XL9vPjMAjuXB8D1RUG6L", 
  "P7Vk63koAhKvjNORtJzZ", "jZ9WrEWPmsnlBG2XfGLl", "81DD7ZNyxI6O2Pl0Ul5j"
];

var tokenP = function() {
  var df = p.defer();
  request(
    {
      method: 'POST',
      url: urlPrefix + 'login', 
      json: true, 
      body: {
        'id': 'OpenReview.net', 'password': ''
      }
    },
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token; 
        df.resolve(token);
      }
    }
  );
  return df.promise;
}();

p.when(tokenP, function(token) {

  var papersP = function() {
    var df = p.defer();
    request(
      {
        method: 'GET',
        url: urlPrefix + 'notes?invitation=ICLR.cc/2016/workshop/-/submission', 
        json: true,
        headers: {
            'Authorization': 'Bearer ' + token
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          df.resolve(body.notes);
        } else {
          df.resolve([]);
        }
      }
    );
    return df.promise;
  }();

  var sendCmtEmail = function(email, name, title) {
    console.log("sendCmtEmail: " + email + ", " + name + ", " + title);
    var subject = "ICLR 2016 Poster Presentation Instructions";
    var message = ( 
      "Dear " + name + ",\n\n"  
      + "We are writing regarding the presentation of your submission "
      + "*" + title + "*.\n\n"
      + "Here are the instructions regarding the presentation of your poster. The poster boards will be 4 ft. high by 8 ft. wide, so make sure your poster will fit within this area. The Conference Track resubmissions to the Workshop Track will be presented during the poster session of May 3rd. You are encouraged to put up your poster as early as the day's morning coffee break (10:20 to 10:50).\n\n" 
      + "Each poster has been assigned a number, shown here:\n\n"
      + "http://www.iclr.cc/doku.php?id=iclr2016:main#workshop_track_posters_may_3rd\n\n"
      + "So please use the poster board corresponding to the number for your work.\n\n"
      + "Once the poster session is over, you have until the end of the day to take off your poster from your assigned poster board.\n\n"
      + "Thanks for helping make ICLR an exciting event, and we're looking forward to the presentation of your work!\n\n"
      + "Hugo, Samy, and Brian -- the ICLR 2016 program committee"
    );
    request(
      {
        'method': 'POST',
        'url': urlPrefix + 'mail', 
        'json': true,
        'body': {
          'groups' : [email], 
          'subject': subject,
          'message': message 
        },
        'headers': {
          'Authorization': 'Bearer ' + token 
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          console.log("cmt sent : " + JSON.stringify(body));
          console.log("paper: " + title);
          console.log("");
        }
      }
    );
  };

  var sendNoncEmail = function(email, name, title) {
    console.log("sendNoncEmail: " + email + ", " + name + ", " + title);
    var subject = "ICLR 2016 Poster Presentation Instructions";
    var message = ( 
      "Dear " + name + ",\n\n"  
      + "We are writing regarding the presentation of your submission "
      + "*" + title + "*.\n\n"
      + "Here are the instructions regarding the presentation of your poster. The poster boards will be 4 ft. high by 8 ft. wide, so make sure your poster will fit within this area. Extended abstracts accepted to the Workshop Track are presented during the poster session of May 2nd. You are encouraged to put up your poster as early as the day's morning coffee break (10:20 to 10:50).\n\n"
      + "Each poster has been assigned a number, shown here:\n\n"
      + "http://www.iclr.cc/doku.php?id=iclr2016:main#workshop_track_posters_may_2nd\n\n"
      + "So please use the poster board corresponding to the number for your work.\n\n"
      + "Once the poster session is over, you have until the end of the day to take off your poster from your assigned poster board.\n\n"
      + "Thanks for helping make ICLR an exciting event, and we're looking forward to the presentation of your work!\n\n"
      + "Hugo, Samy, and Brian -- the ICLR 2016 program committee"
    );
    request(
      {
        'method': 'POST',
        'url': urlPrefix + 'mail', 
        'json': true,
        'body': {
          'groups' : [email], 
          'subject': subject,
          'message': message 
        },
        'headers': {
          'Authorization': 'Bearer ' + token 
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          console.log("nonc sent : " + JSON.stringify(body));
          console.log("paper: " + title);
          console.log("");
        }
      }
    );
  };

  p.when(papersP, function(papers) {

    var id2paperMap = _.fromPairs(_.map(papers, function(p) {
      return [p.id, p];
    }));



    var getNameEmailPairs = function(paper) {
      var authorList = _.map(paper.content.authors.split(","), function(s) {
        return s.trim();
      });
      var authorEmailList = _.map(paper.content.author_emails.split(","), function(s) {
        return s.trim();
      });
      var nameEmailPairs = function() {
        if (authorEmailList.length > 0) {
          return _.map(_.zip(authorList, authorEmailList), function(p) {
            return {name: p[0], email: p[1]};
          });
        } else {
          console.log("No Emails: " + paper.id);
          return [[]];
        }
      }();
      return nameEmailPairs;
    };



    _.forEach(cmtAcceptedPapers, function(pid) {
      var paper = id2paperMap[pid];
      var title = paper.content.title;
      var nameEmailPairs = getNameEmailPairs(paper);
      _.forEach(nameEmailPairs, function(p) { if (p.email && p.name) {
        sendCmtEmail(p.email, p.name, title);
      }});

    });

    _.forEach(noncAcceptedPapers, function(pid) {
      var paper = id2paperMap[pid];
      var title = paper.content.title;
      var nameEmailPairs = getNameEmailPairs(paper);
      _.forEach(nameEmailPairs, function(p) { if (p.email && p.name) {
        sendNoncEmail(p.email, p.name, title);
      }});

    });


  });


});
