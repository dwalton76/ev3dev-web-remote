
// Prevent the page from scrolling on an iphone
// http://stackoverflow.com/questions/7768269/ipad-safari-disable-scrolling-and-bounce-effect
$(document).bind(
    'touchmove',
    function(e) {
        e.preventDefault();
    }
);

function keydown(keyCode) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send.key', true);
    xhr.send(keyCode + ',1');
}

function keyup(keyCode) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send.key', true);
    xhr.send(keyCode + ',0');


    // Refresh the screen on keyup
    d = new Date();
    $("#brick img").attr("src", "/framebuffer.png?"+d.getTime());
}


$(document).ready(function() {

    $(document).keydown(function(e) {
        // console.log("keydown: " + e.keyCode)
        e.preventDefault();

        if (!e.repeat) {
            keydown(e.keyCode);
        }
    });

    $(document).keyup(function(e) {
        // console.log("keyup: " + e.keyCode)
        e.preventDefault();

        if (!e.repeat) {
            keyup(e.keyCode);
        }
    });

    // BACKSPACE is 8
    // UP is 38
    // LEFT is 37
    // ENTER is 13
    // RIGHT is 39
    // DOWN is 40
    $("#back").click(function() {
        console.log("back clicked")
        keydown(8);
        keyup(8);
    });

    $("#up").click(function() {
        console.log("on clicked")
        keydown(38);
        keyup(38);
    });

    $("#left").click(function() {
        console.log("left clicked")
        keydown(37);
        keyup(37);
    });

    $("#enter").click(function() {
        console.log("enter clicked")
        keydown(13);
        keyup(13);
    });

    $("#right").click(function() {
        console.log("right clicked")
        keydown(39);
        keyup(39);
    });

    $("#down").click(function() {
        console.log("down clicked")
        keydown(40);
        keyup(40);
    });
});
