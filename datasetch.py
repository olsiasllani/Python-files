import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# Load dataset
movies_df = pd.read_csv(r"C:\Users\SH.D Ferizaj\Downloads\Top_Movies_2019_to_2025.csv")
# Sidebar filters
st.sidebar.title("Filters")

# Year filter
selected_year = st.sidebar.multiselect(
    "Select Year(s)",
    sorted(movies_df["Year"].unique()),
    default=sorted(movies_df["Year"].unique())
)

# Distributor filter
selected_distributor = st.sidebar.multiselect(
    "Select Distributor(s)",
    sorted(movies_df["Distributor"].unique()),
    default=sorted(movies_df["Distributor"].unique())
)

# Genre filter
all_genres = set()
for genres in movies_df['Genre']:
    for g in genres.split(','):
        all_genres.add(g.strip())
selected_genres = st.sidebar.multiselect(
    "Select Genre(s)",
    sorted(all_genres),
    default=sorted(all_genres)
)

# IMDb Rating filter
min_rating, max_rating = st.sidebar.slider(
    "Select IMDb Rating Range",
    float(movies_df['IMDb Rating'].min()),
    float(movies_df['IMDb Rating'].max()),
    (float(movies_df['IMDb Rating'].min()), float(movies_df['IMDb Rating'].max())),
    step=0.1
)

# Filter dataframe
filtered_df = movies_df[
    (movies_df["Year"].isin(selected_year)) &
    (movies_df["Distributor"].isin(selected_distributor)) &
    (movies_df["IMDb Rating"] >= min_rating) &
    (movies_df["IMDb Rating"] <= max_rating) &
    (movies_df["Genre"].apply(lambda x: any(g in x for g in selected_genres)))
]

# App title
st.title("Most Viewed Movies (2019–2025) Analysis")
st.write("This dashboard presents an analysis of popular movies between 2019 and 2025.")

# Summary statistics
st.subheader("Summary Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Movies", filtered_df.shape[0])
col2.metric("Unique Titles", filtered_df['Title'].nunique())
col3.metric("Average IMDb Rating", round(filtered_df['IMDb Rating'].mean(), 2))
col4.metric("Distributors", filtered_df['Distributor'].nunique())

# Dataset preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(10))

# Most common genres in filtered data
st.subheader("Most Common Genres")
genre_counter = Counter()
for genre_list in filtered_df['Genre']:
    genres = [g.strip() for g in genre_list.split(',')]
    genre_counter.update(genres)

genre_df = pd.DataFrame(genre_counter.items(), columns=["Genre", "Count"]).sort_values(by="Count", ascending=False)
fig_genre = px.bar(genre_df.head(10), x="Genre", y="Count", title="Top 10 Genres")
st.plotly_chart(fig_genre)

# Top 10 movies by rating
st.subheader("Top Rated Movies")
top_rated = filtered_df.sort_values(by="IMDb Rating", ascending=False).head(10)
fig_rating = px.bar(top_rated, x="Title", y="IMDb Rating", color="Distributor", title="Top 10 Rated Movies")
st.plotly_chart(fig_rating)
