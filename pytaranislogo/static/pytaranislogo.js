$(function() {
    // Load flash messages
    $( "#flashDialogSuccess" ).dialog({
        autoOpen: true,
        dialogClass: 'success',
        modal: true,
        open: function(event, ui) {
            setTimeout(function(){
            $('#dialog').dialog('close');                
            }, 5000);
        },
        buttons: {
            Close: function() {
                $(this).dialog("close");
            }
        }
    });
    $( "#flashDialogError" ).dialog({
        autoOpen: true,
        dialogClass: 'error',
        modal: true,
        buttons: {
            Close: function() {
                $(this).dialog("close");
            }
        }
    });
    $( "#flashDialogInfo" ).dialog({
        autoOpen: true,
        dialogClass: 'info',
        modal: true,
        open: function(event, ui) {
            setTimeout(function(){
            $('#dialog').dialog('close');                
            }, 5000);
        },
        buttons: {
            Close: function() {
                $(this).dialog("close");
            }
        }
    });
});
