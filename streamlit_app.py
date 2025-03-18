import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data dan Rename agar konsisten
day_df = pd.read_csv("day.csv")

# Rename agar konsisten
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
day_df['date'] = pd.to_datetime(day_df['date'])

# === CLEANING: Remove Outlier ===
# Pilih kolom numerik
numeric_cols = ['casual', 'registered', 'total_count', 'temp', 'atemp', 'humidity', 'windspeed']

# Deteksi dan hapus outlier (IQR method)
for col in numeric_cols:
    Q1 = day_df[col].quantile(0.25)
    Q3 = day_df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    day_df = day_df[(day_df[col] >= lower_bound) & (day_df[col] <= upper_bound)]

# Dataset sudah bersih & siap digunakan

# === DASHBOARD (sidebar + tab) ===
st.sidebar.header("🔍 Filter Dashboard")
start_date = st.sidebar.date_input("Start Date", day_df['date'].min())
end_date = st.sidebar.date_input("End Date", day_df['date'].max())
season_options = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_options = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}

selected_seasons = st.sidebar.multiselect("Pilih Musim", options=list(season_options.keys()), format_func=lambda x: season_options[x], default=list(season_options.keys()))
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=list(weather_options.keys()), format_func=lambda x: weather_options[x], default=list(weather_options.keys()))
metric = st.sidebar.radio("Pilih Jenis Data", options=['total_count', 'registered', 'casual'], format_func=lambda x: f"Total ({x})" if x == "total_count" else x.capitalize())

filtered_df = day_df[
    (day_df['date'] >= pd.to_datetime(start_date)) &
    (day_df['date'] <= pd.to_datetime(end_date)) &
    (day_df['season'].isin(selected_seasons)) &
    (day_df['weather_situation'].isin(selected_weather))
]
# ==== LAYOUT MULTI-TAB ====
tab1, tab2 = st.tabs(["📊 Interactive Dashboard", "📝 Business Analysis"])

# ==== TAB 1: DASHBOARD INTERAKTIF ====
with tab1:
    st.title("🚲 Bike Sharing Dashboard")
    st.metric(label=f"Total Penyewaan ({metric.capitalize()})", value=filtered_df[metric].sum())
    
    # Lineplot Trend
    st.markdown("### 📅 Trend Penyewaan Harian")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=filtered_df, x='date', y=metric, marker="o", ax=ax)
    plt.title(f"Trend {metric.capitalize()} Harian")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)
    
    # Boxplot Musim
    st.markdown("### ☀️ Distribusi Penyewaan Berdasarkan Musim")
    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.boxplot(data=filtered_df, x='season', y=metric, palette="Set3", ax=ax2)
    ax2.set_xticklabels([season_options[x] for x in filtered_df['season'].unique()])
    plt.grid(True)
    st.pyplot(fig2)

# ==== TAB 2: BUSINESS ANALYSIS ====
with tab2:
    st.title("📌 Business Analysis & Insights")
    
    # Visualisasi distribusi total_count
    st.markdown("### Distribusi Total Penyewaan Sepeda")
    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.histplot(day_df['total_count'], bins=30, kde=True, color="skyblue", ax=ax3)
    plt.grid(True)
    st.pyplot(fig3)
    
    # Pola per jam (rush hour)
    st.markdown("### Pola Penyewaan Berdasarkan Jam (Rush Hour)")
    hour_df = pd.read_csv("hour.csv")
    hour_df.rename(columns={'hr': 'hour', 'cnt': 'total_count'}, inplace=True)
    avg_rent_by_hour = hour_df.groupby('hour')['total_count'].mean()
    fig4, ax4 = plt.subplots(figsize=(8,5))
    sns.lineplot(x=avg_rent_by_hour.index, y=avg_rent_by_hour.values, marker="o", ax=ax4)
    plt.grid(True)
    st.pyplot(fig4)
    
    # Cuaca vs Penyewaan
    st.markdown("### Pengaruh Cuaca terhadap Penyewaan Sepeda")
    fig5, ax5 = plt.subplots(figsize=(8,5))
    sns.boxplot(x='weather_situation', y='total_count', data=day_df, palette="coolwarm", ax=ax5)
    ax5.set_xticklabels([weather_options[x] for x in day_df['weather_situation'].unique()])
    plt.grid(True)
    st.pyplot(fig5)
    
    # Musim vs Penyewaan
    st.markdown("### Pengaruh Musim terhadap Penyewaan Sepeda")
    fig6, ax6 = plt.subplots(figsize=(8,5))
    sns.boxplot(x='season', y='total_count', data=day_df, palette="viridis", ax=ax6)
    ax6.set_xticklabels([season_options[x] for x in day_df['season'].unique()])
    plt.grid(True)
    st.pyplot(fig6)
