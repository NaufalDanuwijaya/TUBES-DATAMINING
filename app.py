import streamlit as st
import pandas as pd
import plotly.express as px

# RANDOM FOREST
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from collections import Counter

import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("hasil_clustering.csv")

X = df[['total_transactions', 'total_products', 'total_unique_products', 'total_sales',
          'avg_product_value', 'avg_cart_value', 'min_cart_value', 'max_cart_value']]
y = df['Cluster']

# Menggunakan SMOTE untuk balancing
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Membagi data menjadi Training dan Testing set
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

# Inisialisasi Random Forest Classifier
rf_model= RandomForestClassifier(n_estimators=100, random_state=42)

# Melatih model
rf_model.fit(X_train, y_train)

# Prediksi pada data testing
y_pred = rf_model.predict(X_test)

# Page Config
st.set_page_config(page_title="Data Mining", layout="wide")

# Custom CSS for Dark Theme and Enhanced Styling
st.markdown("""
<style>
    /* Dark theme background and text color */
    .stApp {
        background-color: #1E2326;
        color: #FFFFFF;
    }

    /* Change the color of input labels to white */
    label {
        color: #FFFFFF !important;
    }
    
    /* Header styling */
    .main-header {
        padding: 2rem 1rem;
        background-color: #2C3333;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .header-title {
        font-size: 32px;
        font-weight: bold;
        color: #FF69B4;
        margin-bottom: 10px;
    }
    .header-subtitle {
        font-size: 18px;
        color: #B0B0B0;
    }

    /* Card styling for metrics */
    .metric-card {
        background-color: #2C3333;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: scale(1.05);
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #FF69B4;
    }
    .metric-label {
        color: #B0B0B0;
        font-size: 16px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Filter section */
    .filters-section {
        background-color: #2C3333;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 30px;
    }

    /* Button styling */
    .stButton>button {
        background-color: #FF69B4;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #FF85C1;
    }
</style>
""", unsafe_allow_html=True)

# Load Data with Caching for Performance
@st.cache_data
def load_data():
    transactions_path = "cleaned_transactions.csv"
    clustering_path = "hasil_clustering.csv"

    transactions_data = pd.read_csv(transactions_path, parse_dates=['InvoiceDate'])
    clustering_data = pd.read_csv(clustering_path)

    return transactions_data, clustering_data

transactions_data, clustering_data = load_data()

# Header Section with Enhanced Styling
st.markdown("""
<div class="main-header">
    <div class="header-title">SEGMENTASI DAN KLASIFIKASI PELANGGAN</div>
    <div class="header-subtitle">Kelompok 6 SI4609</div>
</div>
""", unsafe_allow_html=True)

# Sidebar for Filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Country", options=["All"] + sorted(transactions_data["Country"].unique()))

# Filter Transactions Data Based on User Selections
filtered_data = transactions_data.copy()
if selected_country != "All":
    filtered_data = filtered_data[filtered_data["Country"] == selected_country]

# Key Metrics Displayed as Cards
st.markdown("### Key Metrics")
metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    unique_customers = filtered_data["CustomerID"].nunique()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{unique_customers:,}</div>
        <div class="metric-label">Unique Customers</div>
    </div>
    """, unsafe_allow_html=True)

with metric2:
    unique_invoices = filtered_data["InvoiceNo"].nunique()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{unique_invoices:,}</div>
        <div class="metric-label">Total Invoices</div>
    </div>
    """, unsafe_allow_html=True)

with metric3:
    unique_products = filtered_data["StockCode"].nunique()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{unique_products:,}</div>
        <div class="metric-label">Unique Products</div>
    </div>
    """, unsafe_allow_html=True)

with metric4:
    total_sales = filtered_data['Sales'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${total_sales:,.2f}</div>
        <div class="metric-label">Total Sales</div>
    </div>
    """, unsafe_allow_html=True)

# Charts Section with Enhanced Visuals and Interactivity
st.markdown("### Data Visualizations")
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("#### Sales Over Time")
    sales_over_time = filtered_data.set_index('InvoiceDate').resample('M')['Sales'].sum().reset_index()
    fig = px.line(sales_over_time, x='InvoiceDate', y='Sales', 
                  title='Monthly Sales',
                  labels={'InvoiceDate': 'Date', 'Sales': 'Sales ($)'},
                  template='plotly_dark')
    fig.update_traces(line=dict(color='#FF69B4'))
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.markdown("#### Top 10 Products by Sales")
    top_products = filtered_data.groupby('StockCode')['Sales'].sum().nlargest(10).reset_index()
    fig = px.bar(top_products, x='StockCode', y='Sales',
                 title='Top 10 Products',
                 labels={'StockCode': 'Product Code', 'Sales': 'Sales ($)'},
                 template='plotly_dark',
                 color='Sales',
                 color_continuous_scale='RdBu')
    st.plotly_chart(fig, use_container_width=True)

# Customer Segmentation Visualizations
st.markdown("### Customer Segmentation")

# Pie Chart of Customer Segments
st.markdown("#### Distribution of Customer Segments")
segment_distribution = clustering_data['Customer_Segment'].value_counts().reset_index()
segment_distribution.columns = ['Segment', 'Count']
fig = px.pie(segment_distribution, values='Count', names='Segment', 
             title='Customer Segment Distribution', 
             template='plotly_dark',
             color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True)

# Scatter Plot of Clustering Results
st.markdown("#### Customer Clusters")
fig = px.scatter(clustering_data, x='avg_cart_value', y='total_sales', 
                 color='Cluster',
                 size='total_transactions',
                 hover_data=['CustomerID'],
                 title='Customer Clusters Based on Avg Cart Value and Total Sales',
                 labels={'avg_cart_value': 'Avg Cart Value', 'total_sales': 'Total Sales'},
                 template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)

# Predict Customer Cluster
st.markdown("### Predict Customer Cluster")
st.markdown("Use the inputs below to predict the customer cluster.")

# Input fields
col1, col2 = st.columns(2)
with col1:
    total_transactions = st.number_input("Total Transactions", min_value=0, value=0)
    total_products = st.number_input("Total Products", min_value=0, value=0)
    total_unique_products = st.number_input("Total Unique Products", min_value=0, value=0)
    min_cart_value = st.number_input("Minimum Cart Value", min_value=0.0, value=0.0)
    max_cart_value = st.number_input("Maximum Cart Value", min_value=0.0, value=0.0)
with col2:
    total_sales = st.number_input("Total Sales", min_value=0.0, value=0.0)
    avg_product_value = st.number_input("Average Product Value", min_value=0.0, value=0.0)
    avg_cart_value = st.number_input("Average Cart Value", min_value=0.0, value=0.0)

# Predict Button
if st.button("Predict Cluster"):
    # Create a DataFrame for prediction
    input_data = pd.DataFrame({
        'total_transactions': [total_transactions],
        'total_products': [total_products],
        'total_unique_products': [total_unique_products],
        'total_sales': [total_sales],
        'avg_product_value': [avg_product_value],
        'avg_cart_value': [avg_cart_value],
        'min_cart_value': [min_cart_value],
        'max_cart_value': [max_cart_value] 
    })

    # Perform prediction
    try:
        cluster_prediction = rf_model.predict(input_data)[0]
        st.success(f"The customer belongs to Cluster {cluster_prediction}.")
    except ValueError as e:
        st.error(f"Error: {e}")

# Data Table with Enhanced Styling and Pagination
st.markdown("### Detailed Data Table")
st.dataframe(filtered_data.reset_index(drop=True).style.set_properties(**{
    'background-color': '#2C3333',
    'color': 'white',
    'border-color': '#2C3333',
    'font-size': '14px'
}))

# Footer Section
st.markdown("""
<div style="text-align: center; color: #B0B0B0; padding: 20px;">
    &copy; 2024 Kelompok 6 / SI4609 | All Rights Reserved
</div>
""", unsafe_allow_html=True)
