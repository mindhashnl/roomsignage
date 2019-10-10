$(document).ready(function () {
	// On change
	$('input').change(function (event) {
		const selector = $('#screen_display_' + event.target.name);

		if (event.target.name === 'color') {
			$('#screen_display_info').css('background-color', event.target.jscolor.toHEXString());
		} else if (event.target.files && event.target.files[0]) {
			const reader = new FileReader();

			reader.onload = function (e) {
				selector.attr('src', e.target.result);
			};

			reader.readAsDataURL(event.target.files[0]);
		} else if (event.target.name === 'textcolor') {
			textFields = $('.company-info').css('color', event.target.jscolor.toHEXString())
		} else {
			selector.text(event.target.value);
		}
	});
});
