var fs = require('fs');

var mainProcessFile = process.argv[2];
var outputPath = process.argv[3];

console.log('Main process', mainProcessFile);

var mainProcess = fs.readFileSync(mainProcessFile, 'utf8');

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
console.log('Save to file', newFileName);
fs.writeFileSync(newFileName, mainProcess);
