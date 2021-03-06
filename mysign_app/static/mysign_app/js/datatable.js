/* eslint-disable-next-line no-unused-vars */
function createDataTable(dataJson, listFields) {
	const columns = [];

	Object.values(listFields).forEach(function (key) {
		columns.push({
			data: key,
			defaultContent: 'Not Set',
			createdCell: function (cell, cellData, rowData) {
				if (cellData === 'Not Set') {
					cell.setAttribute('hidden', true);
				}

				cell.classList.add(key);

				if (rowData.company) {
					cell.classList.add('active');
				}
			}
		});
	});

	// Register custom classes
	$.extend($.fn.dataTableExt.oStdClasses, {
		sFilterInput: 'form-control w-100'
	});

	const table = $('#register').DataTable({
		dom:
			'rt<"row"<"col-3 offset-9"f>>' + // Search bar row
			'<"row row-table"<"col-12 h-100" tr>>' + // Data row
			'<"row"<"col-5"i><"col-7"p>>', // Page buttons
		pageLength: 20,
		language: {
			search: '',
			searchPlaceholder: 'Search'
		},
		select: 'single',
		data: dataJson,
		columns: columns,
		fnInitComplete: function () {
			$('#form-fieldset').attr('disabled', true);
		},
		drawCallback: function () {
			// Change table to card view
			let labels = [];
			$('#register').find('thead th').each(function () {
				labels.push($(this).text());
			});

			let max = 185;
			$('#register tr').each(function () {
				max = Math.max($(this).height(), max);
			}).height(max);

			// Add data-label attribute to each cell
			$('#register').find('tbody tr').each(function () {
				$(this).find('td').each(function (column) {
					$(this).attr('data-label', labels[column]);
				});
			});
		}
	})

		.on('select', function (e, dt, type, indexes) {
			let rowData = table.rows(indexes).data().toArray();

			// For all labels
			for (const [key, value] of Object.entries(rowData[0])) {
				if (value === null) {
					// Do nothing if field is not set
				} else if (value === true || value === false) {
					// If field is bool, set checkbox
					let fieldName = '#id_' + key;
					$(fieldName).prop('checked', value);
				} else if (key === 'id') {
					// If key is id, set the id field
					$('#id').val(value);
				} else {
					// Else, set the field with the #id_FIELDNAME id.
					let fieldName = '#id_' + key;
					if (typeof value === 'object') {
						$(fieldName).val(value.id);
					} else {
						$(fieldName).val(value);
					}
				}

				$('#id').change();
			}

			$('#form-fieldset').attr('disabled', false);
		})
		.on('deselect', function () {
			// Disable fields and buttons
			$('#form-fieldset').attr('disabled', true);

			// Reset all input fields
			$('input[name!=csrfmiddlewaretoken]').val(null); // Input fields
			$('input').prop('checked', false); // Checkboxes
			$('select').val(null); // Dropdowns
		});

	// Clicking on the tr doesn't work. This makes the tr click also click on the td
	$('#register').on('click', 'tr', function (event) {
		if (event.target.cells) {
			event.target.cells[0].click(0);
		}
	});
}
