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
});