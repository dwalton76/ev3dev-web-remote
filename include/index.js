
// Prevent the page from scrolling on an iphone
// http://stackoverflow.com/questions/7768269/ipad-safari-disable-scrolling-and-bounce-effect
$(document).bind(
    'touchmove',
    function(e) {
        e.preventDefault();
    }
);


$(document).ready(function() {

    $(document).keydown(function(e) {
        // console.log("keydown: " + e.keyCode)
        e.preventDefault();

        if (!e.repeat) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/send.key', true);
            xhr.send(e.keyCode + ',1');
        }
    });

    $(document).keyup(function(e) {
        // console.log("keyup: " + e.keyCode)
        e.preventDefault();

        if (!e.repeat) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/send.key', true);
            xhr.send(e.keyCode + ',0');
        }
    });
});
