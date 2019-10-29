// This is for the is_admin tooltip on admin/users page
$(function () {
	$('[for="id_is_admin"]').popover({
		trigger: 'hover focus',
		placement: 'right',
		content: 'By enabling this value you allow the user to manage all the companies.'
	});
});
