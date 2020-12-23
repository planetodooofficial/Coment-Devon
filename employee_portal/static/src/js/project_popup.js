$(document).ready(function(){

//    For popup window
	$('.launch-modal').click(function(){
		$('#myModal').modal({
			backdrop: 'static'
		});
	});

//	For numeric keypad
	$('.num').click(function () {
        var num = $(this);
        var text = $.trim(num.find('.txt').clone().children().remove().end().text());
        var telNumber = $('#telNumber');
        $(telNumber).val(telNumber.val() + text);
    });

//    Clear button
    $('#btn-clr').click(function () {
        $('#telNumber').val("");
    });

});

