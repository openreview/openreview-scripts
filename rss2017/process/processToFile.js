var fs = require('fs');

var mainProcessFile = process.argv[2];
var outputPath = process.argv[3];
var track = process.argv[4];

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


// If there is track information add it as an argument to the function call
if (track) {
   console.log('Track: ', track);
   var before = 'functionTrack(){'
   var replacement = "function(){\n\tconst TRACK_NAME = '"+track+"';"
   while (mainProcess.includes(before)) {
        mainProcess = mainProcess.replace(before, replacement)
        console.log('replaced ', before)
   }
}

// The new file is based on the template file with the track name added
var newFileName = mainProcessFile.replace('.template', track+'.js');
console.log('Save to file', newFileName);
fs.writeFileSync(newFileName, mainProcess);
