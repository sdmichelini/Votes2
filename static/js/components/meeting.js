//This file is responsible for controlling the meeting component on a webpage.

$(document).ready(function(){
	getMeetingInfo();
});

var MEETING_URL = '/api/meeting';

function getMeetingInfo(){
	$('#meeting-results').html('Loading Current Meeting Info...');
	$.get(MEETING_URL, function(data){
		if(data == null){
			$('#meeting-results').html('No meeting is currently open.');
		}else{
			$('#meeting-results').html(data);
		}

	}).fail(function(){
		$('#meeting-results').html('Unable to Load Meeting Info...');
	});
}
