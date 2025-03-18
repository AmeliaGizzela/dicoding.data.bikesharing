import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# CLEANING day_df
# =======================

# 1. Drop kolom yang tidak digunakan
# Drop kolom jika ada
if 'instant' in day_df.columns:
    day_df.drop(columns=['instant'], inplace=True)
if 'instant' in hour_df.columns:
    hour_df.drop(columns=['instant'], inplace=True)


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
    options=['total_count', 'registered', 'casual'],
    format_func=lambda x: f"Total ({x})" if x == "total_count" else x.capitalize()
)

# === APPLY FILTER ke day_df ===
filtered_day_df = day_df[
    (day_df['date'] >= pd.to_datetime(start_date)) &
    (day_df['date'] <= pd.to_datetime(end_date)) &
    (day_df['season'].isin(selected_seasons)) &
    (day_df['weather_situation'].isin(selected_weather))
]

# === APPLY FILTER ke hour_df ===
filtered_hour_df = hour_df[
    (hour_df['date'] >= pd.to_datetime(start_date)) &
    (hour_df['date'] <= pd.to_datetime(end_date)) &
    (hour_df['season'].isin(selected_seasons)) &
    (hour_df['weather_situation'].isin(selected_weather))
]

# ==== LAYOUT MULTI-TAB ====
tab1, tab2 = st.tabs(["📊 Dashboard", "📝 Analisis data lanjutan"])

# ==== TAB 1: ====
with tab1:
    st.title("🚲 Bike Sharing Dashboard")
    st.markdown("Dashboard ini menyajikan analisis data penyewaan sepeda berdasarkan dataset `day.csv` dan `hour.csv`.")    
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    # === METRICS ===
    with col1:
        st.metric("Total Penyewaan", f"{filtered_day_df['total_count'].sum():,}")
    
    with col2:
        st.metric("Rata-rata Penyewaan Harian", f"{filtered_day_df['total_count'].mean():.2f}")
    
    with col3:
        st.metric("Total Pengguna Casual", f"{filtered_day_df['casual'].sum():,}")
    
    # === WAKTU PUNCAK PENYEWAAN ===
    st.subheader("⏰ Waktu Puncak Penyewaan")
    
    hour_df['date'] = pd.to_datetime(hour_df['date'])  # sudah rename 'dteday' ke 'date'
    
    hour_filtered = hour_df[
        (hour_df['season'].isin(selected_seasons)) &
        (hour_df['weather_situation'].isin(selected_weather)) &
        (hour_df['date'] >= pd.to_datetime(start_date)) &
        (hour_df['date'] <= pd.to_datetime(end_date))
    ]
    
    peak_hours = hour_filtered.groupby('hour')['total_count'].sum()
    
    fig, ax = plt.subplots()
    sns.lineplot(x=peak_hours.index, y=peak_hours.values, ax=ax)
    ax.set_title("Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Total Penyewaan")
    st.pyplot(fig)
    
    # === PENGARUH CUACA ===
    st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan")
    
    weather_mapping = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
    filtered_day_df['weather_label'] = filtered_day_df['weather_situation'].map(weather_mapping)
    
    fig, ax = plt.subplots()
    sns.boxplot(x='weather_label', y='total_count', data=filtered_day_df, ax=ax)
    ax.set_title("Distribusi Penyewaan Berdasarkan Cuaca")
    st.pyplot(fig)
    
    # === PENGARUH MUSIM ===
    st.subheader("🍂 Pengaruh Musim terhadap Penyewaan")
    
    season_mapping = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'}
    filtered_day_df['season_label'] = filtered_day_df['season'].map(season_mapping)
    
    fig, ax = plt.subplots()
    sns.barplot(x='season_label', y='total_count', data=filtered_day_df, estimator=sum, ax=ax)
    ax.set_title("Total Penyewaan Berdasarkan Musim")
    st.pyplot(fig)


# ==== TAB 2: BUSINESS ANALYSIS ====
with tab2:
    st.title("📌 Business Analysis & Insights")
    
    # ===== SEGMENTASI WAKTU =====
    st.subheader("⏰ Segmentasi Waktu")

    def time_segment(hour):
        if 5 <= hour <= 10:
            return 'Pagi'
        elif 11 <= hour <= 15:
            return 'Siang'
        elif 16 <= hour <= 20:
            return 'Sore'
        else:
            return 'Malam'

    filtered_hour_df['time_segment'] = filtered_hour_df['hour'].astype(int).apply(time_segment)

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='time_segment', y='total_count', data=hour_df, palette='Set2', ax=ax1)
    ax1.set_title("Distribusi Penyewaan Berdasarkan Segmentasi Waktu")
    ax1.set_ylabel("Jumlah Penyewaan")
    ax1.grid(True)
    st.pyplot(fig1)

    # ===== BINNING TOTAL COUNT =====
    st.subheader("📊 Kategori Penggunaan Sepeda")

    Q1 = hour_df['total_count'].quantile(0.25)
    Q3 = hour_df['total_count'].quantile(0.75)

    def usage_category(count):
        if count <= Q1:
            return 'Low Usage'
        elif count >= Q3:
            return 'High Usage'
        else:
            return 'Medium Usage'

    filtered_hour_df['usage_category'] = filtered_hour_df['total_count'].apply(usage_category)

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    # === CROSSTAB TIME SEGMENT ===
    st.subheader("🕒 Proporsi Usage Category per Waktu")

    ct_time = pd.crosstab(
    filtered_hour_df['time_segment'],
    filtered_hour_df['usage_category'],
    normalize='index') * 100


    fig3, ax3 = plt.subplots(figsize=(8, 5))
    ct_time.plot(kind='bar', stacked=True, colormap='Set2', ax=ax3)
    ax3.set_title("Proporsi Usage Category per Waktu")
    ax3.set_ylabel("% Usage")
    ax3.legend(title="Usage Category")
    ax3.grid(True)
    st.pyplot(fig3)

    # === CROSSTAB WEATHER ===
    st.subheader("🌦️ Proporsi Usage Category per Kondisi Cuaca")

    ct_weather = pd.crosstab(
    filtered_hour_df['weather_situation'],
    filtered_hour_df['usage_category'],
    normalize='index') * 100

    fig4, ax4 = plt.subplots(figsize=(8, 5))
    ct_weather.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax4)
    ax4.set_title("Proporsi Usage Category per Kondisi Cuaca")
    ax4.set_ylabel("% Usage")
    ax4.legend(title="Usage Category")
    ax4.grid(True)
    st.pyplot(fig4)
    sns.countplot(x='usage_category', data=hour_df, palette='Set3', ax=ax2)
    ax2.set_title("Distribusi Kategori Penggunaan Sepeda")
    ax2.set_ylabel("Jumlah Observasi")
    ax2.grid(True)
    st.pyplot(fig2)
