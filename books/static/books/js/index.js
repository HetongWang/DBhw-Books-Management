$(function() {
    $('#search-submit').bind('click', function() {
		var search_content = $('#search-content').val();
		if (search_content == '')
			$('#message').text('You have to type something').css('display', 'block');
		else
	        window.location = '/search/' + search_content
    });
});
