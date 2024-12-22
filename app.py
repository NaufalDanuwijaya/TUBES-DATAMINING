import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Pelanggan", layout="wide")

# Header
st.markdown("""
<style>
    .main-header {
        font-size: 30px;
        font-weight: bold;
        text-align: center;
    }
    .sub-header {
        font-size: 20px;
        text-align: center;
    }
</style>
<div class='main-header'>Dashboard Segmentasi dan Klasifikasi Pelanggan</div>
<div class='sub-header'>Visualisasi hasil analisis data pelanggan</div>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    # Ganti path ini sesuai dengan data Anda
    data_path = "cleaned_transactions.csv"  # Anda dapat mengganti ini dengan data yang telah diolah
    return pd.read_csv(data_path)

data = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_country = st.sidebar.selectbox("Pilih Negara", options=["Semua"] + list(data["Country"].unique()))

if selected_country != "Semua":
    data = data[data["Country"] == selected_country]

# Metrics
st.markdown("### Statistik Utama")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pelanggan", len(data["CustomerID"].unique()))
col2.metric("Total Transaksi", data["InvoiceNo"].nunique())
col3.metric("Total Produk", data["StockCode"].nunique())
col4.metric("Total Penjualan", f"${data['Sales'].sum():,.2f}")

# Visualisasi Data
st.markdown("### Visualisasi Penjualan dan Produk")

# Scatter Plot Sales vs Quantity
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=data['Sales'], y=data['Quantity'], ax=ax, color="purple")
ax.set_title("Hubungan Sales vs Quantity")
st.pyplot(fig)

# Bar Chart Penjualan per Negara
sales_country = data.groupby('Country')["Sales"].sum().reset_index()
fig_bar = px.bar(sales_country, x="Country", y="Sales", title="Penjualan per Negara")
st.plotly_chart(fig_bar)

# Pie Chart Segmentasi Pelanggan
if "customer_segment" in data.columns:
    segment_data = data["customer_segment"].value_counts().reset_index()
    segment_data.columns = ["Segment", "Jumlah"]
    fig_pie = px.pie(segment_data, names="Segment", values="Jumlah", title="Segmentasi Pelanggan")
    st.plotly_chart(fig_pie)

# Tabel Data Pelanggan
st.markdown("### Data Pelanggan")
st.dataframe(data.head(20))

# Footer
st.markdown("---")
st.write("Dashboard ini dibuat menggunakan Streamlit.")
