import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("light_spotify_dataset.csv")
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
df['Year'] = df['Release Date'].dt.year

# Set Streamlit page title
st.title("Spotify Music Dataset Explorer")

# App description
st.write(
    "This app lets you explore a Spotify music dataset by filtering songs based on emotion and explicit content. "
    "It includes visualizations to show how features like popularity, danceability, and emotion relate to each other. "
    "Use the sidebar filters to customize your view and discover interesting patterns in the music."
)

# Sidebar: Emotion filter
emotion_filter = st.sidebar.multiselect(
    "Filter by Emotion",
    options=df['emotion'].unique(),
    default=df['emotion'].unique()
)

# Sidebar: Explicit content filter
explicit_filter = st.sidebar.selectbox(
    "Explicit content",
    options=["All", "Yes", "No"]
)

# Filter the data
filtered_df = df[df['emotion'].isin(emotion_filter)]
if explicit_filter != "All":
    filtered_df = filtered_df[filtered_df['Explicit'] == explicit_filter]

# Show filtered data
st.subheader("Filtered Data Sample")
st.dataframe(filtered_df.head())

# Plot: Popularity Distribution
st.subheader("Popularity Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df['Popularity'], kde=True, bins=30, color='skyblue', ax=ax1)
ax1.set_title("Popularity Distribution")
st.pyplot(fig1)

# Plot: Danceability vs Popularity
st.subheader("Danceability vs Popularity")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtered_df, x='Danceability', y='Popularity', alpha=0.6, ax=ax2)
ax2.set_title("Danceability vs Popularity")
st.pyplot(fig2)

# Plot: Popularity by Emotion
st.subheader("Popularity by Emotion")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x='emotion', y='Popularity', palette='pastel', ax=ax3)
ax3.set_title("Popularity by Emotion", fontsize=16)
ax3.set_xlabel("Emotion", fontsize=12)
ax3.set_ylabel("Popularity", fontsize=12)
ax3.tick_params(axis='x', rotation=30)
ax3.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig3)

# Plot: Popularity Over Time
st.subheader("Popularity Over Time")
fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df.sort_values('Year'), x='Year', y='Popularity', marker='o', ax=ax4, color='green')
ax4.set_title("Popularity Over Time", fontsize=16)
ax4.set_xlabel("Year", fontsize=12)
ax4.set_ylabel("Popularity", fontsize=12)
ax4.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig4)
