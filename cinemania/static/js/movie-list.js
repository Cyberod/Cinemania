document.addEventListener('DOMContentLoaded', () => {
    const loadMoreButton = document.getElementById('load-more-button')
    const image_base_url = "https://image.tmdb.org/t/p/w500"
    const urlPattern = loadMoreButton ? loadMoreButton.dataset.urlPattern : '';
    const viewType = loadMoreButton ? loadMoreButton.dataset.viewType : '';
    const searchQuery = new URLSearchParams(window.location.search).get('query');


    function renderMovieCard(movie) {
        const movieCard = document.createElement('div');
        movieCard.classList.add('movie-card');
        const movieDetailUrl = urlPattern.replace('0', movie.id);
        movieCard.innerHTML = `
            <figure class="poster-box card-banner">
                <img src="${image_base_url}${movie.poster_path}" alt="${movie.title}" class="img-cover">
            </figure>
            <h4 class="title">${movie.title}</h4>
            <div class="meta-list">
                <div class="meta-item">
                    <span class="span">${movie.vote_average.toFixed(1)}</span>
                    <i class='bx bxs-star' style='color:#ffb43a' width="20" height="20" loading="lazy" alt="rating"></i>
                </div>
                <div class="card-badge">${movie.release_date.slice(0, 4)}</div>
            </div>
            <a href="${movieDetailUrl}" class="card-btn" title="${movie.title}"></a>
        `;
        return movieCard;
    }

    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', async () => {
            const nextPage = loadMoreButton.dataset.nextPage;
            console.log('Next Page to load:', nextPage);

            let url;
            if (viewType === 'search') {
                url = `?query=${searchQuery}&page=${nextPage}`;
            }
            else {
                url = `?page=${nextPage}`;
            }

            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });

            if (response.ok) {
                const data = await response.json();
                const movieArray = data.movie || [];
                console.log('Data received:', movieArray)
                const sliderInner = document.getElementById('slider-inner');

                movieArray.forEach(movie => {
                    const movieCard = renderMovieCard(movie);
                    sliderInner.appendChild(movieCard);
                });
                
                if (data.page < data.total_pages) {
                    loadMoreButton.dataset.nextPage = parseInt(nextPage) + 1
                } else {
                    loadMoreButton.remove();
                }
            } else {
                console.error('failed to load more movies');
            }

        });
    }
});

