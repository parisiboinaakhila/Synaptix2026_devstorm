import streamlit as st
import random
import pandas as pd

# Soil → Farming mapping
farming_options = {
    "Sandy": ["Groundnut", "Cotton", "Millets"],
    "Clay": ["Rice", "Sugarcane", "Wheat"],
    "Loamy": ["Vegetables", "Fruits", "Pulses"],
    "Saline": ["Barley", "Date Palm", "Fodder"]
}

# Seasonal ranges
seasonal_conditions = {
    "Summer": {"temp": (30, 45), "humidity": (20, 50), "soil": (10, 30)},
    "Rainy": {"temp": (25, 35), "humidity": (60, 90), "soil": (40, 70)},
    "Winter": {"temp": (15, 25), "humidity": (30, 60), "soil": (20, 40)}
}

# Default season mapping
default_season = {
    "Sandy": "Summer",
    "Clay": "Rainy",
    "Loamy": "Winter",
    "Saline": "Summer"
}

# CSI calculation
def calculate_csi(temp, hum, soil):
    w1, w2, w3 = 0.4, 0.3, 0.3
    temp_score = (temp - 20) / 20 * 100
    hum_score = (100 - hum)
    soil_score = (60 - soil)
    csi = w1 * temp_score + w2 * hum_score + w3 * soil_score
    return round(csi, 2)

# Language dictionary
translations = {
    "English": {
        "title": "🌱 Smart Farming Web Application",
        "soil_select": "Choose Soil Type",
        "farming_select": "Choose Farming Type",
        "season_auto": "Season automatically set to",
        "threshold": "Stress Alert Threshold (CSI)",
        "generate": "Generate Dataset",
        "download": "Download Dataset as CSV",
        "alert": "⚠️ ALERT: Crop under stress!",
        "disease": "🌿 Plant Disease Detection",
        "camera": "Take a photo of the plant",
        "disease_alert": "🚨 Disease detected: Leaf Spot",
        "medicine": "Recommended Medicine: Copper Fungicide",
        "dosage": "Dosage: 2g per litre, apply in evening"
    },
    "Telugu": {
        "title": "🌱 స్మార్ట్ వ్యవసాయ వెబ్ అప్లికేషన్",
        "soil_select": "మట్టి రకం ఎంచుకోండి",
        "farming_select": "వ్యవసాయం రకం ఎంచుకోండి",
        "season_auto": "సీజన్ ఆటోమేటిక్‌గా సెట్ చేయబడింది",
        "threshold": "ఒత్తిడి హెచ్చరిక పరిమితి (CSI)",
        "generate": "డేటాసెట్ సృష్టించండి",
        "download": "డేటాసెట్ CSV డౌన్‌లోడ్",
        "alert": "⚠️ హెచ్చరిక: పంట ఒత్తిడిలో ఉంది!",
        "disease": "🌿 మొక్క వ్యాధి గుర్తింపు",
        "camera": "మొక్క ఫోటో తీయండి",
        "disease_alert": "🚨 వ్యాధి గుర్తించబడింది: Leaf Spot",
        "medicine": "సిఫార్సు చేసిన మందు: Copper Fungicide",
        "dosage": "డోసేజ్: లీటరుకు 2g, సాయంత్రం వేయండి"
    },
    "Hindi": {
        "title": "🌱 स्मार्ट खेती वेब एप्लिकेशन",
        "soil_select": "मिट्टी का प्रकार चुनें",
        "farming_select": "खेती का प्रकार चुनें",
        "season_auto": "मौसम स्वतः सेट किया गया",
        "threshold": "तनाव चेतावनी सीमा (CSI)",
        "generate": "डेटासेट बनाएं",
        "download": "CSV डेटा सेट डाउनलोड करें",
        "alert": "⚠️ चेतावनी: फसल तनाव में है!",
        "disease": "🌿 पौध रोग पहचान",
        "camera": "पौधे की फोटो लें",
        "disease_alert": "🚨 रोग पाया गया: Leaf Spot",
        "medicine": "अनुशंसित दवा: Copper Fungicide",
        "dosage": "खुराक: 2g प्रति लीटर, शाम को लगाएं"
    }
}

# --- UI ---
language = st.selectbox("Language", ["English", "Telugu", "Hindi"])
t = translations[language]

st.title(t["title"])

soil_type = st.selectbox(t["soil_select"], list(farming_options.keys()))
farming_type = st.selectbox(t["farming_select"], farming_options[soil_type])
season = default_season[soil_type]
st.info(f"{t['season_auto']}: {season}")

threshold = st.slider(t["threshold"], 0, 100, 70)

if st.button(t["generate"]):
    cond = seasonal_conditions[season]
    data = []
    for day in range(1, 11):  # 10 days sample dataset
        temp = random.uniform(*cond["temp"])
        hum = random.uniform(*cond["humidity"])
        soil = random.uniform(*cond["soil"])
        csi = calculate_csi(temp, hum, soil)
        data.append({
            "Day": day,
            "SoilType": soil_type,
            "FarmingType": farming_type,
            "Season": season,
            "Temperature": round(temp, 2),
            "Humidity": round(hum, 2),
            "SoilMoisture": round(soil, 2),
            "CSI": csi
        })
    df = pd.DataFrame(data)
    st.write(df)

    # Alerts
    for i, row in df.iterrows():
        if row["CSI"] > threshold:
            st.error(f"{t['alert']} (Day {row['Day']}, CSI={row['CSI']})")

    # Graph
    st.subheader("📊 Trends")
    st.line_chart(df[["Temperature", "Humidity", "SoilMoisture", "CSI"]])

    # Download
    st.download_button(
        label=t["download"],
        data=df.to_csv(index=False),
        file_name=f"{soil_type}_{farming_type}_{season}.csv",
        mime="text/csv"
    )

# --- Plant Disease Detection (Camera Input) ---
st.subheader(t["disease"])
img = st.camera_input(t["camera"])
if img:
    # Stub: Here you would load a ML model and run prediction
    st.warning(t["disease_alert"])
    st.write(t["medicine"])
    st.write(t["dosage"])
