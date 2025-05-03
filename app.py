import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("light_spotify_dataset.csv")
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
df['Year'] = df['Release Date'].dt.year

# App title and description
st.title("Spotify Music Dataset Explorer")

st.write(
    "This app lets you explore a Spotify music dataset by filtering songs based on emotion and explicit content. "
    "It also includes a simulated view of Spotify's user growth over time."
)

# Sidebar filters
emotion_filter = st.sidebar.multiselect(
    "Filter by Emotion",
    options=df['emotion'].dropna().unique(),
    default=df['emotion'].dropna().unique()
)

explicit_filter = st.sidebar.selectbox(
    "Explicit content",
    options=["All", "Yes", "No"]
)

# Apply filters
filtered_df = df[df['emotion'].isin(emotion_filter)]
if explicit_filter != "All":
    filtered_df = filtered_df[filtered_df['Explicit'] == explicit_filter]

# Show filtered data
st.subheader("Filtered Data Sample")
st.dataframe(filtered_df.head())

# Popularity Distribution
st.subheader("Popularity Distribution")
fig1 = px.histogram(
    filtered_df,
    x="Popularity",
    nbins=30,
    title="Distribution of Song Popularity",
    color_discrete_sequence=["skyblue"]
)
fig1.update_layout(bargap=0.1)
st.plotly_chart(fig1)

# Danceability vs Popularity
st.subheader("Danceability vs Popularity")
fig2 = px.scatter(
    filtered_df,
    x="Danceability",
    y="Popularity",
    color="emotion",
    hover_data=["song", "artist"],
    title="Danceability vs Popularity"
)
st.plotly_chart(fig2)

# Popularity by Emotion
st.subheader("Popularity by Emotion")
fig3 = px.box(
    filtered_df,
    x="emotion",
    y="Popularity",
    color="emotion",
    title="Popularity by Emotion",
    points="all"
)
fig3.update_layout(
    xaxis_title="Emotion",
    yaxis_title="Popularity",
    showlegend=False
)
st.plotly_chart(fig3)

# Simulated Spotify User Growth
st.subheader("Spotify Global Users Over Time (Simulated)")

# Fake data (realistic estimate from historical public numbers)
user_data = pd.DataFrame({
    "Year": list(range(2010, 2025)),
    "Spotify_Users_Millions": [
        0, 10, 15, 24, 38, 60, 89, 140, 180, 232,
        286, 345, 406, 456, 515
    ]
})

fig4 = px.line(
    user_data,
    x="Year",
    y="Spotify_Users_Millions",
    title="Spotify Global User Growth Over Time",
    markers=True
)
fig4.update_layout(
    xaxis_title="Year",
    yaxis_title="Users (Millions)",
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=10, label="10y", step="year", stepmode="backward"),
                dict(step="all", label="All")
            ])
        ),
        rangeslider=dict(visible=True),
        type="linear"
    )
)
st.plotly_chart(fig4)
