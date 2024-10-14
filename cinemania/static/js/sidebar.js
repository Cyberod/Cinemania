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
