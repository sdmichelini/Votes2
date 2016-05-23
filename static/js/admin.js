$(document).ready(function(){
    //Load in our current state
    getMeetingState();
    loadOpenPolls();

	//We have clicked create poll
 	$('#create-meeting').click(function(){
        //Try to create the meeting
        $.ajax({
            type:'POST',
            url:'/admin/meetings',
            success:function(msg){
                window.location = document.location + '/attendence';
            },
            error:function(){
                alert('Error Opening Meeting.');
            }
        });
    });
    $('#close-meeting').click(function(){
        //Try to create the meeting
        $.ajax({
            type:'DELETE',
            url:'/admin/meetings',
            success:function(msg){
                location.reload();
                getPollResults();
            },
            error:function(){
                alert('Error Closing Meeting.');
            }
        });
    });
    $('#close-poll').click(function(){
        if($('#open-description').html().indexOf("There are no open votes to view")== -1){
            $.ajax({
                type:"DELETE",
                url:'/admin/poll',
                success: onDeleteSuccess,
                error: onDeleteError
            });
            /*$.get('/worker/process_vote',function(data){

                getPollResults();
            }).fail(function(){alert('Houston. We have a problem.');});*/

        }
    });
    $('#create-poll').submit(function(e){
        e.preventDefault();
        if(($('#poll-title').length > 0)&&($('#poll-description').length > 0)){
            poll_title = $('#poll-title').val();
            $('#poll-title').val('');
            poll_description = $('#poll-description').val();
            $('#poll-description').val('');
            $.ajax({
                type:"POST",
                url:'/admin/poll',
                contentType:'application/json',
                dataType:'json',
                data: JSON.stringify({title:poll_title , description:poll_description}),
                success: onCreateSuccess,
                error: onCreateError
            });
        }else{
            console.log("Can't Submit Form.")
        }
    });

});

/*
Retrieve the current state of meetings.
*/
function getMeetingState(){
    $.get('/admin/meetings',function(data){
        if(data && data.meeting_open){
            $('#js-meeting-open').show();
            $('#js-meeting-closed').hide();
        }else{
            $('#js-meeting-open').hide();
            $('#js-meeting-closed').show();
        }
    }).fail(function(){alert('Error Fetching Meetings')});
}
//Success Creation of a Poll
function onCreateSuccess(msg){
    console.log('Created Poll.');
    $('#open-title').html(msg.title);
    $('#open-description').html(msg.description);
    $('#close-poll').show();
}

//Failed Creation of a Poll
function onCreateError(req, status, error){
    console.log('error');
}

function loadOpenPolls(){
    $('#close-poll').hide();
    $.ajax({
        url:'/api/poll',
        success: onLoadSucess,
        error: onLoadError
    });
}

function onLoadSucess(msg){
    //ret = JSON.parse(msg);
    if(msg.length > 0){
        $('#open-title').html(msg[0].title);
        $('#open-description').html(msg[0].description);
        $('#close-poll').show();
    }else{
        $('#open-title').html(" ");
        $('#open-description').html("There are no open votes to view.");
        $('#close-poll').hide();
    }
}

function onLoadError(req, status, error){
    console.log('error');
}

function onDeleteSuccess(msg){
    $('#open-title').html(" ");
    $('#open-description').html("There are no open votes to view.");

}

function onDeleteError(){
    console.log("Delete Error");
}
