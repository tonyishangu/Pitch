$(document).ready(function () {
    $("#profbutton").click(function () {
        $("#updates").slideDown('1500').hide('1000');
        $("#imgform").show('1500');
    });
    $("#submit").click(function () {
        $("#imgform").slideUp('1500');
        $("#updates").slideDown('1500');
    });
});