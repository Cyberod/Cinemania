export function initializeSidebar() {
    document.body.addEventListener('click', function(event) {
        if (event.target.closest('.dropdown')) {
            const dropdown = event.target.closest('.dropdown');
            console.log("Dropdown clicked");
            dropdown.querySelector('.sidebar-menu').classList.toggle('show');
        } else if (!event.target.closest('.sidebar-menu')) {
            document.querySelectorAll('.sidebar-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
}




/* 
export function initializeSidebar() {
    console.log("initializeSidebar function called");
    var dropdowns = document.getElementsByClassName("dropdown");
    for (var i = 0; i < dropdowns.length; i++) {
        dropdowns[i].addEventListener("click", function() {
            console.log("Dropdown clicked");
            this.getElementsByClassName("sidebar-menu")[0].classList.toggle("show");
        });
    }

    window.onclick = function(event) {
        if (!event.target.matches('.dropdown')) {
            var dropdowns = document.getElementsByClassName("sidebar-menu");
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }
}; */




/* document.addEventListener('click', function(event) {
    if (event.target.matches('.dropdown')) {
        event.target.querySelector('.sidebar-menu').classList.toggle('show');
    } else if (!event.target.closest('.dropdown')) {
        var dropdowns = document.getElementsByClassName("sidebar-menu");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
});

function initializeDropdowns() {
    var dropdowns = document.getElementsByClassName("dropdown");
    for (var i = 0; i < dropdowns.length; i++) {
        dropdowns[i].addEventListener("click", function() {
            this.getElementsByClassName("sidebar-menu")[0].classList.toggle("show");
        });
    }
}

document.addEventListener('DOMContentLoaded', initializeDropdowns);

// Call initializeDropdowns() after loading new content via AJAX

 */