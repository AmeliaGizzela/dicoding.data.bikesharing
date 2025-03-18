# streamlit_app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
day_df = pd.read_csv("day.csv")

# Convert dteday to datetime
day_df['date'] = pd.to_datetime(day_df['dteday'])

# Sidebar filter
st.sidebar.header("Filter Data")

# Date filter
start_date = st.sidebar.date_input("Start Date", day_df['date'].min())
end_date = st.sidebar.date_input("End Date", day_df['date'].max())

# Season filter
season_options = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
selected_seasons = st.sidebar.multiselect(
    "Select Season",
    options=list(season_options.keys()),
    format_func=lambda x: season_options[x],
    default=list(season_options.keys())
)

# Apply filter
filtered_df = day_df[
    (day_df['date'] >= pd.to_datetime(start_date)) &
    (day_df['date'] <= pd.to_datetime(end_date)) &
    (day_df['season'].isin(selected_seasons))
]

# Main dashboard
st.title("Bike Sharing Dashboard 🚲")

st.markdown("### Total Penyewaan Sepeda Berdasarkan Filter")

# Visualisasi 1: Trend harian setelah filter
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x='date', y='cnt', marker="o", ax=ax)
plt.title("Trend Penyewaan Sepeda Harian")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

# Visualisasi 2: Boxplot musiman
st.markdown("### Distribusi Penyewaan Berdasarkan Musim")
fig2, ax2 = plt.subplots(figsize=(8,5))
sns.boxplot(data=filtered_df, x='season', y='cnt', palette="Set2", ax=ax2)
ax2.set_xticklabels([season_options[x] for x in filtered_df['season'].unique()])
plt.grid(True)
st.pyplot(fig2)

# Display dataset (optional)
st.dataframe(filtered_df)
# Dictionary Season & Weather
season_options = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_options = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}

# Sidebar filter
st.sidebar.header("Filter Dashboard")

# Date filter
start_date = st.sidebar.date_input("Start Date", day_df['date'].min())
end_date = st.sidebar.date_input("End Date", day_df['date'].max())

# Season filter
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim",
    options=list(season_options.keys()),
    format_func=lambda x: season_options[x],
    default=list(season_options.keys())
)

# Weather filter
selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=list(weather_options.keys()),
    format_func=lambda x: weather_options[x],
    default=list(weather_options.keys())
)

# Metric Selector
metric = st.sidebar.radio(
    "Pilih Tipe Data",
    options=['total_count', 'registered', 'casual'],
    format_func=lambda x: f"Total ({x})" if x == "total_count" else x.capitalize()
)

# Apply filters
filtered_df = day_df[
    (day_df['date'] >= pd.to_datetime(start_date)) &
    (day_df['date'] <= pd.to_datetime(end_date)) &
    (day_df['season'].isin(selected_seasons)) &
    (day_df['weather_situation'].isin(selected_weather))
]

# MAIN DASHBOARD
st.title("Bike Sharing Dashboard 🚲")

# Metric Card
st.metric(label="Total Penyewaan Sepeda (Filtered)", value=filtered_df[metric].sum())

# Lineplot
st.markdown("### Trend Penyewaan Harian")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x='date', y=metric, marker="o", ax=ax)
plt.title(f"Trend {metric.capitalize()} Harian")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

# Boxplot musim
st.markdown("### Distribusi Penyewaan Berdasarkan Musim")
fig2, ax2 = plt.subplots(figsize=(8,5))
sns.boxplot(data=filtered_df, x='season', y=metric, palette="Set3", ax=ax2)
ax2.set_xticklabels([season_options[x] for x in filtered_df['season'].unique()])
plt.grid(True)
st.pyplot(fig2)

# Optional: Download filtered data
st.markdown("### Download Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Data as CSV", data=csv, file_name='filtered_bike_share.csv', mime='text/csv')
