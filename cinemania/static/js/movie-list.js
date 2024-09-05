
document.addEventListener('DOMContentLoaded', () => {
    const loadMoreButton = document.getElementById('load-more-button');
    const image_base_url = 'https://image.tmdb.org/t/p/w500/'
    const urlPattern = loadMoreButton ? loadMoreButton.dataset.urlPattern : '';
    

    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', async () => {
            const nextPage = loadMoreButton.dataset.nextPage;
            console.log('Next Page to load:', nextPage);

            const response = await fetch(`?page=${nextPage}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            /* const movieArray = [] */
            if (response.ok) {
                const data = await response.json();
                const movieArray = data.movie || [];
                data?.movie?.map(movie => movieArray.push(movie));
                console.log('Data received:', movieArray);
                const sliderInner = document.getElementById('slider-inner'); /* you can try movie-grid here instead */

                movieArray?.forEach(movie => {
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
                    sliderInner.appendChild(movieCard);
                });

                if (data.page < data.total_pages) {
                    loadMoreButton.dataset.nextPage = parseInt(nextPage) + 1;
                } else {
                    loadMoreButton.remove();
                }
            } else {
                console.error('Failed to load more movies');
            }
        });
    }
});
