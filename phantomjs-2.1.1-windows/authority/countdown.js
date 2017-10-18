"use strict";
var t = 10,
    interval = setInterval(function(){
        if (t > 0){
            console.log(t--);
        } else {
            console.log("BALST OFF!");
            phantom.exit();
        }
    }, 1000);
