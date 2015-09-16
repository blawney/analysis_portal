
$( document ).ajaxStart(function() {
	console.log( "Triggered ajaxStart handler." );
	$("#loading").fadeIn("fast");
});

$( document ).ajaxStop(function() {
	console.log( "Stopped via ajaxStop." );
	$("#loading").fadeOut("fast");
});

function do_toggle(e){
	$("#wrapper").toggleClass("toggled");
	$("#menu-toggle").toggleClass("vis-toggle");
}

function toggle_input(id){
	// hide all of them
	$("#splash_div").css("display", "none");
	$(".selection_div").css("display", "none");
	$("#results_div").css("display", "none");

	// unhide the selected query type
	$(id).css("display", "block");
}



function retrieve_samples(){
	$.ajax({
		url: "get_samples/",
		type: "POST", 
		data: {project_id: $('#id_project_selector').val()},
		dataType:'html',
		// handle a successful response
		success : function(html) {
		    $("#id_sample_table").html(html);
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
		    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
		});
}


$("#id_project_selector").change(function(){
	console.log('changed!');
	//retrieve_samples();
});


