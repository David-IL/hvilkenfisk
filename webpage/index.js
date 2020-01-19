// This is taken from https://blog.kevinchisholm.com/javascript/node-js/making-a-simple-http-server-with-node-js-part-iv/

const fs = require('fs');  // fs - file system
const http = require('http');
const url = require('url');
const path = require('path');

extensions = {
    ".html" : "text/html",
    ".css" : "text/css",
    ".js" : "application/javascript",
    ".png" : "image/png",
    ".gif" : "image/gif",
    ".jpg" : "image/jpeg",
    ".jpeg" : "image/jpeg",
    ".json": "application/json"
};

/*
// Read json data from local file system
const json = fs.readFileSync(`${__dirname}/Arter.json`, 'utf-8');
const artsData = JSON.parse(json);

console.log(artsData['Kveite']);
console.log(__dirname);
*/

var getArtsData = function() {
    const json = fs.readFileSync(`${__dirname}/Arter.json`, 'utf-8');
    const artsData = JSON.parse(json);

    return artsData;
}

// Create web server on ip and port
const server_old = http.createServer((req, res) => {  // request, response
    css(req, res);

    // This is run every time someone accesses this server (e.g. visits a web page)   
    console.log('Someone did access the server')
    //res.end('URL was not found on the server!');
    
    const pathName = url.parse(req.url, true).pathname;
    const id = url.parse(req.url, true).query.id;
    
    // MAIN PAGE
    if (pathName === '/') {
        res.writeHead(200, { 'Content-type': 'text/html'});  // standard status codes 200, 404
        
        fs.readFile(`${__dirname}/index.html`, 'utf-8', (err, data) => {    
            let mainPage = data;            
            res.end(mainPage);
        });
    } 

    // URL NOT FOUND
    else {
        res.writeHead(404, { 'Content-type': 'text/html'});  // standard status codes 200, 404
        res.end('URL was not found on the server!');
    }

    
});

//step 2) create the server
server = http.createServer(requestHandler);


// Set up server to always listen to an IP address and port
//      (port to listen to, IP address)
server.listen(1337, '127.0.0.1', () => {
    console.log('Listening for requests now');
});


// Helper function handles file verification
function getFile(filePath, res, mimeType){
	//does the requested file exist?
	fs.exists(filePath, function(exists){
		//if it does...
		if(exists) {
			//read the file, run the anonymous function
			fs.readFile(filePath, function(err,contents){
				if(!err) {
					//if there was no error
					//send the contents with the default 200/ok header
					res.writeHead(200, {
						"Content-type" : mimeType,
						"Content-Length" : contents.length
					});
					res.end(contents);
				} else {
					//for our own troubleshooting
					console.dir(err);
				};
			});
		} else {
            console.log(`File ${filePath} does not seem to exist or cannot be found`)
			//if the requested file was not found serve-up our 404 page
			res.writeHead(404, { 'Content-type': 'text/html'});  // standard status codes 200, 404
            res.end('URL was not found on the server!');
		};
	});
};

// Helper function to handle HTTP requests
function requestHandler(req, res) {
    //console.log('Someone did access the server');
	var
    fileName = path.basename(req.url) || 'index.html',    
	ext = path.extname(fileName),
	localFolder = __dirname + '/';
 
	//do we support the requested file type?
	if(!extensions[ext]){
		//for now just send a 404 and a short message
		res.writeHead(404, {'Content-Type': 'text/html'});
        res.end("The requested file type is not supported");
    };
    
    // check if extension is image - in that case it should be in 
    // a subfolder that should be included in path
    if ((/\.(jpg|jpeg|png|gif)$/i).test(fileName)) {
        fileName = req.url.split('/');
        fileName = fileName[1] + '/' + fileName[2];
    }
 
	//call our helper function
	//pass in the path to the file we want,
    //the response object
    //console.log(`${req.url} - ${fileName}`);
	getFile((localFolder + fileName), res, extensions[ext]);
};