var globalData = null;
var numLaunches = null;
var options = {
	"numLaunches" : null
}

function updateOptions(){

	for(var key in options){

		chrome.storage.sync.get(key, function(obj){
			if( obj[key] != options[key]){
				console.log("update in progress, values are different");
				options[key] = obj[key];
			}
		});
	}
}
chrome.storage.sync.get("numLaunches", function(obj){
	if(obj["numLaunches"] == undefined){
		options["numLaunches"] = 5;
	}else{

		options["numLaunches"] = obj["numLaunches"];
	}
});
chrome.runtime.onMessage.addListener(function (message, sender ){
    
        console.log("message received -->");
        console.log(message);
        
        if(message == "refresh"){
			loadLaunchesData();
			updateOptions();
            
        }else if( message == "display"){
            if( globalData == null){
                loadLaunchesData();
            }else{

                chrome.runtime.sendMessage([ "old_data", globalData]);
                console.log("display old data");
            }
        }
        else{

            chrome.runtime.sendMessage("other actions ?");
        }


});


// chrome.alarms.onAlarm.addListener(function( alarm ) {
//     console.log("Got an alarm!", alarm);
//     showNotification();
// });

function sendData(data){

    chrome.runtime.sendMessage(data);
}

function loadLaunchesData(){
    console.log("loadLaunchesData function FIRED");

	$.ajax
	(
		{
			type : 'GET',
			url: "https://launchlibrary.net/1.2/launch/next/"+options["numLaunches"].toString(),
			data :{},
			beforeSend: function(){
				    //Download progress
					//container.html("Loading Data ...");

			},
			success: function(data){

                console.log(data);
                globalData = data;
				sendData(data);
				checkSoon(data);
				// for(var i=0; i<data.count; i++){

				// 	p = $('<p />');
				// 	if(data.launches[i].status == 1){
				// 		var windowStart = new Date(data.launches[i].wsstamp*1000);
				// 		var timeLeft =  new Date( windowStart - now );

				// 		var secs = (timeLeft / 1000);
				// 		var minutes = secs / 60;
				// 		var hours = minutes / 60;
				// 		var days = hours / 24;
						
				// 		// console.log( secs + "secs" );
				// 		// console.log( minutes + "minutes" );
				// 		// console.log( hours + "hours" );
				// 		// console.log( days + "days" );
				// 		var htmlString = "launch -->"+ data.launches[i].name;
				// 		htmlString += "<br /> in "+(Math.floor(days)) + " d" ;
				// 		htmlString += " "+(Math.floor(hours)% 24) + " h" ;
				// 		htmlString += " "+(Math.floor(minutes)% 60) + " mn" ;

				// 		if( data.launches[i].vidURLs[0] !== undefined){

				// 			htmlString += "<br /><a href='"+ data.launches[i].vidURLs[0] +"' target='_blank'>link</a>" ;
				// 		}
				// 		p.html(htmlString);
				// 		launches.push(p);
				// 		//container.append(p);
				// 	}
				// }
                
               
				
			}
		}
	)    
    
    //console.log(launches);
    //return launches;
}


function checkSoon(data)
{
	var now = new Date(Date.now());
	var launches = [];
	console.log("checkSoon()");
	for(var i=0; i< data.count; i++){
		//console.log(data.launches[i]);

		if(data.launches[i].status == 1 && data.launches[i].tbdtime == 0)
		{
			var windowStart = new Date(data.launches[i].wsstamp*1000);
			var timeLeft =  new Date( windowStart - now );

			var secs = (timeLeft / 1000);
			var minutes = secs / 60;
			var hours = minutes / 60;
			var days = hours / 24;

			if(( timeLeft / 1000 / 60 / 60 ) < 17){

				showNotification(timeLeft / 1000 / 60 / 60);
			}
			
			// console.log( secs + "secs" );
			// console.log( minutes + "minutes" );
			// console.log( hours + "hours" );
			// console.log( days + "days" );

			// var htmlString = "launch -->"+ data.launches[i].name;
			// htmlString += "<br /> in "+(Math.floor(days)) + " d" ;
			// htmlString += " "+(Math.floor(hours)% 24) + " h" ;
			// htmlString += " "+(Math.floor(minutes)% 60) + " mn" ;

			// if( data.launches[i].vidURLs[0] !== undefined)
			// {
			// 	htmlString += "<br /><a href='"+ data.launches[i].vidURLs[0] +"' target='_blank'>link</a>" ;
			// }
			// p.html(htmlString);
			// launches.push(p);

				
		}		

	}
}
function showNotification(message) {	
    
		if( message === undefined){
			message = "Rocket Launches Alert";
		}
          // Now create the notification
          chrome.notifications.create('reminder', {
              type: 'basic',
              iconUrl: 'icon.png',
              title: 'Don\'t forget!',
              message: message.toString()
           }, function(notificationId) {});
        
}


$(document).ready(function(){

    var timer = 0.0;

    var launches = [];
    function loop(){
        launches = loadLaunchesData();
        
        setTimeout(loop, 10000);

    }
   // loop();
    
    //console.log("hello !!!!!!!!!!!!!!!!!!!!!!!!!!");

});

