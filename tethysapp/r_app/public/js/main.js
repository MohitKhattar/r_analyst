function requestFullScreen(element) {
    // Supports most browsers and their versions.
    var requestMethod = element.requestFullScreen || element.webkitRequestFullScreen || element.mozRequestFullScreen || element.msRequestFullscreen;

    if (requestMethod) { // Native full screen.
        requestMethod.call(element);
    } else if (typeof window.ActiveXObject !== "undefined") { // Older IE.
        var wscript = new ActiveXObject("WScript.Shell");
        if (wscript !== null) {
            wscript.SendKeys("{F11}");
        }
    }
}

function makefullscreen() {

    //make iframe take up entire space
    var ifr = document.getElementById("output");
    ifr.className = 'fullscreen';

    //var elem = document.body;
    requestFullScreen(ifr);
}

$('#get-form').on('submit', function(event){

    event.preventDefault();
    console.log("form submitted!");
    create_get();
    });


function create_get() {
    console.log("create get called");

    var ifr = document.getElementById('output');

    var params = create_paramStr();

    console.log(params);

    ifr.setAttribute('src', "http://".concat(get_host()).concat("/cgi-bin/R/tethys-scripts/").concat(get_fileName()).concat(params));

    ifr.removeAttribute('hidden');
    document.getElementById('fullscreen').style.visibility = 'visible';

}
