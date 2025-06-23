import streamlit as st
import requests

st.set_page_config(page_title="🎬 Movie Tracker", layout="wide")

API_URL = "http://localhost:8000"

st.title("🎬 My Movie Tracker")

# Sidebar filters
st.sidebar.header("Filter Movies")

# Genre filter
genres = ["All", "Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Thriller", "Musical", "Other"]
selected_genre = st.sidebar.selectbox("Select Genre", genres)

# Minimum rating filter
selected_rating = st.sidebar.slider("Minimum Rating", 1, 5, 1)

# Release year range filter
min_year = 1900
max_year = 2100
selected_year_range = st.sidebar.slider("Release Year Range", min_year, max_year, (2000, 2025))

# Fetch movies from backend
movies = requests.get(f"{API_URL}/movies/").json()

# Apply filters
if selected_genre != "All":
    movies = [m for m in movies if m['genre'] == selected_genre]

movies = [m for m in movies if m['rating'] >= selected_rating]

movies = [m for m in movies if selected_year_range[0] <= m['year'] <= selected_year_range[1]]

# Main area: add movie form
st.header("➕ Add a New Movie")

with st.form("add_movie"):
    title = st.text_input("Movie Title")
    director = st.text_input("Director")
    year = st.number_input("Release Year", min_value=min_year, max_value=max_year, value=2023)
    genre = st.selectbox("Genre", genres[1:])  # exclude 'All'
    rating = st.slider("Rating (1-5)", 1, 5)
    submitted = st.form_submit_button("Add Movie")

    if submitted:
        res = requests.post(f"{API_URL}/movies/", json={
            "title": title,
            "director": director,
            "year": year,
            "genre": genre,
            "rating": rating
        })
        if res.status_code == 200:
            st.success("✅ Movie added!")
        else:
            st.error(f"❌ Error: {res.json().get('detail', 'Unknown error')}")

st.divider()

# Display filtered movies
st.header("📽️ Movie List")

if not movies:
    st.info("No movies match the filters.")
else:
    for movie in movies:
        stars = "⭐" * movie['rating']
        st.markdown(f"""
        - **{movie['title']}** ({movie['year']})  
        🎬 Directed by: *{movie['director']}*  
        🎭 Genre: `{movie['genre']}`  
        ⭐ Rating: {stars}
        """)
