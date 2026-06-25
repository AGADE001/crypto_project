import streamlit as st
import psycopg2
import os
import pandas as pd

st.set_page_config(page_title="Digital Commodity Analytics", layout="wide")

st.markdown("Project 1")
st.markdown("---")

#----------Database Connection----------#
DB_HOST = "crypto-db"
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

#Function to safely pull historical rows
def fetch_dashboard_data():
    #SQL Connection
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    #CRITICAL: This query targets 'commodity_history' table, also its just a string
    query = """
    SELECT symbol, price, timestamp 
    FROM commodity_history ORDER BY 
    timestamp DESC LIMIT 200;
    """
    #'pd.read_sql asks for ('sql statement','sql connection')'
    df = pd.read_sql(query,conn)
    conn.close()
    return df

#Render content to webpage
try:
    #----------Website Front End----------#
    df = fetch_dashboard_data()
    if not df.empty: #Guarantees we only pull when data frame is populated
        #---Card Grid---#
        m1,m2,m3 = st.columns(3)
        with m1: 
            st.metric(label="Tracking Network State:", value="🟢 ONLINE")
        with m2:
            st.metric(label="Total Unique Assets", value=f"{df['symbol'].nunique()}: Commodities")
        with m3:
            latest_time = df['timestamp'].iloc[0].strftime('%Y-%m-%d %H:%M:%S')
            st.metric(label="Last Ingestion Engine Cycle", value=latest_time)
        st.markdown("---")
        #Dropdown menu to filter which asset to display analytics
        unique_symbols = sorted(df['symbol'].unique())

        col_select, _ = st.columns([1,2])
        with col_select:
            selected_symbol = st.selectbox("Select Token to Visualize: ", unique_symbols)
        
        #Filtered dataframe(table) of the selected choice from the pool of symbols obtained from the unfiltered dataframe 
        filtered_df = df[df["symbol"] == selected_symbol].copy()

        chart_col, ledger_col = st.columns([2.5,1])

        #column front end
        with chart_col:
            st.subheader(f"{selected_symbol} Asset Performance History")
            chart_data = filtered_df.set_index('timestamp')['price']#Make x-axis time stamp, price y
            st.line_chart(chart_data)

        #ledger frontend
        with ledger_col:
            st.subheader("Ledger")
            display_ledger = filtered_df.sort_values(by='timestamp', ascending=False)[['price', 'timestamp']]
            st.dataframe(display_ledger, width="stretch", height=320)
    else:
        st.warning("Database is connected, but the 'commodity_history' table is currently empty.")
except Exception as e:
    st.error(f"Waiting for pipeline sync... Connection status: {e}")