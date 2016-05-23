$(document).ready(function(){
	$('#create-user').submit(function(e){
		e.preventDefault();
		name = $('#username').val();
		email2 = $('#email').val();
		grad_year2 = $('#grad-year').val();
		console.log(name);console.log(email2);console.log(grad_year2);
		$.ajax({
			type:'POST',
			url: '/admin/users',
			contentType:'application/json',
			dataType:'json',
			data: JSON.stringify({ email: email2, grad_year: grad_year2, username: name}),
			success: function(msg){
				$('#create-error').hide();
				curHtml = $('#user-data').html();
				$('#user-data').html(curHtml + "<li class='list-group-item'>" + name +
					"<button type='button' class='close' aria-label='Delete User'>" +
						"<span aria-hidden='true'>&times;</span>"+
					"</button></li>");
				$('#username').val('');
				$('#email').val('');
				$('#grad-year').val('');

			},
			error: function(req, status, error){
				console.log(req);
			    console.log('error');
				$('#create-error').show();
				$('#create-error').html('Error Adding User.');

			}
		});
	});
});
