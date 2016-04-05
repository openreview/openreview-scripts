#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');
var stringify = require('csv-stringify');
var _ = require('lodash');
var p = require('node-promise');

var urlPrefix = 'http://localhost:8529/_db/_system/openreview/'; 

var papersP = function() {
  var df = p.defer();
  request(
    {
      method: 'GET',
      url: urlPrefix + 'notes?invitation=ICLR.cc/2016/workshop/-/submission', 
      json: true,
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

var accepted = _.fromPairs(_.map([
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
  "91EvmZNlwtkRlNvXUKL9", "r8lrEqPpYF8wknpYt57j", "ZY9xxQDMMu5Pk8ELfEz4", "P7q1lVQQvSKvjNORtJZL",
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
], function(id) {
  return [id, true];
}));

p.when(papersP, function(papers) {

  var acceptedGooglePapers = _.filter(papers, function(paper) {
    return accepted[paper.id] && paper.content.author_emails.indexOf("@google.com") > -1; 
  });

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

  var tripleList = _.flatten(_.map(acceptedGooglePapers, function(paper) {
    var nameEmailPairs = _.filter(getNameEmailPairs(paper), function(pair) {
      return pair.email.indexOf("@google.com") > -1; 
    });
    return _.map(nameEmailPairs, function(nameEmailPair) {
      return _.assign(nameEmailPair, {title: paper.content.title});
    });
  }));

  stringify(_.map(tripleList, function(trip) {
    return [trip.name, trip.email, trip.title];
  }), function(err, str) {
    console.log(str);
  });

});
