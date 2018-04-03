$(function(context) {
    return function() {

        var container = $('#inner_page')
        var catID = document.getElementById("catID").innerHTML
        console.log(catID)
        var page_num = document.getElementById("pageNumber").innerHTML
        console.log(page_num)
        var num_of_pages = document.getElementById("maxPageNumber").innerHTML
        console.log(num_of_pages)
        container.load('/catalog/innerindex/' + catID + "/" + page_num)
        var changeInPage = 0

        document.getElementById('previous_page').onclick = function() {
          if (changeInPage + parseInt(page_num) > 1){
            changeInPage = changeInPage - 1;
            var currentPage = String(parseInt(page_num) + changeInPage)
            container.load('/catalog/innerindex/' + catID + "/" + currentPage)
            document.getElementById("current_page").innerHTML = currentPage
          }
        };

        document.getElementById('next_page').onclick = function() {
          if (changeInPage + parseInt(page_num) < num_of_pages){
            changeInPage = changeInPage + 1;
            var currentPage = String(parseInt(page_num) + changeInPage)
            container.load('/catalog/innerindex/' + catID + "/" + currentPage)
            document.getElementById("current_page").innerHTML = currentPage
          }
        };
    }
}(DMP_CONTEXT.get()))
