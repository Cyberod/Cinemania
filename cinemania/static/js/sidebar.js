
document.addEventListener("DOMContentLoaded", function () {
    // Select all dropdown links
    const dropdowns = document.querySelectorAll(".sidebar-link.dropdown");

    dropdowns.forEach((dropdown) => {
        const toggleButton = dropdown.querySelector(".bx-chevron-down");
        const menu = dropdown.querySelector(".sidebar-menu");

        // Add event listener to toggle the dropdown menu
        toggleButton.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior if any


            // Toggle the "active" class to show/hide the menu
            menu.classList.toggle("active");

           

            // Rotate the chevron icon
            toggleButton.classList.toggle("rotate");
        });

        // Close dropdown if clicked outside
        document.addEventListener("click", function (event) {
            if (!dropdown.contains(event.target)) {
                menu.classList.remove("active");
                toggleButton.classList.remove("rotate");
            }
        });
    });
});

    
