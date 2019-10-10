$(function () {
	$('*.form :input:not([type=hidden])').change(function () {
		// Show dif if changed
		$('#collapseDiv').show();
	});
});

$(function () {
	// If id field is triggered, another card is selected, hide div
	$('*.form :input[type=hidden]').change(function () {
		$('#collapseDiv').hide();
	});
});
