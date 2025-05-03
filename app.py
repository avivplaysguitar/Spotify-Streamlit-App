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
    "Use the sidebar to filter the data and view interactive charts that show trends and comparisons in song popularity."
)

# Sidebar filters
emotion_filter = st.sidebar.multiselect(
    "Filter by Emotion",
    options=df['emotion'].unique(),
    default=df['emotion'].unique()
)

explicit_filter = st.sidebar.selectbox(
    "Explicit content",
    options=["All", "Yes", "No"]
)

# Filter data
filtered_df = df[df['emotion'].isin(emotion_filter)]
if explicit_filter != "All":
    filtered_df = filtered_df[filtered_df['Explicit'] == explicit_filter]

# Show filtered data
st.subheader("Filtered Data Sample")
st.dataframe(filtered_df.head())

# Chart: Popularity Distribution
st.subheader("Popularity Distribution")
fig1 = px.histogram(
    filtered_df,
    x="Popularity",
    nbins=30,
    title="Popularity Distribution",
    color_discrete_sequence=["skyblue"]
)
fig1.update_layout(bargap=0.1)
st.plotly_chart(fig1)

# Chart: Danceability vs Popularity
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

# Chart: Popularity by Emotion (Boxplot)
st.subheader("Popularity by Emotion")
fig3 = px.box(
    filtered_df,
    x="emotion",
    y="Popularity",
    color="emotion",
    title="Popularity by Emotion",
    points="all"  # show individual points
)
fig3.update_layout(xaxis_title="Emotion", yaxis_title="Popularity", showlegend=False)
st.plotly_chart(fig3)

# Chart: Popularity Over Time
st.subheader("Popularity Over Time")
fig4 = px.line(
    filtered_df.groupby("Year")["Popularity"].mean().reset_index(),
    x="Year",
    y="Popularity",
    title="Average Popularity Over Time",
    markers=True
)
fig4.update_traces(line=dict(color="green"))
st.plotly_chart(fig4)
