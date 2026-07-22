import pandas as pd
import streamlit as st
import requests
import plotly.express as px

df= pd.read_csv(r"C:\Users\Yogesh kangare\Documents\Capstone project\Part-3-Interactive-Dashboard\dataset.csv")

genre = st.selectbox(
    "Select Genre",
    ["Pop", "Rock", "Hip-Hop"]
)

popularity = st.slider(
    "Minimum Popularity",
    0,
    100,
    50
)

explicit = st.checkbox("Explicit Songs Only")

filtered = df[df["track_genre"] == genre]

filtered = filtered[
    filtered["popularity"] >= popularity
]

if explicit:
    filtered = filtered[
        filtered["explicit"] == True
    ]


st.metric(
    "Songs",
    len(filtered)
)

## Chart
#Top Artists

filtered_df = df[df["track_genre"] == genre]

filtered_df = filtered_df[
    filtered_df["popularity"] >= popularity
]

if explicit:
    filtered_df = filtered_df[
        filtered_df["explicit"] == True
    ]

artist_popularity = (
    filtered_df
    .groupby("artists")["popularity"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


#X-axis: Artist names
#Y-axis: Average popularity score

fig1 = px.bar(
    artist_popularity,
    x="artists",
    y="popularity",
    title="Top 10 Artists by Average Popularity",
    color="popularity",
    text="popularity"
)

fig1.update_layout(
    xaxis_title="Artist",
    yaxis_title="Average Popularity"
)

st.plotly_chart(fig1, use_container_width=True)

#Danceability vs Energy (Scatter Plot)

#Each dot represents one song
#X-axis: Danceability
#Y-axis: Energy
#Color: Popularity

fig2 = px.scatter(
    filtered_df,
    x="danceability",
    y="energy",
    color="popularity",
    hover_data=[
        "track_name",
        "artists"
    ],
    title="Danceability vs Energy"
)

fig2.update_layout(
    xaxis_title="Danceability",
    yaxis_title="Energy"
)

st.plotly_chart(fig2, use_container_width=True)

#Pie Chart- Top 10 Genres Distribution

genre_count = (
    df["track_genre"]
    .value_counts()
    .head(10)
    .reset_index()
)

genre_count.columns = [
    "Genre",
    "Songs"
]

fig3 = px.pie(
    genre_count,
    names="Genre",
    values="Songs",
    title="Top 10 Genres Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

#Display Live Data Table

st.subheader("Filtered Dataset")
st.dataframe(filtered_df)

#Dashboard Layout

st.title("🎵 Spotify Music Analytics Dashboard")

st.subheader("📊 Chart 1")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📈 Chart 2")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🥧 Chart 3")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📋 Live Data Table")
st.dataframe(filtered_df)


url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"


import requests
import streamlit as st

st.subheader("🌦 Live Weather Information")

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 18.5204,
    "longitude": 73.8567,
    "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
}

try:
    response = requests.get(url, params=params)

    if response.status_code == 200:

        weather = response.json()

        temperature = weather["current"]["temperature_2m"]
        wind_speed = weather["current"]["wind_speed_10m"]
        humidity = weather["current"]["relative_humidity_2m"]

        col1, col2, col3 = st.columns(3)

        col1.metric("🌡 Temperature", f"{temperature} °C")
        col2.metric("💨 Wind Speed", f"{wind_speed} km/h")
        col3.metric("💧 Humidity", f"{humidity}%")

    else:
        st.error("Weather API returned an error.")

except Exception as e:
    st.error(f"API Error: {e}")


