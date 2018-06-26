function (note) {
  var mag_raw = JSON.parse(note.content.MAG);
  var json = {};

  var processANF = function(ANF){
    var sortedAuthors = ANF.sort(function(a, b){
      return a.S - b.S;
    });
    return sortedAuthors.map(entry=>(entry.FN + ' ' + entry.LN));
  }

  var processInvertedIndex = function(InvertedIndex){
    var forwardIndex = {};
    var maxIndex = 0;
    var wordArray = []
    for(var word in InvertedIndex){
      var indexList = InvertedIndex[word];
      for(var i in indexList){
        var index = indexList[i]
        forwardIndex[index] = word.replace(/[\$]/g,'');
        if(index > maxIndex){
          maxIndex = index;
        }
      }
    }
    for(var c=0; c<=maxIndex; c++){
      wordArray.push(forwardIndex[c]);
    }

    return wordArray.join(' ');
  }

  var findValidSource = function(S){
    for(var i in S){
      var source = S[i];
      if(source.hasOwnProperty('Ty') && source.hasOwnProperty('U') && source.Ty == 3 && source.U.endsWith('.pdf')) {
        return source.U;
      }
    }
    return null;
  }

  if(mag_raw.hasOwnProperty('Ti')){
    json.title = mag_raw.Ti.replace(/\./g,'');
  }

  if(mag_raw.hasOwnProperty('AA')){
    json.authors = mag_raw.AA.map(entry=>entry.AuN);
  }

  if(mag_raw.hasOwnProperty('E')){
    var entity = mag_raw.E;
    if(entity.hasOwnProperty('DN')){
      json.title = entity.DN.replace(/\./g,'');
    }

    if(entity.hasOwnProperty('ANF')){
      json.authors = processANF(entity.ANF);
    }

    if(entity.hasOwnProperty('DOI')){
      json.DOI = entity.DOI;
    }

    if(entity.hasOwnProperty('IA')){
      if(entity.IA.hasOwnProperty('InvertedIndex')){
        json.abstract = processInvertedIndex(entity.IA.InvertedIndex);
      }
    }
    if(entity.hasOwnProperty('S')){
      validSource = findValidSource(entity.S);
      if(validSource != null){
        json.pdf = validSource;
      }
    }
  }
  note.content = json;
  return note;
};
