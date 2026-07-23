# Spotify Tracks Explorer

An interactive Streamlit dashboard for exploring a dataset of ~114,000 Spotify
tracks by genre, popularity, and audio features (danceability, energy,
valence, etc.), with a live lookup against the Deezer public API.

**Live app:** https://YOUR-APP-NAME.streamlit.app  ← replace this after you deploy (see steps below)

## What's in this repo

- `app.py` – the Streamlit dashboard
- `requirements.txt` – Python dependencies
- `data/spotify_tracks.csv` – the bundled dataset (self-contained, no external file dependency)

## Features

- **Interactive widgets** (sidebar): a genre `selectbox`, a popularity range
  `slider`, and a "top N tracks" `slider`. Changing any of these re-filters
  the whole page.
- **3 charts that update with the widgets:**
  1. Horizontal bar chart – most popular tracks in the selected genre
  2. Histogram – distribution of danceability for the filtered tracks
  3. Scatter plot – energy vs. valence ("mood map"), colored by popularity
- **Live data table** (`st.dataframe`) showing every track that matches the
  current filters.
- **Live external API call** – see below.

## External API integration

- **Endpoint:** `https://api.deezer.com/search/artist?q={artist_name}&limit=1`
  (Deezer's public Search API — free, no API key or signup required)
- **HTTP method:** `GET`
- **What it returns:** Given an artist name, the endpoint returns a JSON
  object with an array of matching artists on Deezer, each including fields
  like `name`, `nb_fan` (number of Deezer fans), `nb_album` (number of
  albums), a `picture_medium` image URL, and a `link` to the artist's Deezer
  page. My app takes the top-charting artist from whatever genre/filter the
  user currently has selected, sends a live GET request to this endpoint,
  and displays the artist's name, fan count, album count, photo, and profile
  link on the page. This is a real-time network call made every time the
  filter selection changes (results are cached for an hour per artist to
  avoid hammering the API), not data read from the CSV.
- **Fields displayed:** `name`, `nb_fan`, `nb_album`, `picture_medium`, `link`

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Deploying to Streamlit Community Cloud (free)

1. Create a new **public** GitHub repository and push these three items to
   its root: `app.py`, `requirements.txt`, `README.md`, and the `data/`
   folder.
   ```bash
   git init
   git add .
   git commit -m "Spotify tracks dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   your GitHub account.
3. Click **"New app"**, pick your repository, branch `main`, and set the
   main file path to `app.py`.
4. Click **Deploy**. Streamlit Community Cloud will install
   `requirements.txt` automatically and give you a public URL like
   `https://<your-app-name>.streamlit.app`.
5. Copy that URL into the **Live app** line at the top of this README and
   commit the change.

No payment method or paid plan is required — Streamlit Community Cloud's
free tier is sufficient for this app.

## Dataset

The dataset (`data/spotify_tracks.csv`) contains ~114,000 Spotify tracks
across 114 genres, with columns such as `track_name`, `artists`,
`popularity`, `danceability`, `energy`, `valence`, `tempo`, and
`track_genre`. It is bundled directly in this repository so the app is
fully self-contained and requires no external download.
