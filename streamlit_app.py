import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Convert date column
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Sidebar navigation
st.sidebar.title("🚲 Bike Sharing Dashboard")
page = st.sidebar.radio("Pilih Analisis", ["Dataset & Statistik", "Waktu Puncak", "Cuaca & Musim", "RFM Analysis & Clustering"])

# Page: Dataset & Statistik
if page == "Dataset & Statistik":
    st.title("📊 Exploratory Data Analysis")
    
    if st.checkbox("Tampilkan dataset harian"):
        st.write(day_df.head())

    if st.checkbox("Tampilkan dataset per jam"):
        st.write(hour_df.head())

    st.subheader("📌 Statistik Penyewaan Sepeda Harian")
    st.write(day_df[['casual', 'registered', 'cnt']].describe())

    # Distribusi jumlah penyewaan
    st.subheader("📊 Distribusi Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(day_df["cnt"], bins=30, kde=True, color="blue", ax=ax)
    ax.set_xlabel("Jumlah Penyewaan Sepeda")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Distribusi Penyewaan Sepeda")
    st.pyplot(fig)

# Page: Waktu Puncak Penyewaan
elif page == "Waktu Puncak":
    st.title("⏰ Analisis Waktu Puncak Penyewaan")

    avg_rent_by_hour = hour_df.groupby("hr")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=avg_rent_by_hour.index, y=avg_rent_by_hour.values, marker="o", color="b", ax=ax)
    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
    ax.grid(True)
    st.pyplot(fig)

    st.write("🚲 **Insight:**")
    st.write("- Puncak penyewaan terjadi pada pukul **07:00 - 09:00** dan **17:00 - 19:00**.")
    st.write("- Hal ini menunjukkan bahwa banyak orang menggunakan sepeda untuk keperluan komuter.")

# Page: Pengaruh Cuaca & Musim
elif page == "Cuaca & Musim":
    st.title("🌦️ Analisis Pengaruh Cuaca & Musim")

    # Pengaruh cuaca
    st.subheader("☁️ Pengaruh Cuaca terhadap Penyewaan")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="weathersit", y="cnt", data=day_df, palette="coolwarm", ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    ax.set_xticklabels(["Cerah", "Berkabut", "Hujan Ringan", "Hujan Lebat"])
    st.pyplot(fig)

    # Pengaruh musim
    st.subheader("🍂 Pengaruh Musim terhadap Penyewaan")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="season", y="cnt", data=day_df, palette="viridis", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
    st.pyplot(fig)

    st.write("🚲 **Insight:**")
    st.write("- Penyewaan tertinggi saat cuaca **cerah**.")
    st.write("- Penyewaan menurun drastis saat hujan.")
    st.write("- Musim gugur memiliki penyewaan tertinggi, sedangkan musim semi dan dingin terendah.")

# Page: RFM Analysis & Clustering
elif page == "RFM Analysis & Clustering":
    st.title("📈 RFM Analysis & Clustering")

    # Recency Calculation
    latest_date = day_df["dteday"].max()
    day_df["recency"] = (latest_date - day_df["dteday"]).dt.days

    # Frequency & Monetary
    freq_by_weekday = day_df.groupby("weekday")["cnt"].mean()
    monetary = day_df.groupby("weekday")["cnt"].sum()

    # Recency Histogram
    st.subheader("📅 Distribusi Recency Penyewaan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(day_df["recency"], bins=30, kde=True, color="blue", ax=ax)
    ax.set_xlabel("Hari Sejak Penyewaan Terakhir")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Distribusi Recency Penyewaan Sepeda")
    st.pyplot(fig)

    # Frequency & Monetary Charts
    st.subheader("📊 Rata-rata & Total Penyewaan per Hari")
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    
    sns.barplot(x=freq_by_weekday.index, y=freq_by_weekday.values, ax=ax[0], palette="coolwarm")
    ax[0].set_title("Rata-rata Penyewaan per Hari")
    ax[0].set_xlabel("Hari dalam Seminggu (0=Senin, 6=Minggu)")
    ax[0].set_ylabel("Rata-rata Penyewaan")

    sns.barplot(x=monetary.index, y=monetary.values, ax=ax[1], palette="viridis")
    ax[1].set_title("Total Penyewaan Berdasarkan Hari")
    ax[1].set_xlabel("Hari dalam Seminggu (0=Senin, 6=Minggu)")
    ax[1].set_ylabel("Total Penyewaan")

    st.pyplot(fig)

    # Clustering (Binning)
    st.subheader("📌 Clustering Kategori Penyewaan")
    bins = [0, 2500, 5000, 7500, 10000]
    labels = ["Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]
    day_df["rent_category"] = pd.cut(day_df["cnt"], bins=bins, labels=labels)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x=day_df["rent_category"], palette="pastel", ax=ax)
    ax.set_xlabel("Kategori Penyewaan")
    ax.set_ylabel("Jumlah Hari")
    ax.set_title("Distribusi Kategori Penyewaan Sepeda")
    st.pyplot(fig)

    st.write("🚲 **Insight:** Penyewaan dapat dikategorikan ke dalam 4 kelompok berdasarkan jumlah totalnya.")
