

    function fetchMovies() {
        let query = document.getElementById("searchQuery").value;
        
        // Clear results if the search box is empty
        if (query === "") {
            document.getElementById("searchResults").innerHTML = "";
            return;
        }

        // TMDB API endpoint for searching movies
        let apiURL = '/search/?query=${query}';

        fetch(apiURL)
            .then(response => response.json())
            .then(data => {
                let movies = data.results;
                displayResults(movies);
            })
            .catch(error => console.error('Error fetching movies:', error));
    }

    function displayResults(movies) {
        let searchResults = document.getElementById("searchResults");
        searchResults.innerHTML = ""; // Clear previous results
        
        if (movies.length === 0) {
            searchResults.innerHTML = "<p>No movies found.</p>";
            return;
        }

        movies.forEach(movie => {
            let movieCard = `
                <div class="movie-inner">
                    <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">
                    <h3>${movie.title}</h3>
                </div>
            `;
            searchResults.innerHTML += movieCard;
        });
    }


