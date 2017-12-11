$(function(){

    chrome.storage.sync.get("numLaunches", function(val){

        console.log("got return value :");
        console.log(val);
        $("#numLaunches").val(val["numLaunches"]);
    });


    
    $('#saveNumLaunches').on('click', function(){
        var numLaunches = $('#numLaunches').val();
        chrome.storage.sync.set({"numLaunches" : numLaunches});
    });
})