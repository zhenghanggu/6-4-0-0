init()

function init()
{
	//setup additional ESFs
	refreshAdditionalESFs();

	//add event listener for ESF select
	$("#primary-esfs").change(refreshAdditionalESFs);
	$("#cancelButton").click(onCancel)
}

function onCancel()
{
	window.location.href="/menu";
}


$("#addCapability").click(addCapability);
function addCapability()
{
	var cap = $("#new_capability").val()
	if(cap == ""){return}

	//add capability
	$("#capabilities").append(
		//make one visual and one hidden (so they cant select the items)
		'<option selected>'+cap+'</option>'
	)
	//empty textbox
	$("#new_capability").val("")
}

function refreshAdditionalESFs()
{
	var selectedESF = $( "#primary-esfs option:selected" ).text();

	$("#additional-esfs").empty();
	$("#primary-esfs > option").each(function() {
		if(this.text != selectedESF)
		{
			$("#additional-esfs").append(
				'<option value='+$(this).val()+'>'+this.text+'</option>'
			)
		}
	});
}