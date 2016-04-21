
    function start() {
    var elem = document.getElementById("lapBar"); 
    var width = 10;
    var id = setInterval(frame, 10);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++; 
            elem.style.width = width + '%'; 
            document.getElementById("lapTime").innerHTML = width * 1  + '%';
        }
    }
}


    function download() {
    var elem = document.getElementById("downloadBar"); 
    var width = 10;
    var id = setInterval(frame, 10);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++; 
            elem.style.width = width + '%'; 
            document.getElementById("downloadTime").innerHTML = width * 1  + '%';
        }
    }
}
