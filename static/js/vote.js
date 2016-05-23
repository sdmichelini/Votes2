$(document).ready(function(){

	$('#btn-yes').click(function(){
		vote('Y');
	});
	$('#btn-no').click(function(){
		vote('N');
	});
	$('#btn-abstain').click(function(){
		vote('A');
	});
});

function vote(type){
	$.ajax({type:'PUT',
	url: '/api/poll',
	contentType:'application/json',
	dataType:'json',
	data: JSON.stringify({ vote:type }),
	success:function(msg){
		$('#cur-vote').html('Current Vote: '+type);
	},
	error: function(){
		alert('Error');
	}
	});
}
