import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === LOAD DATA ===
day_df = pd.read_csv("day.csv")
day_df['date'] = pd.to_datetime(day_df['dteday'])

# === DICTIONARY OPTIONS ===
season_options = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_options = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}

# === SIDEBAR FILTER ===
st.sidebar.header("🔍 Filter Dashboard")

# Filter Tanggal
start_date = st.sidebar.date_input("Start Date", day_df['date'].min())
end_date = st.sidebar.date_input("End Date", day_df['date'].max())

# Filter Musim
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim",
    options=list(season_options.keys()),
    format_func=lambda x: season_options[x],
    default=list(season_options.keys())
)

# Filter Cuaca
selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=list(weather_options.keys()),
    format_func=lambda x: weather_options[x],
    default=list(weather_options.keys())
)

# Pilih Metric
metric = st.sidebar.radio(
    "Pilih Jenis Data",
    options=['total_count', 'registered', 'casual'],
    format_func=lambda x: f"Total ({x})" if x == "total_count" else x.capitalize()
)

# === APPLY FILTER ===
filtered_df = day_df[
    (day_df['date'] >= pd.to_datetime(start_date)) &
    (day_df['date'] <= pd.to_datetime(end_date)) &
    (day_df['season'].isin(selected_seasons)) &
    (day_df['weather_situation'].isin(selected_weather))
]

# === MAIN DASHBOARD ===
st.title("🚲 Bike Sharing Dashboard")

# METRIC CARD
st.metric(label=f"Total Penyewaan ({metric.capitalize()})", value=filtered_df[metric].sum())

# === VISUALISASI 1: Trend Harian ===
st.markdown("### 📅 Trend Penyewaan Harian")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x='date', y=metric, marker="o", ax=ax)
plt.title(f"Trend {metric.capitalize()} Harian")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

# === VISUALISASI 2: Distribusi Berdasarkan Musim ===
st.markdown("### ☀️ Distribusi Penyewaan Berdasarkan Musim")
fig2, ax2 = plt.subplots(figsize=(8,5))
sns.boxplot(data=filtered_df, x='season', y=metric, palette="Set3", ax=ax2)
ax2.set_xticklabels([season_options[x] for x in filtered_df['season'].unique()])
plt.grid(True)
st.pyplot(fig2)

# === DOWNLOAD DATA ===
st.markdown("### 📥 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Data as CSV", data=csv, file_name='filtered_bike_share.csv', mime='text/csv')
