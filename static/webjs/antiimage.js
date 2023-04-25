document.addEventListener('contextmenu', event => event.preventDefault());
var images = document.getElementsByTagName("img");
    for (var i = 0; i < images.length; i++) {
        images[i].setAttribute("draggable", "false");
    }