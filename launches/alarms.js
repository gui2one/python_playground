function showNotification() {	
    
    
          // Now create the notification
          chrome.notifications.create('reminder', {
              type: 'basic',
              iconUrl: 'icon.png',
              title: 'Don\'t forget!',
              message: 'You have things to do. Wake up, dude!'
           }, function(notificationId) {});
        
}

chrome.alarms.onAlarm.addListener(function( alarm ) {
    // console.log("Got an alarm!", alarm);
    // showNotification();
});
// chrome.runtime.onMessage.addListener(function (message, sender ){

//     console.log("message received -->");
//     console.log(sender);
// });



$(document).ready(function(){
    'use strict';
     var alarmName = 'remindme';
     function checkAlarm(callback) {
       chrome.alarms.getAll(function(alarms) {
         var hasAlarm = alarms.some(function(a) {
           return a.name == alarmName;
         });
         var newLabel;
         if (hasAlarm) {
           newLabel = 'Cancel alarm';
         } else {
           newLabel = 'Activate alarm';
         }
         document.getElementById('toggleAlarm').innerText = newLabel;
         if (callback) callback(hasAlarm);
       })
     }
     function createAlarm() {
       chrome.alarms.create(alarmName, {
         delayInMinutes: 0.1, periodInMinutes: 0.1});
     }
     function cancelAlarm() {
       chrome.alarms.clear(alarmName);
     }
     function doToggleAlarm() {
       checkAlarm( function(hasAlarm) {
           console.log("toggle Alarm");
         if (hasAlarm) {
           cancelAlarm();
         } else {
           createAlarm();
         }
         checkAlarm();
       });
     }
    $('#toggleAlarm').on('click', doToggleAlarm);
    // $('#toggleAlarm').on('click', showNotification);
    checkAlarm();
});