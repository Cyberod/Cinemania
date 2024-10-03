document.addEventListener('DOMContentLoaded', function() {
    const sliderItems = document.querySelectorAll('.slider-item');
    const posterBoxes = document.querySelectorAll('.poster-box');

    function setActiveItem(movieId) {
        sliderItems.forEach(item => {
            if (item.dataset.movieId === movieId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        posterBoxes.forEach(box => {
            if (box.dataset.movieId === movieId) {
                box.classList.add('active');
            } else {
                box.classList.remove('active');
            }
        });
    }

    posterBoxes.forEach(box => {
        box.addEventListener('click', function() {
            const movieId = this.dataset.movieId;
            setActiveItem(movieId);
        });
    });
});
