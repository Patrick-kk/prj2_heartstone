"use strick";
var system = require('system');

if (system.args.length !== 2) {
    console.log("Usage: phantomjs scandir.js DIRECTORY_TO_SCAN");
    phantom.exit(1);
}

var scanDirectory = function (path) {
    var fs = require('fs');
    if (fs.exists(path) && fs.isFile(path)) {
        console.log(path);
    } else if (fs.isDirectory(path)) {
        fs.list(path).forEach(function (e){ 
            if (e !== '.' && e !== '..') { // avoid loops
                scanDirectory(path + '/' + e);
            }
        });
    } else {
        console.log('Wrong path');
        phantom.exit();
    }
};
scanDirectory(system.args[1]);
phantom.exit();