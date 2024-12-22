import streamlit as st
import pandas as pd
import plotly.express as px

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

# Header Section with Enhanced Styling
st.markdown("""
<div class="main-header">
    <div class="header-title">SEGMENTASI DAN KLASIFIKASI PELANGGAN</div>
    <div class="header-subtitle">Kelompok 6 SI4609</div>
</div>
""", unsafe_allow_html=True)

# Load Data with Caching for Performance
@st.cache_data
def load_data():
    data_path = "cleaned_transactions.csv"
    data = pd.read_csv(data_path, parse_dates=['InvoiceDate'])  # Ensure date parsing
    return data

data = load_data()

# Sidebar for Filters (Enhancing User Control)
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Country", options=["All"] + sorted(data["Country"].unique()))

# Filter Data Based on User Selections
filtered_data = data.copy()
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
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('</div>', unsafe_allow_html=True)

insight1 = st.container()

with insight1:
    st.markdown("#### Sales by Country")
    sales_country = filtered_data.groupby('Country')['Sales'].sum().reset_index()
    fig = px.choropleth(sales_country, locations='Country',
                        locationmode='country names',
                        color='Sales',
                        hover_name='Country',
                        color_continuous_scale='RdBu',
                        title='Global Sales Distribution',
                        template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Data Table with Enhanced Styling and Pagination
st.markdown("### Detailed Data Table")
st.markdown('<div>', unsafe_allow_html=True)
st.dataframe(filtered_data.reset_index(drop=True).style.set_properties(**{
    'background-color': '#2C3333',
    'color': 'white',
    'border-color': '#2C3333',
    'font-size': '14px'
}))
st.markdown('</div>', unsafe_allow_html=True)

# Footer Section
st.markdown("""
<div style="text-align: center; color: #B0B0B0; padding: 20px;">
    &copy; 2024 Kelompok 6 / SI4609 | All Rights Reserved
</div>
""", unsafe_allow_html=True)
