var tagClick = function(tag) {
	var $tag = $(tag);
	$('.side-bar-tag').removeClass('active-tag')
	$tag.addClass('active-tag');
	var formid = '#' + tag.id + '-tag';
	$('.mng-tag').addClass('hidden');
	$(formid).removeClass('hidden');
}

$(function() {
	$('.side-bar-tag').bind('click', function() {
		tagClick(this);
	});
	$('.btn').click(function(event) {
		event.preventDefault();
		var _id = this.id.replace('mng', 'book')
		var action = _id.match(/(\w+)-(\w+)-submit/);
		action = action[2] + '_' + action[1];

		var data = {'action': action};
		inputs = $('#' + this.id.replace('submit', 'tag')).find('input');
		for (var i = inputs.length - 1; i >= 0; i--) {
			data[inputs[i].name] = $(inputs[i]).val();
		}; 

		var cookie = document.cookie + ';';
		csrftoken = cookie.match(/csrftoken=(\w+);/)[1];

		$.ajax({
			url: '/libadmin/',
    		type: 'POST',
    		contentType: 'application/json; charset=utf-8',
    		data: JSON.stringify(data),
    		dataType: 'json',
    		beforeSend: function(xhr, settings) {
            	xhr.setRequestHeader("X-CSRFToken", csrftoken);
    		}
		});
	});
});