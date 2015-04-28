var tagClick = function(tag) {
    var $tag = $(tag);
    $('.side-bar-tag').removeClass('active-tag')
    $tag.addClass('active-tag');
    var formid = '#' + tag.id + '-tag';
    $('.mng-tag').addClass('hidden');
    $(formid).removeClass('hidden');
};

var postmsg = function(succ, msg) {
    var $div = $('<div class="message alert" style="display:none;" role="alert"></div>')
    $('#op-field').prepend($div);

    if (succ) {
        $div.addClass('alert-success').text(msg)
            .fadeIn();
    }
    else {
        $div.addClass('alert-danger').html('<b>Error: </b>' + msg)
            .fadeIn();
    }

    setTimeout(function() {
        $div.fadeOut(function() {
            $div.remove();
        });
    }, 3000)
};

var getcsrftoken = function() {
    var cookie = document.cookie + ';';
    csrftoken = cookie.match(/csrftoken=(\w+);/)[1];
    return csrftoken;
}

$(function() {
    $('.side-bar-tag').bind('click', function() {
        tagClick(this);
        $('#message').addClass('hidden');
    });
    $('form').submit(function(event) {
        event.preventDefault();
        var _id = $(this).parent()[0].id
        if (_id == 'book-file-tag')
            return false;

        var action = _id.match(/(\w+)-(\w+)-tag/);
        action = action[1] + '_' + action[2];

        var data = {'action': action};
        inputs = $(this).find('input');
        for (var i = inputs.length - 1; i >= 0; i--) {
            data[inputs[i].name] = $(inputs[i]).val();
        };  
        var csrftoken = getcsrftoken();

        $.ajax({
            url: '/libadmin/',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data, status, xhr) {
                if (data.err == false)
                    postmsg(true, 'Operate Successfully');
                else
                    postmsg(false, data.msg);
            },
            error: function(xhr, errorType, error) {
                postmsg(false, 'Unexcept error, please check input');
            }
        });
    });
    $('#book-file-tag').children('form').submit(function(event) {
        var action = 'add_book';
        var jsonstr = $(this).find('textarea').val();
        try {
            var jsondata = JSON.parse(jsonstr);
        }
        catch (e) {
            postmsg(false, 'Please typte standard JSON');
        }
        if (jsondata !== undefined) {
            if (Object.prototype.toString.call(a) === '[object Array]')
                jsondata = [jsondata];

            for (var i = 0; i < jsondata.length; i++) {
                var data = jsondata[i];

                $.ajax({
                    url: '/libadmin/',
                    type: 'POST',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify(data),
                    dataType: 'json',
                    beforeSend: function(xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", getcsrftoken());
                    },
                    success: function(data, status, xhr) {
                        if (data.err == false)
                            postmsg(true, 'Operate Successfully');
                        else
                            postmsg(false, data.msg);
                    },
                    error: function(xhr, errorType, error) {
                        postmsg(false, 'Unexcept error, please check input');
                    }
                });
            }
        }
    });
});