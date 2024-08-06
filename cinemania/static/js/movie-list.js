// static/js/trending.js

document.addEventListener('DOMContentLoaded', () => {
    const loadMoreButton = document.getElementById('load-more-button');
    
    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', async () => {
            const nextPage = loadMoreButton.dataset.nextPage;
            const response = await fetch(`?page=${nextPage}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const movies = data.movies;
                const movieGrid = document.getElementById('movie-grid');
                
                movies.forEach(movie => {
                    const movieCard = document.createElement('div');
                    movieCard.classList.add('movie-card');
                    movieCard.innerHTML = `
                        <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">
                        <h2>${movie.title}</h2>
                    `;
                    movieGrid.appendChild(movieCard);
                });
                
                if (data.has_next) {
                    loadMoreButton.dataset.nextPage = data.next_page_number;
                } else {
                    loadMoreButton.remove();
                }
            } else {
                console.error('Failed to load more movies');
            }
        });
    }
});
