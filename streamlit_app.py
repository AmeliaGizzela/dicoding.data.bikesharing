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


# CLEANING day_df
# =======================

# 1. Drop kolom yang tidak digunakan
# Drop kolom jika ada
# if 'instant' in day_df.columns:
#     day_df.drop(columns=['instant'], inplace=True)
# if 'instant' in hour_df.columns:
#     hour_df.drop(columns=['instant'], inplace=True)


# 2. Rename kolom agar lebih deskriptif
day_df.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'holiday': 'is_holiday',
    'weekday': 'weekday',
    'workingday': 'is_workingday',
    'weathersit': 'weather_situation',
    'hum': 'humidity',
    'cnt': 'total_count'
}, inplace=True)

# 3. Convert tipe data
day_df['date'] = pd.to_datetime(day_df['date'])
categorical_cols_day = ['season', 'year', 'month', 'weekday', 'is_holiday', 'is_workingday', 'weather_situation']
day_df[categorical_cols_day] = day_df[categorical_cols_day].astype('category')

hour_df.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'hr': 'hour',
    'holiday': 'is_holiday',
    'weekday': 'weekday',
    'workingday': 'is_workingday',
    'weathersit': 'weather_situation',
    'hum': 'humidity',
    'cnt': 'total_count'
}, inplace=True)

# 3. Convert tipe data
hour_df['date'] = pd.to_datetime(hour_df['date'])
categorical_cols_hour = ['season', 'year', 'month', 'hour', 'weekday', 'is_holiday', 'is_workingday', 'weather_situation']
hour_df[categorical_cols_hour] = hour_df[categorical_cols_hour].astype('category')


#Sidebar
# === DICTIONARY OPTIONS ===
season_options = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_options = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}

# === SIDEBAR FILTER ===
st.sidebar.header("🔍 Filter Dashboard")

# Filter Tanggal
min_date = min(day_df['date'].min(), hour_df['date'].min())
max_date = max(day_df['date'].max(), hour_df['date'].max())

start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

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
    options=['cnt', 'registered', 'casual'],
    format_func=lambda x: f"Total ({x})" if x == "cnt" else x.capitalize()
)

# === APPLY FILTER ke day_df ===
filtered_day_df = day_df[
    (day_df['date'] >= pd.to_datetime(start_date)) &
    (day_df['date'] <= pd.to_datetime(end_date)) &
    (day_df['season'].isin(selected_seasons)) &
    (day_df['weathersit'].isin(selected_weather))
]

# === APPLY FILTER ke hour_df ===
filtered_hour_df = hour_df[
    (hour_df['date'] >= pd.to_datetime(start_date)) &
    (hour_df['date'] <= pd.to_datetime(end_date)) &
    (hour_df['season'].isin(selected_seasons)) &
    (hour_df['weathersit'].isin(selected_weather))
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
