$(document).ready(function(){
	$('#do_attendence').click(calcAttendence);
});

function calcAttendence(){
	present = []; excused = []; unexcused = [];
	$('.users').each(function(i){
		email = $(this).html();
		present_selector = '#'+email.replace("@","").replace(".","")+'1';
		excused_selector = '#'+email.replace("@","").replace(".","")+'2';
		unexcused_selector = '#'+email.replace("@","").replace(".","")+'3';
		if($(present_selector).is(':checked')){
			present.push(email);
		}else if($(excused_selector).is(':checked')){
			excused.push(email);
		}else if($(unexcused_selector).is(':checked')){
			unexcused.push(email);
		}else{
			console.log('Could not determine presence for: '+email);
		}
	});

	console.log(present);
	console.log(excused);
	console.log(unexcused);
	$.ajax({
		type:'POST',
		url: '/admin/attendence',
		data: JSON.stringify({present: present, excused: excused, unexcused: unexcused}),
		success: function(msg){
			console.log('Success');
			document.location.href="/admin";
		},
		error: function(){
			alert('Error Submitting Attendence');
		}
	});
}
