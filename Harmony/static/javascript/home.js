document.addEventListener('DOMContentLoaded', function () {
    // Get the current page URL
    var currentPage = window.location.href;
    var menuItems = document.querySelectorAll('.menu-item');
    
    
    // Select the menu item based on the current page
    var menuItem = document.querySelector('a[href="' + currentPage + '"]');
    console.log(menuItem);
    // Add the "active" class if a matching menu item is found
    if (menuItem) {
        menuItem.classList.add('App__category-item--selected');
    }
});


$(document).ready(function () {
    // const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $("#searchInput").on("input", function () {
      const searchTerm = $(this).val();
      $.ajax({
        url: "search", 
        method: "get", 
        data: { q: searchTerm },
        success: function (response) {
            // var x=JSON.parse(response)
          console.log(response);
        },
        error: function (error) {
          console.error("Error:", error);
        }
      });
    });
  });
