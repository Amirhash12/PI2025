import streamlit as st 
import pandas as pd

# Function to embed Power BI dashboard
def embed_powerbi_dashboard():
    st.markdown(
        """
        <iframe width="100%" height="1500" src="https://app.powerbi.com/reportEmbed?reportId=983aee91-5e6a-47f8-b313-58a4325faf8e&autoAuth=true&ctid=fb7a3c6a-18b6-4c53-85a8-0a0132044db9" frameborder="0" allowFullScreen="true"></iframe>
        """,
        unsafe_allow_html=True
    )

# Load Excel data
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/Amirhash12/PI2025/3107a53c39bc5771d619031a91cb154991f4a424/ConsolidatedPE.xlsx'
    df = pd.read_excel(url, engine='openpyxl')
    return df
st.title('Data Loader')

data = load_data()
st.write(data)

# Streamlit App
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Price Management Application")
with col2:
    st.image("C:/any/image.png", width=300)  # Adjust the width as needed

# Create Tabs
tab1, tab2 = st.tabs(["Power BI Dashboard", "Price Adjuster"])

with tab1:
    embed_powerbi_dashboard()

with tab2:
    st.header("Product Price Adjuster")
    
    # Initialize session state for products to adjust
    if 'products_to_adjust' not in st.session_state:
        st.session_state.products_to_adjust = []

    # Function to add new product to the list
    def add_product():
        st.session_state.products_to_adjust.append({'product': '', 'Gross ASP LCY in USD without Samples': 0, 'country': ''})

    # Add button to add more products
    if st.button("Add Product"):
        add_product()
    
    # Display the products to adjust
    for i, product in enumerate(st.session_state.products_to_adjust):
        st.subheader(f"Product {i+1}")
        
        # Create columns for filters and slicers
        col1, col2, col3 = st.columns(3)
        
        with col1:
            country = st.selectbox(f"Select Country {i+1}", data['Country'].unique(), key=f"country_{i}")
        
        with col2:
            product_name = st.selectbox(f"Select a Product {i+1}", data[data['Country'] == country]['Product'].unique(), key=f"product_{i}")
        
        with col3:
            current_price = data.loc[(data['Product'] == product_name) & (data['Country'] == country), 'Gross ASP LCY in USD without Samples'].values[0]
            st.write(f"Current Price: {round(current_price,4)}")
            
       # Create columns for price range selection and new price input
        col4, col5, col6 = st.columns(3)
        
        with col4:
            price_range = st.radio(f"Select Price Change Range for {product_name} in {country}",
                                   options=['2.5% to 2.7%', '2.7% to 2.9%', '2.9% to 3%'],
                                   key=f"range_{i}")
        
        with col5:
            # Calculate new price based on selected range
            if price_range == '2.5% to 2.7%':
                min_increase, max_increase = 0.025, 0.027
            elif price_range == '2.7% to 2.9%':
                min_increase, max_increase = 0.027, 0.029
            else:  # '2.9% to 3%'
                min_increase, max_increase = 0.029, 0.030
            
            lower_price = current_price * (1 + min_increase)
            upper_price = current_price * (1 + max_increase)
            
            st.write(f"MIN Price: {round(lower_price, 2)}")
            st.write(f"MAX Price: {round(upper_price, 2)}")
        
        with col6:
            # Default new price calculation (midpoint of the range)
            new_price = current_price * (1 + (min_increase + max_increase) / 2)
            new_price = st.number_input(f"New Price for {product_name} in {country}", value=round(new_price, 2), key=f"price_{i}")
        
        # Save the adjusted product
        st.session_state.products_to_adjust[i] = {'product': product_name, 'price': new_price, 'country': country, 'range': price_range}
    
    # Button to update all prices
    if st.button("Update Prices"):
        for product in st.session_state.products_to_adjust:
            data.loc[(data['Product'] == product['product']) & (data['Country'] == product['country']), 'Gross ASP LCY in USD without Samples'] = product['Gross ASP LCY in USD without Samples']
        # Save the updated data to Excel
        data.to_excel('path_to_excel_file.xlsx', index=False)
        st.success("Prices have been updated.")