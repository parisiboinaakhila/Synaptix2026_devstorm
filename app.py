import streamlit as st
import random
import statistics
import pandas as pd

# --- Functions ---
def get_sensor_data():
    temperature = random.uniform(20, 40)
    humidity = random.uniform(20, 80)
    soil_moisture = random.uniform(10, 60)
    return temperature, humidity, soil_moisture

def calculate_csi(temp, hum, soil):
    w1, w2, w3 = 0.4, 0.3, 0.3
    temp_score = (temp - 20) / 20 * 100
    hum_score = (100 - hum)
    soil_score = (60 - soil)
    csi = w1*temp_score + w2*hum_score + w3*soil_score
    return round(csi, 2)

def detect_anomaly(data_series, new_value):
    mean = statistics.mean(data_series)
    stdev = statistics.pstdev(data_series)
    if stdev == 0:
        return False
    z_score = (new_value - mean) / stdev
    return abs(z_score) > 2

# --- Language dictionary ---
translations = {
    "English": {
        "title": "🌱 Farm Micro-Climate Monitoring Dashboard",
        "temp": "Temperature",
        "hum": "Humidity",
        "soil": "Soil Moisture",
        "csi": "Crop Stress Index",
        "alert": "⚠️ ALERT: Crop under stress!",
        "anomaly": "🚨 Anomaly detected in temperature!",
        "combined_chart": "📊 Combined Trends (Temperature, Humidity, Soil Moisture, CSI)"
    },
    "Telugu": {
        "title": "🌱 వ్యవసాయ సూక్ష్మ-వాతావరణ పర్యవేక్షణ డాష్‌బోర్డ్",
        "temp": "ఉష్ణోగ్రత",
        "hum": "ఆర్ద్రత",
        "soil": "మట్టి తేమ",
        "csi": "పంట ఒత్తిడి సూచిక",
        "alert": "⚠️ హెచ్చరిక: పంట ఒత్తిడిలో ఉంది!",
        "anomaly": "🚨 ఉష్ణోగ్రతలో అసాధారణం గుర్తించబడింది!",
        "combined_chart": "📊 కలిపిన ధోరణులు (ఉష్ణోగ్రత, ఆర్ద్రత, మట్టి తేమ, పంట ఒత్తిడి సూచిక)"
    },
    "Hindi": {
        "title": "🌱 कृषि सूक्ष्म-जलवायु निगरानी डैशबोर्ड",
        "temp": "तापमान",
        "hum": "आर्द्रता",
        "soil": "मिट्टी की नमी",
        "csi": "फसल तनाव सूचकांक",
        "alert": "⚠️ चेतावनी: फसल तनाव में है!",
        "anomaly": "🚨 तापमान में असामान्यता पाई गई!",
        "combined_chart": "📊 संयुक्त प्रवृत्तियाँ (तापमान, आर्द्रता, मिट्टी की नमी, फसल तनाव सूचकांक)"
    }
}

# --- Streamlit UI ---
language = st.selectbox("Choose Language", ["English", "Telugu", "Hindi"])
t = translations[language]

st.title(t["title"])

threshold = st.slider("Stress Alert Threshold (CSI)", 0, 100, 70)

if "data" not in st.session_state:
    st.session_state.data = []

if st.button("Generate New Reading"):
    temp, hum, soil = get_sensor_data()
    csi = calculate_csi(temp, hum, soil)
    anomaly = detect_anomaly([d["Temp"] for d in st.session_state.data] or [temp], temp)

    st.session_state.data.append({
        "Temp": temp,
        "Humidity": hum,
        "SoilMoisture": soil,
        "CSI": csi
    })

    st.write(f"**{t['temp']}:** {temp:.2f}")
    st.write(f"**{t['hum']}:** {hum:.2f}")
    st.write(f"**{t['soil']}:** {soil:.2f}")
    st.write(f"**{t['csi']}:** {csi}")

    if csi > threshold:
        st.error(t["alert"])
    if anomaly:
        st.warning(t["anomaly"])

# --- Combined Graph ---
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    st.subheader(t["combined_chart"])
    st.line_chart(df[["Temp", "Humidity", "SoilMoisture", "CSI"]])

    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv(index=False),
        file_name="farm_data.csv",
        mime="text/csv"
    )
