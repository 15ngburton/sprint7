$(function(context) {
  return function() {
    console.log("THIS TEXT");
    var thumbnails = document.getElementsByClassName("thumbnail");
    for (i = 0; i < thumbnails.length; i++) {
      thumbnails[i].onmouseover = function() {
        document.getElementById("largeImage").setAttribute("src", this.getAttribute("src"))
      }
    }
  }
}(DMP_CONTEXT.get()))
