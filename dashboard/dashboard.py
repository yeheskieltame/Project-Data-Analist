import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ssl
import urllib.request

# Nonaktifkan verifikasi SSL
ssl._create_default_https_context = ssl._create_unverified_context


# Muat data
@st.cache_data
def load_data():
    day_path = "https://raw.githubusercontent.com/yeheskieltame/Project-Data-Analist/main/Data/day.csv"
    hour_path = "https://raw.githubusercontent.com/yeheskieltame/Project-Data-Analist/main/Data/hour.csv"

    with urllib.request.urlopen(day_path) as response:
        data_day = pd.read_csv(response)
    with urllib.request.urlopen(hour_path) as response:
        data_hour = pd.read_csv(response)

    return data_day, data_hour


try:
    data_day, data_hour = load_data()
except Exception as e:
    st.error(f"Kesalahan saat memuat data: {e}")
    st.stop()

# Persiapkan data
data_day['is_weekend'] = data_day['weekday'].apply(lambda x: 1 if x in [5, 6] else 0)

# Aplikasi Streamlit
st.title('Dashboard Analisis Penyewaan Sepeda')

# Sidebar
st.sidebar.header('Filter')
date_range = st.sidebar.date_input('Rentang Tanggal',
                                   [pd.to_datetime(data_day['dteday']).min(), pd.to_datetime(data_day['dteday']).max()])

# Konten Utama
st.header('Penyewaan Sepeda: Hari Libur vs Hari Kerja')
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='holiday', y='cnt', data=data_day, ax=ax)
ax.set_title('Perbandingan Penyewaan Sepeda antara Hari Libur dan Hari Kerja')
ax.set_xticklabels(['Hari Kerja', 'Hari Libur'])
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

st.header('Rata-rata Penyewaan Sepeda per Hari')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='weekday', y='cnt', data=data_day, ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda per Hari dalam Seminggu')
ax.set_xlabel('Hari dalam Seminggu')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks(range(7))
ax.set_xticklabels(['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'])
st.pyplot(fig)

st.header('Pola Penyewaan Sepeda per Jam')
hourly_counts = data_hour.groupby('hr')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_counts, ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks(range(0, 24))
ax.grid()
st.pyplot(fig)

# Wawasan tambahan
st.header('Wawasan Utama')
st.write("""
- Terdapat perbedaan signifikan dalam penyewaan sepeda antara hari libur dan hari kerja, dengan hari kerja menunjukkan rata-rata penyewaan yang lebih tinggi.
- Akhir pekan juga menunjukkan tren penyewaan yang lebih tinggi dibandingkan dengan hari kerja biasa.
- Penyewaan sepeda mencapai puncaknya antara pukul 17:00 dan 19:00, menunjukkan penggunaan yang lebih tinggi selama jam pulang kerja.
""")

# Elemen interaktif
st.header('Jelajahi Data')
if st.checkbox('Tampilkan data mentah'):
    st.subheader('Data mentah')
    st.write(data_day)

st.subheader('Penyewaan Harian')
selected_date = st.date_input('Pilih tanggal', min_value=pd.to_datetime(data_day['dteday']).min(),
                              max_value=pd.to_datetime(data_day['dteday']).max())
filtered_data = data_day[pd.to_datetime(data_day['dteday']).dt.date == selected_date]
if not filtered_data.empty:
    st.write(f"Total penyewaan pada {selected_date}: {filtered_data['cnt'].values[0]}")
else:
    st.write("Tidak ada data tersedia untuk tanggal yang dipilih.")

# Jalankan aplikasi Streamlit
if __name__ == '__main__':
    st.sidebar.info(
        'Dashboard ini menyediakan wawasan tentang pola penyewaan sepeda berdasarkan analisis yang diberikan.')
