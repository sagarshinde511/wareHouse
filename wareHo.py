import streamlit as st
import pandas as pd
import mysql.connector
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# -------------------- CONFIG --------------------
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students"
}

USERNAME = "admin"
PASSWORD = "admin"

# -------------------- AUTO REFRESH (10 sec) --------------------
st_autorefresh(interval=10000, key="refresh")

# -------------------- LOGIN SYSTEM --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🍇 Warehouse Monitoring Login")
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

# -------------------- DASHBOARD --------------------
st.title("🍇 Grapes Warehouse Monitoring Dashboard")

df = fetch_data()

if df.empty:
    st.warning("No data available")
else:
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df_sorted = df.sort_values("DateTime")

    # -------- Latest Data --------
    st.subheader("Latest Readings")
    st.dataframe(df.head(10), use_container_width=True)

    # -------- Combined Graph --------
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted["DateTime"],
        y=df_sorted["temp"],
        name="Temperature (°C)",
        yaxis="y1"
    ))

    fig.add_trace(go.Scatter(
        x=df_sorted["DateTime"],
        y=df_sorted["humi"],
        name="Humidity (%)",
        yaxis="y2"
    ))

    fig.add_trace(go.Scatter(
        x=df_sorted["DateTime"],
        y=df_sorted["gas"],
        name="CO Gas",
        yaxis="y3"
    ))

    fig.update_layout(
        title="Warehouse Environmental Monitoring",
        xaxis=dict(title="DateTime"),

        yaxis=dict(
            title="Temperature (°C)",
            side="left"
        ),

        yaxis2=dict(
            title="Humidity (%)",
            overlaying="y",
            side="right"
        ),

        yaxis3=dict(
            title="CO Gas",
            overlaying="y",
            side="right",
            position=0.95
        ),

        legend=dict(x=0.01, y=0.99),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------- CSV Download --------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Full Data CSV", csv, "warehouse_data.csv", "text/csv")
