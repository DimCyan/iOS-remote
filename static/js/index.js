window.onload = function () {
    var div1 = document.getElementById("remote");
    var disX = disY = 0;

    div1.onmousedown = function (e) {
        var evnt = e || event;
        var eleH = div1.offsetHeight;
        var eleW = div1.offsetWidth;
        console.log('H: ' + eleH + ' W:' + eleW)
        disX = evnt.offsetX - div1.offsetLeft;
        disY = evnt.offsetY - div1.offsetTop;

        div1.onmousemove = function (e) {
            var evnt = e || event;
            var x = evnt.offsetX - div1.offsetLeft;
            var y = evnt.offsetY - div1.offsetTop;

            div1.onmouseup = function () {
                if (x || y) {
                    var data = {
                        data: JSON.stringify({
                            'disX': (disX / eleW).toFixed(2),
                            'disY': (disY / eleH).toFixed(2),
                            'toX': (x / eleW).toFixed(2),
                            'toY': (y / eleH).toFixed(2)
                        }),
                    }
                    console.log('drag: ' + disX + ' , ' + disY + ' to: ' + x + ' , ' + y)
                    $.ajax({
                        url: 'http://localhost:5000/drag',
                        type: 'POST',
                        data: data,
                        dataType: 'json',
                    })
                }
                div1.onmousemove = null;
                div1.onmouup = null;
            };
        };

        div1.onmouseup = function () {
            if (disX || disY) {
                var data = {
                    data: JSON.stringify({
                        'disX': (disX / eleW).toFixed(2),
                        'disY': (disY / eleH).toFixed(2)
                    }),
                }
                console.log('click: ' + disX + ' , ' + disY)
                $.ajax({
                    url: 'http://localhost:5000/click',
                    type: 'POST',
                    data: data,
                    dataType: 'json',
                })
            }
            div1.onmousemove = null;
            div1.onmouup = null;
        };

        return false;
    };
    $("#main-send").focus(function () {
        $("#main-send").keydown(function (e) {
            if (e.keyCode == 13 && e.ctrlKey == 1) {
                console.log('ctrl+enter!!!');
                var content = $("#main-send").val();
                var data = {
                    data: JSON.stringify({
                        'text': content,
                    }),
                };
                console.log('send: ' + content);
                $.ajax({
                    url: 'http://localhost:5000/send',
                    type: 'POST',
                    data: data,
                    dataType: 'json',
                });
                $("#main-send").val("");
            };
            if (e.keyCode == 8 && e.ctrlKey == 1) {
                console.log('backspace!!!');
                $.ajax({
                    url: 'http://localhost:5000/backspace',
                    type: 'POST',
                });
            };
            if (e.keyCode == 13 && e.shiftKey == 1) {
                console.log('enter!!!');
                $.ajax({
                    url: 'http://localhost:5000/enter',
                    type: 'POST',
                });
                $("#main-send").val("");
            };
        })
    });
    $("#connect-stream").click(function () {
        $("#remote").attr("src", $("#connect-input").val());
    });
    $(".home").click(function () {
        console.log('click home buttom')
        $.ajax({
            url: 'http://localhost:5000/home',
            type: 'POST',
        })
    });
    $(".lock").click(function () {
        console.log('Press lock button')
        $.ajax({
            url: 'http://localhost:5000/lock',
            type: 'POST',
        })
    });
    $(".screenshot").click(function () {
        console.log('click screenshot buttom')
        $.ajax({
            url: 'http://localhost:5000/screenshot',
            type: 'POST',
        })
    });
    $(".rotation").click(function () {
        console.log('switch orientation')
        $.ajax({
            url: 'http://localhost:5000/rotation',
            type: 'POST',
        })
    });
    $("#resize").click(function () {
        $("#remote").css("width", "100%");
    });
    $("#resize75").click(function () {
        $("#remote").css("width", "75%");
    });
    $("#resize50").click(function () {
        $("#remote").css("width", "50%");
    });
    $("#resize45").click(function () {
        $("#remote").css("width", "45%");
    });
};