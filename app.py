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
    "Use the sidebar to customize your view and discover trends in popularity, emotion, and danceability."
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

# Popularity Over Time (stock-style with range slider)
st.subheader("Popularity Over Time")
pop_by_year = (
    filtered_df.dropna(subset=["Year"])
    .groupby("Year")["Popularity"]
    .mean()
    .reset_index()
    .sort_values("Year")
)

if not pop_by_year.empty:
    fig4 = px.line(
        pop_by_year,
        x="Year",
        y="Popularity",
        title="Average Popularity Over Time (Stock Chart Style)",
        markers=True
    )
    fig4.update_layout(
        xaxis_title="Year",
        yaxis_title="Avg Popularity",
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
else:
    st.info("No popularity data available for the selected filters.")
