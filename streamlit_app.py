import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Title
st.title("🚲 Bike Sharing Data Dashboard")
st.write("Analisis interaktif dari penggunaan sepeda berdasarkan dataset penyewaan sepeda.")

# Sidebar untuk memilih dataset
dataset_option = st.sidebar.selectbox("Pilih Dataset", ["Daily Data", "Hourly Data"])

# Menampilkan dataset yang dipilih
if dataset_option == "Daily Data":
    st.subheader("📅 Daily Bike Sharing Data")
    df = day_df
else:
    st.subheader("⏳ Hourly Bike Sharing Data")
    df = hour_df

# Menampilkan dataset dan statistik deskriptif
if st.checkbox("Tampilkan Dataframe"):
    st.write(df)

if st.checkbox("Tampilkan Statistik Deskriptif"):
    st.write(df.describe())

# Visualisasi Tren Penyewaan Sepeda
st.subheader("📈 Tren Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['dteday'], df['cnt'], label='Total Rentals', color='blue')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda dari Waktu ke Waktu")
ax.legend()
st.pyplot(fig)

# Analisis Waktu Sibuk
st.subheader("⏰ Kapan Waktu Puncak Penyewaan?")
if dataset_option == "Hourly Data":
    peak_hours = df.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(peak_hours.index, peak_hours.values, color='green')
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_title("Pola Penyewaan Sepeda per Jam")
    st.pyplot(fig)
else:
    st.write("Pilih dataset Hourly Data untuk analisis ini.")

# Analisis Pengaruh Musim
st.subheader("🌦️ Pengaruh Cuaca dan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x="season", y="cnt", data=df, palette="viridis", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
st.pyplot(fig)

st.write("Dari hasil analisis, terlihat bahwa musim gugur memiliki jumlah penyewaan tertinggi.")

# Footer
st.markdown("---")
st.write("📊 Dashboard ini dibuat menggunakan Streamlit.")
