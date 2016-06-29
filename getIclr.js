var or3client = require('../../or3/client').mkClient(80,'http://beta.openreview.net');
var _ = require('lodash');

var rootUser = {
  id:'OpenReview.net',
  password:'12345678'
}

or3client.getUserTokenP(rootUser).then(function(token){
	or3client.or3request(or3client.grpUrl+"?id=ICLR.cc",{},'GET',token)
	.then(result=>console.log(result.groups[0].signatures));
});
