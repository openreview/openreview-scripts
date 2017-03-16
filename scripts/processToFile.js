var fs = require('fs');

var mainProcessFile = process.argv[2];
var outputPath = process.argv[3];
const PARAM_START_INDEX = 4;

console.log('Main process', mainProcessFile);

var mainProcess = fs.readFileSync(mainProcessFile, 'utf8');

// Look for << filename.js>> and replace that string with the code in the file
var regex = new RegExp('<<(.+\.js)>>', 'g');
var matches = mainProcess.match(regex);
console.log('matches', matches);
if(matches) {
	matches.forEach(function(m) {

		var fileName = m.replace('<<', '').replace('>>', '');
		var fileContent = fs.readFileSync(outputPath + '/' + fileName, 'utf8');
		mainProcess = mainProcess.replace(m, fileContent);
		console.log('Processing file', fileName);

	})
}

var newFileName = mainProcessFile.replace('.template', '.js');

// Look for <<param>>, see if there is a index attached
// and replace that string with the corresponding argument.
//   <<param>> will be replaced w/ process.argv[PARAM_START_INDEX]
//   <<param2>> will be replaced w/ process.argv[PARAM_START_INDEX+2]
regex = new RegExp('<<(param.*)>>', 'g');
matches = mainProcess.match(regex);
if(matches) {
    var param_max = process.argv.length - PARAM_START_INDEX;
    matches.forEach(function(m) {
        var i = Number(m.replace('<<param', '').replace('>>', ''));
        // check if index is a number and has a corresponding argument
        if (i != NaN  && i >= 0 && i < param_max) {
            mainProcess = mainProcess.replace(m, '\''+process.argv[PARAM_START_INDEX + i]+'\'');
            console.log('Replaced', m, 'with', process.argv[PARAM_START_INDEX + i]);
        }
        else {
            console.log('ERROR: invalid param string:', m);
        }
    })
    // Add the first of the parameters to the file name.
    newFileName = newFileName.replace('.js', process.argv[PARAM_START_INDEX]+'.js');
}

console.log('Save to file', newFileName);
fs.writeFileSync(newFileName, mainProcess);
