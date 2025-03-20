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
# 4. Cek missing values
print("Missing values in day_df:\n", day_df.isnull().sum())

# =======================
# CLEANING hour_df
# =======================

# 2. Rename kolom agar lebih deskriptif
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

#====CLEANING DATA OUTLIER====

# Pilih hanya kolom numerik
numeric_cols_day = day_df.select_dtypes(include=['int64', 'float64']).columns
numeric_cols_hour = hour_df.select_dtypes(include=['int64', 'float64']).columns

# 1. Preprocessing & Outlier Handling
import numpy as np

# Backup dataset sebelum treatment
day_df_original = day_df.copy()

# Deteksi outlier (IQR method) dan buat mask outlier
outlier_mask = pd.DataFrame(False, index=day_df.index, columns=numeric_cols_day)

for col in numeric_cols_day:
    Q1 = day_df[col].quantile(0.25)
    Q3 = day_df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outlier_mask[col] = (day_df[col] < lower_bound) | (day_df[col] > upper_bound)

# Gabungkan mask dari semua kolom -> True jika baris outlier di kolom manapun
rows_to_drop = outlier_mask.any(axis=1)

# Drop baris-baris yang memiliki outlier
day_df_cleaned = day_df[~rows_to_drop]

# Info berapa banyak yang terhapus
print(f'Total baris sebelum: {len(day_df)}')
print(f'Total baris setelah: {len(day_df_cleaned)}')
print(f'Baris yang dihapus karena outlier: {rows_to_drop.sum()}')

# 2. Visualisasi distribusi sebelum & sesudah treatment
fig, axes = plt.subplots(len(numeric_cols_day), 2, figsize=(14, len(numeric_cols_day) * 3))
for idx, col in enumerate(numeric_cols_day):
    sns.boxplot(data=day_df_original, y=col, ax=axes[idx, 0])
    axes[idx, 0].set_title(f'{col} - Before Outlier Removal')
    sns.boxplot(data=day_df_cleaned, y=col, ax=axes[idx, 1])
    axes[idx, 1].set_title(f'{col} - After Outlier Removal')
plt.tight_layout()
plt.show()

# 1. Preprocessing & Outlier Handling
import numpy as np

# Backup dataset sebelum treatment
hour_df_original = hour_df.copy()

# Deteksi outlier (IQR method) dan buat mask outlier
outlier_mask = pd.DataFrame(False, index=hour_df.index, columns=numeric_cols_hour)

for col in numeric_cols_hour:
    Q1 = hour_df[col].quantile(0.25)
    Q3 = hour_df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outlier_mask[col] = (hour_df[col] < lower_bound) | (hour_df[col] > upper_bound)

# Gabungkan mask dari semua kolom -> True jika baris outlier di kolom manapun
rows_to_drop = outlier_mask.any(axis=1)

# Drop baris-baris yang memiliki outlier
hour_df_cleaned = hour_df[~rows_to_drop]

# Info berapa banyak yang terhapus
print(f'Total baris sebelum: {len(hour_df)}')
print(f'Total baris setelah: {len(hour_df_cleaned)}')
print(f'Baris yang dihapus karena outlier: {rows_to_drop.sum()}')

# 2. Visualisasi distribusi sebelum & sesudah treatment
fig, axes = plt.subplots(len(numeric_cols_hour), 2, figsize=(14, len(numeric_cols_hour) * 3))
for idx, col in enumerate(numeric_cols_hour):
    sns.boxplot(data=hour_df_original, y=col, ax=axes[idx, 0])
    axes[idx, 0].set_title(f'{col} - Before Outlier Removal')
    sns.boxplot(data=hour_df_cleaned, y=col, ax=axes[idx, 1])
    axes[idx, 1].set_title(f'{col} - After Outlier Removal')
plt.tight_layout()
plt.show()


day_df=day_df_cleaned
hour_df=hour_df_cleaned


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
    # Statistik dasar penyewaan sepeda harian
    st.subheader("Statistik dasar penyewaan sepeda harian")
    
    # Visualisasi distribusi jumlah penyewaan
    desc_stats = filtered_day_df[['casual', 'registered', 'total_count']].agg(['mean', 'median', 'min', 'max'])
    
    fig1, ax1 = plt.subplots(figsize=(10,6))
    desc_stats.T.plot(kind='bar', ax=ax1)
    ax1.set_title("Summary Statistics of Casual, Registered, and Total Count")
    ax1.set_ylabel("Jumlah Penyewaan")
    ax1.set_xticklabels(desc_stats.columns, rotation=0)
    ax1.grid(True)
    st.pyplot(fig1)
    
    # Insight
    st.markdown("""
    **Insight:**
    - *casual* (penyewa non-member) memiliki rata-rata yang lebih rendah dibandingkan *registered* (penyewa member).
    - Penyewa *registered* lebih dominan dibandingkan *casual*, ini menunjukkan bahwa sebagian besar pelanggan adalah pengguna yang sudah berlangganan atau rutin.
    """)
    
    # Statistik dasar penyewaan sepeda per Jam
    st.subheader("Statistik dasar penyewaan sepeda per Jam")
    
    avg_rent_by_hour = filtered_hour_df.groupby('hour')['total_count'].mean()
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=avg_rent_by_hour.index, y=avg_rent_by_hour.values, marker="o", color="b", ax=ax2)
    ax2.set_xticks(range(0, 24))
    ax2.set_xlabel("Jam dalam Sehari")
    ax2.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax2.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
    ax2.grid(True)
    st.pyplot(fig2)
    
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

    hour_df['time_segment'] = hour_df['hour'].astype(int).apply(time_segment)

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

    hour_df['usage_category'] = hour_df['total_count'].apply(usage_category)

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    # === CROSSTAB TIME SEGMENT ===
    st.subheader("🕒 Proporsi Usage Category per Waktu")

    ct_time = pd.crosstab(hour_df['time_segment'], hour_df['usage_category'], normalize='index') * 100

    fig3, ax3 = plt.subplots(figsize=(8, 5))
    ct_time.plot(kind='bar', stacked=True, colormap='Set2', ax=ax3)
    ax3.set_title("Proporsi Usage Category per Waktu")
    ax3.set_ylabel("% Usage")
    ax3.legend(title="Usage Category")
    ax3.grid(True)
    st.pyplot(fig3)

    # === CROSSTAB WEATHER ===
    st.subheader("🌦️ Proporsi Usage Category per Kondisi Cuaca")

    ct_weather = pd.crosstab(hour_df['weather_situation'], hour_df['usage_category'], normalize='index') * 100

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
