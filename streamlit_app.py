import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
day = pd.read_csv('day.csv')
hour = pd.read_csv('hour.csv')

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Dashboard ini menyajikan analisis data penyewaan sepeda berdasarkan dataset `day.csv` dan `hour.csv`.")

st.sidebar.header("Filter Data")
# Filter Season
season = st.sidebar.multiselect(
    "Pilih Season",
    options=day['season'].unique(),
    default=day['season'].unique()
)

# Filter Weather
weather = st.sidebar.multiselect(
    "Pilih Cuaca",
    options=day['weathersit'].unique(),
    default=day['weathersit'].unique()
)

# Filter Rentang Tanggal
date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    [pd.to_datetime(day['dteday']).min(), pd.to_datetime(day['dteday']).max()]
)

# Apply Filter
day_filtered = day[
    (day['season'].isin(season)) &
    (day['weathersit'].isin(weather)) &
    (pd.to_datetime(day['dteday']) >= pd.to_datetime(date_range[0])) &
    (pd.to_datetime(day['dteday']) <= pd.to_datetime(date_range[1]))
]

st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Penyewaan", f"{day_filtered['cnt'].sum():,}")

with col2:
    st.metric("Rata-rata Penyewaan Harian", f"{day_filtered['cnt'].mean():.2f}")

with col3:
    st.metric("Total Pengguna Casual", f"{day_filtered['casual'].sum():,}")

st.subheader("⏰ Waktu Puncak Penyewaan")

hour['dteday'] = pd.to_datetime(hour['dteday'])
hour_filtered = hour[
    (hour['season'].isin(season)) &
    (hour['weathersit'].isin(weather)) &
    (hour['dteday'] >= pd.to_datetime(date_range[0])) &
    (hour['dteday'] <= pd.to_datetime(date_range[1]))
]

peak_hours = hour_filtered.groupby('hr')['cnt'].sum()

fig, ax = plt.subplots()
sns.lineplot(x=peak_hours.index, y=peak_hours.values, ax=ax)
ax.set_title("Penyewaan Sepeda per Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan")

weather_mapping = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}
day_filtered['weather_label'] = day_filtered['weathersit'].map(weather_mapping)

fig, ax = plt.subplots()
sns.boxplot(x='weather_label', y='cnt', data=day_filtered, ax=ax)
ax.set_title("Distribusi Penyewaan Berdasarkan Cuaca")
st.pyplot(fig)

st.subheader("🍂 Pengaruh Musim terhadap Penyewaan")

season_mapping = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'}
day_filtered['season_label'] = day_filtered['season'].map(season_mapping)

fig, ax = plt.subplots()
sns.barplot(x='season_label', y='cnt', data=day_filtered, estimator=sum, ax=ax)
ax.set_title("Total Penyewaan Berdasarkan Musim")
st.pyplot(fig)
