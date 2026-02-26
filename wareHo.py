import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import time

# -------------------- CONFIG --------------------
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students"
}

USERNAME = "admin"
PASSWORD = "admin"

REFRESH_INTERVAL = 10  # seconds

# -------------------- LOGIN --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Warehouse Monitoring Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")

if not st.session_state.logged_in:
    login()
    st.stop()

# -------------------- DATABASE FUNCTION --------------------
def fetch_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT * FROM WareHouse ORDER BY DateTime DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# -------------------- MAIN DASHBOARD --------------------
st.title("🍇 Grapes Warehouse Monitoring Dashboard")

placeholder = st.empty()

while True:
    with placeholder.container():

        df = fetch_data()

        if df.empty:
            st.warning("No data available")
        else:
            df["DateTime"] = pd.to_datetime(df["DateTime"])

            st.subheader("Latest Readings")
            st.dataframe(df.head(10), use_container_width=True)

            # Temperature Graph
            fig_temp = px.line(df.sort_values("DateTime"),
                               x="DateTime",
                               y="temp",
                               title="Temperature Trend")
            st.plotly_chart(fig_temp, use_container_width=True)

            # Humidity Graph
            fig_humi = px.line(df.sort_values("DateTime"),
                               x="DateTime",
                               y="humi",
                               title="Humidity Trend")
            st.plotly_chart(fig_humi, use_container_width=True)

            # Gas Graph
            fig_gas = px.line(df.sort_values("DateTime"),
                              x="DateTime",
                              y="gas",
                              title="CO Gas Trend")
            st.plotly_chart(fig_gas, use_container_width=True)

            # Download CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "warehouse_data.csv", "text/csv")

    time.sleep(REFRESH_INTERVAL)
