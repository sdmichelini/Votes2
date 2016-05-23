//This file manages the polls components for a webpage

$(document).ready(function(){
	getPollResults();
});

var POLL_URL = '/api/polls';
/*
	Get's the recent poll results from the remote server.
*/
function getPollResults(){
	$('#poll-results').html('Fetching poll results...');
    $.get(POLL_URL,function(data){
        if(data.length > 0){
            $('#poll-results').html(makePollHtml(data));
        }else{
			$('#poll-results').html('There are no poll results available.');
		}
    }).fail(function(){alert('Unable to load poll results.');
		$('#poll-results').html('We are unable to load poll results.');
	});
}

function genResults(data){
    ret = '';

    for(var i = 0; i < data.length; i++){
        ret +=  makeOldHtml(data[i]);
	}
    return ret;
}

function makePollHtml(data){
	ret = ' <ul class="list-group list-group-flush">';
	for(var i = 0; i < data.length; i++){
		ret += "<li class='list-group-item'>" +"<div class='row'><strong>"+data[i].title+"</strong></div><div class='row'>Y:"+data[i].votes_yes+ " N:"+data[i].votes_no+" A:"+data[i].votes_abstain+"</div></li>"
	}
	ret += '</ul>'
	return ret;
}

function makeOldHtml(data){
	return "<div class='row'>"+data.title+"</div>"+"<div class='row'>"+"Yes: "+data.votes_yes+" No: "+data.votes_no+" Abstain: "+data.votes_abstain+"</div>";
}
