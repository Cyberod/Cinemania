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

addEventOnElements(searchTogglers, "click", function() { 
    searchBox.classList.toggle("active");
    subBtn.classList.toggle("active");
    dropdown.classList.toggle("active");
 });


 export function initializeSidebar() {
    const menuBtn = document.querySelector('[menu-btn]');
    const sidebar = document.querySelector('.sidebar');

    menuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        menuBtn.classList.toggle('active');
    });

    // ... existing click event listener ...
}




