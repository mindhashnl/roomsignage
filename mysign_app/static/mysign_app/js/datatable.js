/* eslint-disable-next-line no-unused-vars */
function createDataTable(dataJson, listFields) {

    let columns = [
        // {   /* created column to show a picture just to make this demo look better */
        //     "orderable": false, "data": "Photo", "name": "Photo", "defaultContent": "",
        //     "visible": true, "className": "text-center", "width": "20px",
        //     "createdCell": function (td, cellData, rowData, row, col) {
        //         console.log(cellData)
        //         var $ctl = $('<i class="fa fa-user fa-fw"></i>');
        //         $(td).append($ctl);
        //     }
        // }
        ];

    Object.values(listFields).forEach(function (key) {
        columns.push({data: key, name: key});
    });

    const table = $('#register').DataTable({
        dom: 'fBtp', // Register plugins see https://datatables.net/reference/option/dom
        pageLength: 10,
        buttons: [
            {
                text: '<i class="fa fa-id-badge fa-fw fa-lg" aria-hidden="true"></i>',
                action: function () {

                    $("#register").toggleClass("cards");
                    $("#card-toggle .fa").toggleClass(["fa-table", "fa-id-badge"]);
                    $("#register thead").toggle();

                    if ($("#register").hasClass("cards")) {
                        // Create an array of labels containing all table headers
                        var labels = [];
                        console.log(labels)
                        $('#register').find('thead th').each(function () {
                            labels.push($(this).text());
                        });

                        // Add data-label attribute to each cell
                        $('#register').find('tbody tr').each(function () {
                            $(this).find('td').each(function (column) {
                                $(this).attr('data-label', labels[column]);
                            });
                        });

                        // set correct hight
                        let max = 0;
                        $('#register tr').each(function () {
                            max = Math.max($(this).height(), max);
                        }).height(max);
                    } else {
                        // Remove data-label attribute from each cell
                        $('#register').find('td').each(function () {
                            $(this).removeAttr('data-label');
                        });

                        $("#register tr").each(function () {
                            $(this).height("auto");
                        });
                    }
                },
                attr: {
                    title: 'Change views',
                    id: 'card-toggle'
                }
            }
        ],
        select: 'single',
        data: dataJson,
        columns: columns,
        fnInitComplete: function () {
            $('#card-toggle').click();
            $('#register thead').hide();

        },
    })

    .on('select', function (e, dt, type, indexes) {
        let rowData = table.rows(indexes).data().toArray();

        //For all labels
        for (const [key, value] of Object.entries(rowData[0])) {

            //if field is bool, set checkbox
            if (value === true ||  value === false){
                fieldName = "#id_" + key;
                $(fieldName).prop('checked', value)
            } else
                //If key is id, set the id field
                if (key === 'id') {
                $(id).val(value)
            }
                //Else, set the field with the #id_FIELDNAME id.
            else {
                fieldName = "#id_" + key;
                $(fieldName).val(value)
            }
        }


    })
}