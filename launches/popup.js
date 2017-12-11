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
	numLaunches = obj["numLaunches"];
});
chrome.runtime.onMessage.addListener(function (message, sender ){
	
		if(message[0] === "old_data"){
			displayLaunches(message[1]);
		}else{

			console.log("popup message received -->");
			console.log(message);
			displayLaunches(message);
		}
});

function displayLaunches(data){
	var now = new Date(Date.now());
	var launches = [];
	//console.log(data);
	for(var i=0; i<data.count; i++){

		p = $('<p />');
		p.addClass("launch_cell");
		if(data.launches[i].status == 1 && data.launches[i].tbdtime == 0){
			var windowStart = new Date(data.launches[i].wsstamp*1000);
			var timeLeft =  new Date( windowStart - now );

			var secs = (timeLeft / 1000);
			var minutes = secs / 60;
			var hours = minutes / 60;
			var days = hours / 24;
			
			// console.log( secs + "secs" );
			// console.log( minutes + "minutes" );
			// console.log( hours + "hours" );
			// console.log( days + "days" );
			var htmlString = "<b>"+data.launches[i].name +"</b>";
			htmlString += "<br />in "+(Math.floor(days)) + " d" ;
			htmlString += " "+(Math.floor(hours)% 24) + " h" ;
			htmlString += " "+(Math.floor(minutes)% 60) + " mn" ;

			if( data.launches[i].vidURLs[0] !== undefined){

				htmlString += "<br /><a href='"+ data.launches[i].vidURLs[0] +"' target='_blank'>link</a>" ;
			}
			p.html(htmlString);
			if(( timeLeft / 1000 /60 / 60) < 14){
				$(p).css({
					backgroundColor:'#cc0000'
				});

			}
			launches.push(p);
			//container.append(p);
		}
	}
	
	$('#status').html(launches);



}

$(document).ready(function(){
	updateOptions();
	chrome.runtime.sendMessage("display");
	$('#refreshData').on("click", function(){
		updateOptions();
		$('#status').html("loading data ....");
		chrome.runtime.sendMessage("refresh");
	});


});

