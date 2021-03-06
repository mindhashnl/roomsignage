$(document).ready(function () {
	// On change
	$('input').change(function (event) {
		const selector = $('#screen_display_' + event.target.name.replace('-clear', ''));

		if (event.target.name === 'color') {
			$('#screen_display_info').css('background-color', event.target.jscolor.toHEXString());
		} else if (event.target.files && event.target.files[0]) {
			const reader = new FileReader();

			reader.onload = function (e) {
				selector.attr('src', e.target.result);
			};

			reader.readAsDataURL(event.target.files[0]);
		} else if (event.target.name === 'image-clear') {
			selector.attr('src', '/static/mysign_app/image-fallback.png');
		} else if (event.target.name === 'logo-clear') {
			selector.attr('src', '/static/mysign_app/logo-fallback.png');
		} else if (event.target.name === 'text_color') {
			$('.company-info').css('color', event.target.jscolor.toHEXString());
		} else {
			selector.text(event.target.value);
		}
	});
});
