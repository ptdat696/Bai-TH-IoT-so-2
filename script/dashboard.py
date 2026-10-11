
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="IoT Sensor Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Dashboard giám sát dữ liệu IoT")
st.caption("ESP32 · Wokwi · ThingsBoard · InfluxDB")

try:
    df = pd.read_csv("iot_processed.csv", parse_dates=["time"])
except FileNotFoundError:
    st.warning("Chua co file iot_processed.csv. Hay chay preprocess.py truoc.")
    st.stop()

if df.empty:
    st.info("Chua co du lieu de hien thi.")
    st.stop()

df = df.sort_values("time")
latest = df.iloc[-1]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Nhiệt độ mới nhất",
    f"{latest['temperature']:.2f} °C"
    if pd.notna(latest["temperature"]) else "N/A",
)

c2.metric(
    "Độ ẩm mới nhất",
    f"{latest['humidity']:.2f} %"
    if pd.notna(latest["humidity"]) else "N/A",
)

c3.metric(
    "Khoảng cách mới nhất",
    f"{latest['distance_cm']:.2f} cm"
    if pd.notna(latest["distance_cm"]) else "N/A",
)

st.subheader("Biến thiên cảm biến theo thời gian")

for column, title, unit in [
    ("temperature", "Nhiệt độ", "°C"),
    ("humidity", "Độ ẩm", "%"),
    ("distance_cm", "Khoảng cách", "cm"),
]:
    st.markdown(f"**{title} ({unit})**")

    plot_df = df.set_index("time")[[column]].dropna()
    st.line_chart(plot_df)

st.subheader("So sánh dữ liệu gốc sau resampling và dữ liệu làm mượt")

for column in ["temperature", "humidity", "distance_cm"]:
    rolling_col = f"{column}_rolling_mean"

    if column in df.columns and rolling_col in df.columns:
        st.markdown(f"**{column}**")
        chart_df = df.set_index("time")[[column, rolling_col]].dropna(
            how="all"
        )
        st.line_chart(chart_df)

st.subheader("Bảng dữ liệu đã tiền xử lý")
st.dataframe(df.tail(100), use_container_width=True)

st.download_button(
    "Tải dữ liệu CSV",
    data=df.to_csv(index=False).encode("utf-8-sig"),
    file_name="iot_processed.csv",
    mime="text/csv",
)