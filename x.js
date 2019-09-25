<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Datatables card example</title>
<style>
        .cards tbody tr {
            float: left;
            width: 20rem;
            margin: 0.5rem;
            border: 0.0625rem solid rgba(0,0,0,.125);
    	    border-radius: .25rem;
            box-shadow: 0.25rem 0.25rem 0.5rem rgba(0,0,0,0.25);
        }
        .cards tbody td {
            display: block;
        }
        
        .cards td:before {
            content: attr(data-label);
        	display: inline;
        	position: relative;
        	font-size: 85%;
        	top: -0.5rem;
        	float: left;
        	color: #808080;
        	min-width: 4rem;
        	margin-left: 0;
        	margin-right: 1rem;
        	text-align: left;
        }
        tr.selected td:before {
            color: #404040;
        }

        .table .fa {
            font-size: 2.5rem;
            text-align: center;
        }
        .cards .fa {
            font-size: 7.5rem;
        }
        
        
    </style>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/animate.css@3.5.2/animate.min.css">

<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous" type="492e21ba4dbe2f246c90df61-text/javascript"></script>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous" type="492e21ba4dbe2f246c90df61-text/javascript"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/js/bootstrap.min.js" integrity="sha384-a5N7Y/aK3qNeh15eJKGWxsqtnX/wWdSZSKp+81YjTmS15nvnvxKHuzaWwXHDli+4" crossorigin="anonymous" type="492e21ba4dbe2f246c90df61-text/javascript"></script>

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/bs4/dt-1.10.16/b-1.5.1/sc-1.4.3/sl-1.2.4/datatables.min.css" />
<script type="492e21ba4dbe2f246c90df61-text/javascript" src="https://cdn.datatables.net/v/bs4/dt-1.10.16/b-1.5.1/sc-1.4.3/sl-1.2.4/datatables.min.js"></script>

<script type="492e21ba4dbe2f246c90df61-text/javascript">
        var colors = ["Crimson ", "Cyan ", "DarkBlue ", "DarkCyan ", "DarkGoldenRod ", "DarkGray ", "DarkGrey ", "DarkGreen ", "DarkKhaki ", "DarkMagenta ", "DarkOliveGreen ", "DarkOrange "];
        var sampleData = [{ "name": "Tiger Nixon", "position": "This is an abnormally long description for the position of System Architect so that I can demonstrate the effect of changing the height of the tr element using jQuery", "salary": "$320,800", "start_date": "2011/04/25", "office": "Edinburgh", "extn": "5421" }, { "name": "Garrett Winters", "position": "Accountant", "salary": "$170,750", "start_date": "2011/07/25", "office": "Tokyo", "extn": "8422" }, { "name": "Ashton Cox", "position": "Junior Technical Author", "salary": "$86,000", "start_date": "2009/01/12", "office": "San Francisco", "extn": "1562" }, { "name": "Cedric Kelly", "position": "Senior Javascript Developer", "salary": "$433,060", "start_date": "2012/03/29", "office": "Edinburgh", "extn": "6224" }, { "name": "Airi Satou", "position": "Accountant", "salary": "$162,700", "start_date": "2008/11/28", "office": "Tokyo", "extn": "5407" }, { "name": "Brielle Williamson", "position": "Integration Specialist", "salary": "$372,000", "start_date": "2012/12/02", "office": "New York", "extn": "4804" }, { "name": "Herrod Chandler", "position": "Sales Assistant", "salary": "$137,500", "start_date": "2012/08/06", "office": "San Francisco", "extn": "9608" }, { "name": "Rhona Davidson", "position": "Integration Specialist", "salary": "$327,900", "start_date": "2010/10/14", "office": "Tokyo", "extn": "6200" }, { "name": "Colleen Hurst", "position": "Javascript Developer", "salary": "$205,500", "start_date": "2009/09/15", "office": "San Francisco", "extn": "2360" }, { "name": "Sonya Frost", "position": "Software Engineer", "salary": "$103,600", "start_date": "2008/12/13", "office": "Edinburgh", "extn": "1667" }, { "name": "Jena Gaines", "position": "Office Manager", "salary": "$90,560", "start_date": "2008/12/19", "office": "London", "extn": "3814" }, { "name": "Quinn Flynn", "position": "Support Lead", "salary": "$342,000", "start_date": "2013/03/03", "office": "Edinburgh", "extn": "9497" }, { "name": "Charde Marshall", "position": "Regional Director", "salary": "$470,600", "start_date": "2008/10/16", "office": "San Francisco", "extn": "6741" }, { "name": "Haley Kennedy", "position": "Senior Marketing Designer", "salary": "$313,500", "start_date": "2012/12/18", "office": "London", "extn": "3597" }, { "name": "Tatyana Fitzpatrick", "position": "Regional Director", "salary": "$385,750", "start_date": "2010/03/17", "office": "London", "extn": "1965" }, { "name": "Michael Silva", "position": "Marketing Designer", "salary": "$198,500", "start_date": "2012/11/27", "office": "London", "extn": "1581" }, { "name": "Paul Byrd", "position": "Chief Financial Officer (CFO)", "salary": "$725,000", "start_date": "2010/06/09", "office": "New York", "extn": "3059" }, { "name": "Gloria Little", "position": "Systems Administrator", "salary": "$237,500", "start_date": "2009/04/10", "office": "New York", "extn": "1721" }, { "name": "Bradley Greer", "position": "Software Engineer", "salary": "$132,000", "start_date": "2012/10/13", "office": "London", "extn": "2558" }, { "name": "Dai Rios", "position": "Personnel Lead", "salary": "$217,500", "start_date": "2012/09/26", "office": "Edinburgh", "extn": "2290" }, { "name": "Jenette Caldwell", "position": "Development Lead", "salary": "$345,000", "start_date": "2011/09/03", "office": "New York", "extn": "1937" }, { "name": "Yuri Berry", "position": "Chief Marketing Officer (CMO)", "salary": "$675,000", "start_date": "2009/06/25", "office": "New York", "extn": "6154" }, { "name": "Caesar Vance", "position": "Pre-Sales Support", "salary": "$106,450", "start_date": "2011/12/12", "office": "New York", "extn": "8330" }, { "name": "Doris Wilder", "position": "Sales Assistant", "salary": "$85,600", "start_date": "2010/09/20", "office": "Sidney", "extn": "3023" }, { "name": "Angelica Ramos", "position": "Chief Executive Officer (CEO)", "salary": "$1,200,000", "start_date": "2009/10/09", "office": "London", "extn": "5797" }, { "name": "Gavin Joyce", "position": "Developer", "salary": "$92,575", "start_date": "2010/12/22", "office": "Edinburgh", "extn": "8822" }, { "name": "Jennifer Chang", "position": "Regional Director", "salary": "$357,650", "start_date": "2010/11/14", "office": "Singapore", "extn": "9239" }, { "name": "Brenden Wagner", "position": "Software Engineer", "salary": "$206,850", "start_date": "2011/06/07", "office": "San Francisco", "extn": "1314" }, { "name": "Fiona Green", "position": "Chief Operating Officer (COO)", "salary": "$850,000", "start_date": "2010/03/11", "office": "San Francisco", "extn": "2947" }, { "name": "Shou Itou", "position": "Regional Marketing", "salary": "$163,000", "start_date": "2011/08/14", "office": "Tokyo", "extn": "8899" }, { "name": "Michelle House", "position": "Integration Specialist", "salary": "$95,400", "start_date": "2011/06/02", "office": "Sidney", "extn": "2769" }, { "name": "Suki Burks", "position": "Developer", "salary": "$114,500", "start_date": "2009/10/22", "office": "London", "extn": "6832" }, { "name": "Prescott Bartlett", "position": "Technical Author", "salary": "$145,000", "start_date": "2011/05/07", "office": "London", "extn": "3606" }, { "name": "Gavin Cortez", "position": "Team Leader", "salary": "$235,500", "start_date": "2008/10/26", "office": "San Francisco", "extn": "2860" }, { "name": "Martena Mccray", "position": "Post-Sales support", "salary": "$324,050", "start_date": "2011/03/09", "office": "Edinburgh", "extn": "8240" }, { "name": "Unity Butler", "position": "Marketing Designer", "salary": "$85,675", "start_date": "2009/12/09", "office": "San Francisco", "extn": "5384" }, { "name": "Howard Hatfield", "position": "Office Manager", "salary": "$164,500", "start_date": "2008/12/16", "office": "San Francisco", "extn": "7031" }, { "name": "Hope Fuentes", "position": "Secretary", "salary": "$109,850", "start_date": "2010/02/12", "office": "San Francisco", "extn": "6318" }, { "name": "Vivian Harrell", "position": "Financial Controller", "salary": "$452,500", "start_date": "2009/02/14", "office": "San Francisco", "extn": "9422" }, { "name": "Timothy Mooney", "position": "Office Manager", "salary": "$136,200", "start_date": "2008/12/11", "office": "London", "extn": "7580" }, { "name": "Jackson Bradshaw", "position": "Director", "salary": "$645,750", "start_date": "2008/09/26", "office": "New York", "extn": "1042" }, { "name": "Olivia Liang", "position": "Support Engineer", "salary": "$234,500", "start_date": "2011/02/03", "office": "Singapore", "extn": "2120" }, { "name": "Bruno Nash", "position": "Software Engineer", "salary": "$163,500", "start_date": "2011/05/03", "office": "London", "extn": "6222" }, { "name": "Sakura Yamamoto", "position": "Support Engineer", "salary": "$139,575", "start_date": "2009/08/19", "office": "Tokyo", "extn": "9383" }, { "name": "Thor Walton", "position": "Developer", "salary": "$98,540", "start_date": "2013/08/11", "office": "New York", "extn": "8327" }, { "name": "Finn Camacho", "position": "Support Engineer", "salary": "$87,500", "start_date": "2009/07/07", "office": "San Francisco", "extn": "2927" }, { "name": "Serge Baldwin", "position": "Data Coordinator", "salary": "$138,575", "start_date": "2012/04/09", "office": "Singapore", "extn": "8352" }, { "name": "Zenaida Frank", "position": "Software Engineer", "salary": "$125,250", "start_date": "2010/01/04", "office": "New York", "extn": "7439" }, { "name": "Zorita Serrano", "position": "Software Engineer", "salary": "$115,000", "start_date": "2012/06/01", "office": "San Francisco", "extn": "4389" }, { "name": "Jennifer Acosta", "position": "Junior Javascript Developer", "salary": "$75,650", "start_date": "2013/02/01", "office": "Edinburgh", "extn": "3431" }, { "name": "Cara Stevens", "position": "Sales Assistant", "salary": "$145,600", "start_date": "2011/12/06", "office": "New York", "extn": "3990" }, { "name": "Hermione Butler", "position": "Regional Director", "salary": "$356,250", "start_date": "2011/03/21", "office": "London", "extn": "1016" }, { "name": "Lael Greer", "position": "Systems Administrator", "salary": "$103,500", "start_date": "2009/02/27", "office": "London", "extn": "6733" }, { "name": "Jonas Alexander", "position": "Developer", "salary": "$86,500", "start_date": "2010/07/14", "office": "San Francisco", "extn": "8196" }, { "name": "Shad Decker", "position": "Regional Director", "salary": "$183,000", "start_date": "2008/11/13", "office": "Edinburgh", "extn": "6373" }, { "name": "Michael Bruce", "position": "Javascript Developer", "salary": "$183,000", "start_date": "2011/06/27", "office": "Singapore", "extn": "5384" }, { "name": "Donna Snider", "position": "Customer Support", "salary": "$112,000", "start_date": "2011/01/25", "office": "New York", "extn": "4226" }];

        $(document).ready(function () {

            var table = $('#register').DataTable({
                dom: 'fBtip',
                pageLength: 10,
                buttons: [
                    {
                        text: '<i class="fa fa-id-badge fa-fw fa-lg" aria-hidden="true"></i>',
                        action: function () {
                            
                            $("#register").toggleClass("cards");
                            $("#card-toggle .fa").toggleClass([ "fa-table", "fa-id-badge" ]);
                            $("#register thead").toggle();
                        
                            if($("#register").hasClass("cards")){

                                // Create an array of labels containing all table headers
                                var labels = [];
                                $('#register').find('thead th').each(function() {
                                    labels.push($(this).text());
                                });

                                // Add data-label attribute to each cell
                                $('#register').find('tbody tr').each(function() {
                                    $(this).find('td').each(function(column) {
                                        $(this).attr('data-label', labels[column]);
                                    });
                                });

                                var max = 0;
                                $('#register tr').each(function() {
                                    max = Math.max($(this).height(), max);
                                }).height(max);

                            } else {

                                // Remove data-label attribute from each cell
                                $('#register').find('td').each(function() {
                                    $(this).removeAttr('data-label');
                                });

                                $("#register tr").each(function(){
                                    $(this).height("auto");
                                });
                                
                            }
                        },
                        attr:  {
                            title: 'Change views',
                            id: 'card-toggle'
                        }
                    }
                ],
                select: 'single',
                data: sampleData,
                columns: [
                    {   /* created column to show a picture just to make this demo look better */
                        "orderable": false, "data": "Photo", "name": "Photo", "defaultContent": "",
                        "visible": true, "className": "text-center", "width": "20px",
                        "createdCell": function (td, cellData, rowData, row, col) {
                            var $ctl = $('<i class="fa fa-user fa-fw"></i>').css('color', colors[Math.floor(Math.random() * colors.length) + 1])
                            $(td).append($ctl);
                        }
                    },
                    {
                        "data": "name",
                        "name": "name"
                    },
                    {
                        "data": "position",
                        "name": "position"
                    },
                    {
                        "data": "salary",
                        "name": "salary",
                        "class": "text-right"
                    },
                    {
                        "data": "start_date",
                        "name": "start_date",
                        "class": "text-right"
                    },
                    {
                        "data": "office",
                        "name": "office",
                        "visible": false
                    },
                    {
                        "data": "extn",
                        "name": "extn"
                    }
                ],
                initComplete: function () {
                    var api = this.api();
                    var rows = api.rows().nodes();
                    var values = $.map(api.column('office:name').data().sort().unique(), function(value, index) { return [value]; });

                    var legend = '';
                    for (var key in values) {
                        legend += '<dt class="col-1">'+key+'</dt><dd class="col-11">'+values[key]+'</dd>';
                    }
                    legend = '<dl class="row">'+legend+'</dl>';
                    $("#legend").append(legend);

                    api.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
                        var index = values.indexOf(this.cell(rowLoop,'office:name').node().innerHTML);
                        var data = this.cell(rowLoop,'position:name').data();
                        data = data.replace(/<sup.*>.*?<\/sup>/ig, '');
                        this.cell(rowLoop,'position:name').data( data+' <sup>'+index+'</sup>');
                    } );
                }
            })
            .on('select', function (e, dt, type, indexes) {
                var rowData = table.rows(indexes).data().toArray()
                $('#row-data').html(JSON.stringify(rowData))
            })
            .on('deselect', function () {
                $('#row-data').html('')
            })
            
            
        });
    </script>
</head>
<body>
<div class="container-fluid">
<div class="row m-3">
<h5>DataTables as Card View <span style="color:red;">(Legend test)</span>:</h5>
</div>
<div class="row m-3 border border-info bg-light">
<div class="col-6">
<h6>Adopted from:</h6>
<ul>
<li><a href="https://web.archive.org/web/20170605170544/http://azguys.com/datatables/index.html" target="_blank">This page on the Way Back Machine</a> and <a href="https://datatables.net/forums/discussion/comment/123294/#Comment_123294" target="_blank">this discussion on the Datatables forums</a></li>
<li>Updated to Datatables 1.10.16 and Select 1.2.4, JQuery 3.2.1, and Bootstrap 4 beta 3; included Font Awesome 4.7</li>
<li>Streamlined css; added a js 'deselect' to appropriately remove the row data from the alert on the bottom</li>
</ul>
</div>
<div class="col-6">
<h6>Features:</h6>
<ul>
<li>Simple CSS allows the table to switch from normal table layout view to a card type view.</li>
<li>No hiding of the datatable and creating a secondary card type display.</li>
<li>Retains all datatable API interoperability, paging and filtering, row select.</li>
</ul>
</div>
</div>
<div class="row m-3">
<div class="col alert alert-primary" role="alert">
Row data: <span id="row-data"></span>
</div>
</div>
<div class="row m-3">
<div class="col-9">
<table id="register" class="table table-sm table-hover" cellspacing="0">
<thead>
<tr>
<th></th>
<th>Name</th>
<th>Position</th>
<th>Salary</th>
<th>Start</th>
<th>Office</th>
<th>Extn</th>
</tr>
</thead>
</table>
</div>
<div class="col-3">
<div class="card animated bounce">
<h5 class="card-header">Legend</h5>
<div class="card-body">
<p id="legend" class="card-text"></p>
</div>
</div>
</div>
</div>
</div>
<script src="https://ajax.cloudflare.com/cdn-cgi/scripts/95c75768/cloudflare-static/rocket-loader.min.js" data-cf-settings="492e21ba4dbe2f246c90df61-|49" defer=""></script></body>
</html>