
# 🎥 Cinemania

Cinemania is a dynamic and feature-rich movie discovery platform that allows users to explore, search, and discover movies effortlessly. Powered by the TMDB (The Movie Database) API, Cinemania provides real-time access to trending, popular, and upcoming movies, along with detailed information about each title. Whether you're a casual moviegoer or a cinephile, Cinemania is your go-to app for all things movies.

---

## 🌟 Features

### 🔍 **Search Movies**
- Search for movies by title with real-time results.
- Supports pagination for large search results.
- AJAX-powered search for seamless user experience.

### 🎬 **Movie Details**
- View detailed information about a movie, including:
  - Title, runtime, release year, and synopsis.
  - Cast and crew details.
  - Embedded trailers and clips from YouTube.
  - Recommendations for similar movies.

### 📊 **Trending and Popular Movies**
- Explore trending movies of the week.
- Browse popular, now-playing, upcoming, and top-rated movies.

### 🎭 **Genre and Language Filtering**
- Discover movies by genre with a dedicated genre page.
- Filter movies by their original language, including support for Nigerian languages like **Igbo**, **Yoruba**, and **Hausa**.

### 🎞️ **Trailers and Recommendations**
- Watch trailers directly on the platform.
- Get personalized recommendations for similar movies.

### 🌐 **Global Context**
- Access global data like genres and languages across all pages for consistent navigation and filtering.

### 📱 **Responsive Design**
- Fully responsive UI for a seamless experience on desktop, tablet, and mobile devices.

---

## 🛠️ Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **API Integration**: TMDB (The Movie Database) API
- **AJAX**: For dynamic content updates
- **Pagination**: Django's built-in paginator for efficient data handling

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 4.0+
- TMDB API Key (Sign up at [TMDB](https://www.themoviedb.org/) to get your API key)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cinemania.git
   cd cinemania
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a .env file in the project root and add the following:
     ```env
     TMDB_API_KEY=your_tmdb_api_key
     TMDB_API_BASE_URL=https://api.themoviedb.org/3/
     TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500/
     ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the app at `http://127.0.0.1:8000`.

---

## 📂 Project Structure

```
Cinemania/
├── movies/
│   ├── templates/
│   │   ├── movies/
│   │   │   ├── index.html
│   │   │   ├── movie_detail.html
│   │   │   ├── search_movies.html
│   │   │   ├── trending.html
│   │   │   ├── genre_movies.html
│   │   │   └── language_movies.html
│   ├── views.py
│   ├── urls.py
│   └── models.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── manage.py
└── requirements.txt
```

---

## 🌐 API Endpoints Used

- **Movie Details**: `/movie/{movie_id}`
- **Search Movies**: `/search/movie`
- **Trending Movies**: `/trending/movie/week`
- **Genres**: `/genre/movie/list`
- **Languages**: `/configuration/languages`
- **Recommendations**: `/movie/{movie_id}/recommendations`
- **Trailers**: `/movie/{movie_id}/videos`

---

## 📸 Screenshots

### Home Page
<img src="[image-url](https://github.com/user-attachments/assets/bc7e0d62-8714-4a1a-9a95-c51201678e1f)" alt="Homepage" width="300" style="border-radius: 8px; border: 2px solid #ccc;" />

### Movie Details
<img src="[image-url](https://github.com/user-attachments/assets/bc7e0d62-8714-4a1a-9a95-c51201678e1f)" alt="Movie Details" width="300" style="border-radius: 8px; border: 2px solid #ccc;" />

### Search Results
<img src="[image-url](https://github.com/user-attachments/assets/bc7e0d62-8714-4a1a-9a95-c51201678e1f)" alt="Search Results" width="300" style="border-radius: 8px; border: 2px solid #ccc;" />


---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 📧 Contact

For questions or feedback, feel free to reach out:

- **Email**: jonazkeez@gmail.com
- **GitHub**: [Cyberod](https://github.com/Cyberod)

---

