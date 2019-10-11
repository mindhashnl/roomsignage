$(function () {
	$('*.form :input:not([type=hidden])').change(function () {
		// Show dif if changed
		$('#data-changed-div').slideDown(500);
	});
});

$(function () {
	// If id field is triggered, another card is selected, hide div
	$('*.form :input[type=hidden]').change(function () {
		$('#data-changed-div').slideUp(500);
	});
});
