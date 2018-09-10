$(function () {
    $("#rotate").click(function () {
        var filename = $('.img01').attr('src');
        var array = filename.split('/');
        var name = array[array.length - 1];
        var b = name.indexOf('?') != -1;
        var ss = name;
        console.log(ss);
        if (b) {
            var dd = name.split('?');
            ss = dd[0];
        } else {
            ss = name;
        }
        zlajax.get({
            'url': '/rotate',
            'data': {
                filename: ss
            },
            'success': function (data) {
                /*后面加个随机数是方便页面刷新*/
                $('.img01').attr('src', '../../static/ima/' + data['filename'] + "?t=" + Math.random());
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
});


$(function () {
    $("#tongdao").click(function () {
        var filename = $('.img01').attr('src');
        var array = filename.split('/');
        var name = array[array.length - 1];
        var b = name.indexOf('?') != -1;
        var ss = name;
        console.log(ss);
        if (b) {
            var dd = name.split('?');
            ss = dd[0];
        } else {
            ss = name;
        }
        zlajax.get({
            'url': '/tongdao',
            'data': {
                filename: ss
            },
            'success': function (data) {
                /*后面加个随机数是方便页面刷新*/
                $('.img01').attr('src', '../../static/ima/' + data['filename'] + "?t=" + Math.random());
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
});

$(function () {
    $("#filter").click(function () {
        var filename = $('.img01').attr('src');
        var array = filename.split('/');
        var name = array[array.length - 1];
        var b = name.indexOf('?') != -1;
        var ss = name;
        console.log(ss);
        if (b) {
            var dd = name.split('?');
            ss = dd[0];
        } else {
            ss = name;
        }
        zlajax.get({
            'url': '/filter',
            'data': {
                filename: ss
            },
            'success': function (data) {
                /*后面加个随机数是方便页面刷新*/
                $('.img01').attr('src', '../../static/ima/' + data['filename'] + "?t=" + Math.random());
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
});