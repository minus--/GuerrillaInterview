$(document).ready(function() {

    /*var dataSet = [
        ['John Doe','Engineer','Tunis','30','30-01-2014','10,000 $'],
        ['Doe John','Manager','Tunis','34','30-03-2014','15,000 $']
    ];

    var colDef = [
        { "title": "Name" },
        { "title": "Position" },
        { "title": "Office" },
        { "title": "Age"},
        { "title": "StartDate"},
        { "title": "Salary"}
    ];

    $('<table class="display" id="tmain_table" width="100%" </table>').appendTo('#table_container');

    var table = $('#tmain_table').dataTable({
        "data": dataSet,
        'columns': colDef
    });*/

    $('#create_table_id').click(function()
    {
        $('#table_container1').append('<button id="create_table1_id" class="btn btn-primary">Submit</button>');
    });

});