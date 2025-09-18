import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load sample metadata.csv
@st.cache_data
def load_data():
    return pd.read_csv("metadata.csv")

df = load_data()

# Basic cleaning
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

# Streamlit UI
st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers using sample metadata.csv")

# Year range filter
year_min, year_max = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("Select year range", year_min, year_max, (year_min, year_max))

# Filter data
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.write(f"Showing {len(filtered)} papers from {year_range[0]} to {year_range[1]}")

# Publications by Year
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_title("Publications by Year")
st.pyplot(fig)

# Top Journals
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
top_journals.plot(kind='bar', ax=ax)
ax.set_title("Top 10 Journals")
st.pyplot(fig)

# Show sample data
st.subheader("Sample Data")
st.write(filtered.head())