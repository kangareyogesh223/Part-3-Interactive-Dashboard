import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="Spotify Tracks Explorer", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "spotify_tracks.csv")

path = ("data\spotify.csv")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0)
    df = df.dropna(subset=["artists", "track_name", "track_genre"])
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_deezer_artist_info(artist_name: str):
    """
    GET request to the Deezer public search API (no key required).
    Docs: https://developers.deezer.com/api/search
    Returns the first matching artist's basic profile info, or None on failure.
    """
    url = "https://api.deezer.com/search/artist"
    params = {"q": artist_name, "limit": 1}
    try:
        response = requests.get(url, params=params, timeout=8)
        response.raise_for_status()
        payload = response.json()
        results = payload.get("data", [])
        if results:
            return results[0]
    except requests.RequestException:
        return None
    return None


# Load data

df = load_data(path)

st.title("🎧 Spotify Tracks Explorer")
st.caption(
    "Explore ~114,000 Spotify tracks by genre, and pull a live artist "
    "profile from the Deezer API."
)

# Sidebar / interactive widgets
st.sidebar.header("Filters")

genres = sorted(df["track_genre"].unique())
selected_genre = st.sidebar.selectbox(
    "Choose a genre", options=genres, index=genres.index("pop") if "pop" in genres else 0
)

pop_min, pop_max = st.sidebar.slider(
    "Popularity range",
    min_value=0,
    max_value=100,
    value=(0, 100),
    help="Filter tracks by Spotify popularity score",
)

top_n = st.sidebar.slider("Number of top tracks to show", 5, 30, 10)

# Filtered data (drives every chart + the table below)

filtered = df[
    (df["track_genre"] == selected_genre)
    & (df["popularity"] >= pop_min)
    & (df["popularity"] <= pop_max)
].copy()

st.subheader(f"Genre: {selected_genre}  ·  {len(filtered):,} tracks match your filters")

if filtered.empty:
    st.warning("No tracks match the current filters. Try widening the popularity range.")
else:
    col1, col2 = st.columns(2)

    # Chart 1: Bar chart - most popular tracks in this genre
    with col1:
        top_tracks = (
            filtered.sort_values("popularity", ascending=False)
            .drop_duplicates(subset=["track_name"])
            .head(top_n)
        )
        fig_bar = px.bar(
            top_tracks,
            x="popularity",
            y="track_name",
            orientation="h",
            color="popularity",
            title=f"Top {top_n} Most Popular Tracks",
            labels={"popularity": "Popularity", "track_name": "Track"},
        )
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_bar, use_container_width=True)

    # Chart 2: Histogram - danceability distribution
    with col2:
        fig_hist = px.histogram(
            filtered,
            x="danceability",
            nbins=30,
            title="Danceability Distribution",
            labels={"danceability": "Danceability"},
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # Chart 3: Scatter - energy vs valence, colored by popularity
    fig_scatter = px.scatter(
        filtered,
        x="energy",
        y="valence",
        color="popularity",
        size="loudness" if (filtered["loudness"] > 0).any() else None,
        hover_data=["track_name", "artists"],
        title="Energy vs. Valence (mood map)",
        labels={"energy": "Energy", "valence": "Valence (musical positivity)"},
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Live data table reflecting current filter state
    st.subheader("Matching tracks")
    st.dataframe(
        filtered[
            [
                "track_name",
                "artists",
                "album_name",
                "popularity",
                "danceability",
                "energy",
                "valence",
                "tempo",
            ]
        ].reset_index(drop=True),
        use_container_width=True,
    )

    # Live external API integration (Deezer, GET, no key required)
    st.subheader("🔗 Live artist lookup (Deezer API)")
    st.caption(
        "Data below is fetched live from https://api.deezer.com/search/artist "
        "for the top artist in your current filter — not from the CSV."
    )

    top_artist_raw = top_tracks.iloc[0]["artists"]
    # the dataset separates collaborating artists with ';'; use the first one
    top_artist = top_artist_raw.split(";")[0].strip()

    with st.spinner(f"Looking up '{top_artist}' on Deezer..."):
        artist_info = fetch_deezer_artist_info(top_artist)

    if artist_info:
        c1, c2, c3 = st.columns(3)
        c1.metric("Artist", artist_info.get("name", "N/A"))
        c2.metric("Deezer fans", f"{artist_info.get('nb_fan', 0):,}")
        c3.metric("Albums on Deezer", artist_info.get("nb_album", "N/A"))
        if artist_info.get("picture_medium"):
            st.image(artist_info["picture_medium"], width=150)
        if artist_info.get("link"):
            st.markdown(f"[View artist on Deezer]({artist_info['link']})")
    else:
        st.info(f"No Deezer match found for '{top_artist}' right now.")

st.divider()
st.caption(
    "Dataset: Spotify tracks CSV bundled in this repo (data/spotify_tracks.csv). "
    "Live API: Deezer public Search API (GET, no key required)."
)
