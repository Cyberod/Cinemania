'use strict';

/**
 * Add events on elements
 */

const addEventOnElements = function (elements, eventType, callback) {
    for (const elem of elements) elem.addEventListener(eventType, callback);
}


/**
 * Toggle search box in mobile device || mall creen
 */

const searchBox = document.querySelector("[search-box]");
const searchTogglers = document.querySelectorAll("[search-toggler]");
const menuTogglers = document.querySelectorAll("[menu-toggler]");


addEventOnElements(searchTogglers, "click", function() { 
    searchBox.classList.toggle("active");

 });

 const sidebar = document.querySelector(".sidebar");
 addEventOnElements(menuTogglers, "click", function() {
     sidebar.classList.toggle("active");
 });
 
 /**
  * Close sidebar when clicking outside
  */
 document.addEventListener("click", function(event) {
     if (!event.target.closest(".sidebar") && !event.target.closest("[menu-toggler]")) {
         sidebar.classList.remove("active");
     }
 });

 const searchForm = document.getElementById('search-form');
const searchInput = searchForm.querySelector('input[name="query"]');

searchForm.addEventListener('submit', function(event) {
    if (searchInput.value.trim() === '') {
        event.preventDefault();
    }
});





 





