
document.addEventListener('DOMContentLoaded', function() {
    var dropdowns = document.getElementsByClassName("dropdown");
    for (var i = 0; i < dropdowns.length; i++) {
        dropdowns[i].addEventListener("click", function() {
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
});


