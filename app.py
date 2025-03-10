%%writefile app.py
import streamlit as st
import pandas as pd

# Load dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Judul Aplikasi
st.title("Bike Sharing Data Analysis")

# Sidebar untuk memilih dataset
dataset_option = st.sidebar.selectbox("Pilih Dataset", ["Daily Data", "Hourly Data"])

# Menampilkan dataset yang dipilih
if dataset_option == "Daily Data":
    st.subheader("Daily Bike Sharing Data")
    st.write(day_df)
else:
    st.subheader("Hourly Bike Sharing Data")
    st.write(hour_df)

# Menampilkan statistik dasar
st.subheader("Statistik Deskriptif")
if dataset_option == "Daily Data":
    st.write(day_df.describe())
else:
    st.write(hour_df.describe())
