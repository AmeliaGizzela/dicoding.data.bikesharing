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

        # Insight
    st.markdown("""
    **Insight:**
    - Nilai minimum total_count adalah 22 dan maksimum mencapai 8714, menandakan adanya variasi besar dalam jumlah penyewaan harian.
    - Penyewaan sepeda meningkat tajam pada pukul **07:00 - 09:00** (jam berangkat kerja) dan **17:00 - 19:00** (jam pulang kerja).
    """)
    
    # === PENGARUH CUACA ===
    st.subheader("🌦️Pertanyaan 2. Analisis Pengaruh Cuaca terhadap Penyewaan Sepeda")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        x='weather_situation', 
        y='total_count', 
        data=filtered_day_df, 
        palette="coolwarm", 
        ax=ax
    )
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    ax.set_xticks([0,1,2,3])
    ax.set_xticklabels(["Cerah", "Berkabut", "Hujan Ringan", "Hujan Lebat"])
    ax.grid(True)
    st.pyplot(fig)

     # Insight
    st.markdown("""
    **Insight:**
    - Pada cuaca cerah dan berkabut, jumlah penyewaan sepeda jauh lebih tinggi.
    - Penyewaan menurun drastis saat cuaca hujan ringan dan hujan lebat.
    - Artinya, cuaca buruk sangat mempengaruhi penurunan demand sepeda.
    """)
    
    # === PENGARUH MUSIM ===
    st.subheader("🍂Pertanyaan 3. Analisis Pengaruh Musim terhadap Penyewaan Sepeda")
        
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        x="season", 
        y='total_count', 
        data=filtered_day_df, 
        palette="viridis", 
        ax=ax
    )
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
    ax.grid(True)
    st.pyplot(fig)
    
    # === Insight ===
    st.markdown("""
    **Insight:**
    - Penyewaan paling tinggi terjadi saat musim **Fall** dan **Summer**.
    - Penyewaan lebih rendah di **Winter** dan **Spring**.
    - Musim memiliki pengaruh yang signifikan terhadap demand.
    """)

# ==== TAB 2: BUSINESS ANALYSIS ====
with tab2:
    st.title("📌 Business Analysis & Insights")
    
    # === MANUAL GROUPING BERDASARKAN WAKTU ===
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
    
    # === BINNING TOTAL COUNT ===
    Q1 = filtered_hour_df['total_count'].quantile(0.25)
    Q3 = filtered_hour_df['total_count'].quantile(0.75)
    
    def usage_category(count):
        if count <= Q1:
            return 'Low Usage'
        elif count >= Q3:
            return 'High Usage'
        else:
            return 'Medium Usage'
    
    filtered_hour_df['usage_category'] = filtered_hour_df['total_count'].apply(usage_category)
    
    # === VISUALISASI 1: Penyewaan Berdasarkan Segmentasi Waktu ===
    st.markdown("### **Distribusi Penyewaan Berdasarkan Segmentasi Waktu**")
    fig1, ax1 = plt.subplots(figsize=(8,5))
    sns.boxplot(x='time_segment', y='total_count', data=filtered_hour_df, palette='Set2', ax=ax1)
    ax1.set_title("Distribusi Penyewaan Berdasarkan Segmentasi Waktu")
    ax1.set_ylabel("Jumlah Penyewaan")
    ax1.grid(True)
    st.pyplot(fig1)
    
    # === VISUALISASI 2: Distribusi Kategori Penggunaan ===
    st.markdown("### **Distribusi Kategori Penggunaan Sepeda**")
    fig2, ax2 = plt.subplots(figsize=(7,4))
    sns.countplot(x='usage_category', data=filtered_hour_df, palette='Set3', ax=ax2)
    ax2.set_title("Distribusi Kategori Penggunaan Sepeda")
    ax2.set_ylabel("Jumlah Observasi")
    ax2.grid(True)
    st.pyplot(fig2)
    
    # === CROSS ANALYSIS ===
    st.markdown("### **Cross Analysis: Kapan dan Kondisi Apa Perlu Tambah Sepeda?**")
    
    # Crosstab High Usage vs Time Segment
    ct_time = pd.crosstab(filtered_hour_df['time_segment'], filtered_hour_df['usage_category'], normalize='index') * 100
    
    # Crosstab High Usage vs Weather
    ct_weather = pd.crosstab(filtered_hour_df['weather_situation'], filtered_hour_df['usage_category'], normalize='index') * 100
    
    # Tampilkan tabel
    st.markdown("#### Proporsi Usage Category per Waktu")
    st.dataframe(ct_time.round(2))
    
    st.markdown("#### Proporsi Usage Category per Kondisi Cuaca")
    st.dataframe(ct_weather.round(2))
    
    # === VISUALISASI CROSS ===
    fig3, ax3 = plt.subplots(figsize=(8,5))
    ct_time.plot(kind='bar', stacked=True, colormap='Set2', ax=ax3)
    ax3.set_title("Proporsi Usage Category per Waktu")
    ax3.set_ylabel("% Usage")
    ax3.legend(title="Usage Category")
    ax3.grid(True)
    st.pyplot(fig3)
    
    fig4, ax4 = plt.subplots(figsize=(8,5))
    ct_weather.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax4)
    ax4.set_title("Proporsi Usage Category per Kondisi Cuaca")
    ax4.set_ylabel("% Usage")
    ax4.legend(title="Usage Category")
    ax4.grid(True)
    st.pyplot(fig4)
    
    # === INSIGHT ===
    st.markdown("""
    #### **Kapan sebaiknya deploy sepeda lebih banyak?**
    - **Pagi** (5:00 - 10:00) dan **Sore** (16:00 - 20:00) menunjukkan proporsi tertinggi untuk High Usage.
    🚩 **Action:** Tambahkan sepeda lebih banyak di slot waktu ini, khususnya di weekdays.
    
    - **Malam** (21:00 - 4:00) memiliki dominasi Low Usage, artinya kamu bisa menurunkan jumlah sepeda aktif di jam ini, kecuali untuk area tertentu (misal: dekat hiburan malam/weekend spot).
    
    #### **Kondisi apa yang butuh extra sepeda?**
    - Pada cuaca **cerah** (Cerah & Berkabut), High Usage mendominasi lebih dari 50% total sewa.
    🚩 **Action:** Perbanyak sepeda di hari-hari cerah.
    
    - Pada **hujan ringan** dan **hujan lebat**, distribusi usage lebih banyak di Low Usage, jadi kamu bisa kurangi jumlah sepeda yang tersedia di stasiun pada hari hujan.
    """)
