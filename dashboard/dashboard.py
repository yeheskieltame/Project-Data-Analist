import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Dataset Bike Sharing")

# Mengimpor Data
@st.cache
def load_data():
    day_path = 'day.csv'
    hour_path = 'hour.csv'
    data_day = pd.read_csv(day_path)
    data_hour = pd.read_csv(hour_path)
    return data_day, data_hour

data_day, data_hour = load_data()

# Pertanyaan 1: Hari Libur vs Hari Kerja
st.header("Penyewaan Sepeda: Hari Libur vs Hari Kerja")
holiday_counts = data_day[data_day['holiday'] == 1]['cnt'].describe()
workingday_counts = data_day[data_day['holiday'] == 0]['cnt'].describe()

st.write("Statistik Penyewaan pada Hari Libur:")
st.write(holiday_counts)

st.write("Statistik Penyewaan pada Hari Kerja:")
st.write(workingday_counts)

# Visualisasi
fig, ax = plt.subplots()
sns.boxplot(x='holiday', y='cnt', data=data_day, ax=ax)
ax.set_xticklabels(['Hari Kerja', 'Hari Libur'])
plt.title('Perbandingan Penyewaan Sepeda')
st.pyplot(fig)

# Pertanyaan 2: Penyewaan per Jam
st.header("Rata-rata Penyewaan Sepeda per Jam")
hourly_counts = data_hour.groupby('hr')['cnt'].mean().reset_index()

fig, ax = plt.subplots()
sns.lineplot(x='hr', y='cnt', data=hourly_counts, ax=ax)
plt.title('Rata-rata Penyewaan Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(range(0, 24))
plt.grid()
st.pyplot(fig)

# Kesimpulan
st.header("Kesimpulan")
st.write("""
- Penyewaan sepeda lebih tinggi pada hari kerja dibandingkan dengan hari libur.
- Penyewaan sepeda paling tinggi terjadi pada sore hari, terutama antara jam 17:00 dan 19:00.
""")
