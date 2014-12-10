function set_language(language_code, editor) {
    var assignment_id = $('#assignment_id').val();
    var url = '/sample/'+ assignment_id +'/' + language_code;
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        contentType: "application/json",
        accepts: "application/json",
        success: function(data) {
            editor.getDoc().setValue(data['sample']);
        }
    });
}

/*
 Document initialization
 */
$(document).ready(function() {
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        lineNumbers: true,
        matchBrackets: true,
        mode: "text/x-csharp",
        continueComments: "Enter",
        extraKeys: {"Ctrl-Q": "toggleComment"}
        });
    var language_code = 1;
    set_language(language_code,editor);
    $('#language-select').change(function(){
        var selection = $(this).val();
        editor.setOption("mode", selection);
        switch (selection){
            case 'text/x-csharp':
                language_code = 1;
                break;
            case 'javascript':
                language_code = 17;
                break;
            case 'python':
                language_code = 5;
                break;
            default:
                language_code = 1;
                break;
        };
        set_language(language_code,editor);
    });

    $('#submit_button').on('click', function(e) {
        e.preventDefault();
        alert("submit");

        var user_code = editor.getValue();
        var message = {
            code: user_code
        };

        $.ajax({
            type: 'POST',
            url: '/assignment/1',
            dataType: 'json',
            data: JSON.stringify(message),
            contentType: "application/json",
            accepts: "application/json",
            success: function (data) {
                console.log("saved");
            }, error: function (data) {
                console.log("not saved");
            }, complete: function (data) {

            }
        });
    });

    $('#run_button').on('click', function(e) {
        e.preventDefault();
        var user_code = editor.getValue();
        var message = {
            LanguageChoiceWrapper: language_code,
            Program: user_code
        };

        $.ajax({
            type: 'POST',
            url: '/run',
            dataType: 'json',
            data: JSON.stringify(message),
            contentType: "application/json",
            accepts: "application/json",
            success: function(data) {
                var result = data['Result'];
                var warning = data['Warnings'];
                var error = data['Errors'];
                var stat = data['Stats'];
                // Clean the API response for display
                if (result == null)
                    result = '';
                if (stat == null)
                    stat = '';
                if (warning == null)
                    warning = '';
                if (error == null)
                    error = '';
                // Display the result in the dedicated html node
                $('#code_result').html('<p><b>Result: </b></p>'+result);
                $('#code_stats').html('<p><i>'+stat+'</i></p>');
                $('#code_warnings').html('<p><b>Warning: </b></p>'+warning);
                $('#code_errors').html('<p><b>Error: </b></p>'+error);
            }, error: function (data) {
                $('#code_warnings').html('<p><b>Warning: </b></p>'+JSON.stringify( data ));
            }, complete: function ( data ) {

            }
        });
    });
});
