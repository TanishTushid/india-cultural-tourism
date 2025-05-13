import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# ------------------ PAGE SETUP ------------------
st.set_page_config(page_title="India's Cultural Lens", layout="wide")
st.sidebar.title("📂 Navigate")
page = st.sidebar.radio("Go to", [
    "Home 🏠",
    "Traditional Art 🎨",
    "Tourism Trends 📊",
    "Cultural Map 🗺️",
    "Responsible Tourism 🌿"
])

# ------------------ HOME PAGE ------------------
if page == "Home 🏠":
    st.title("🇮🇳 India's Cultural Lens")
    st.markdown("""
        Welcome to **India's Cultural Lens** — a Streamlit-powered platform that bridges **art**, **culture**, and **tourism** through **data and maps**. 🎨🛕🌏

        - 🔍 Discover traditional art forms  
        - 📊 Explore tourism trends  
        - 🗺️ Interact with cultural hotspots map  
        - 🌿 Take a pledge for responsible tourism  
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/98/Art_and_culture_banner.jpg", use_column_width=True)
    st.markdown("---")

# ------------------ TRADITIONAL ART ------------------
elif page == "Traditional Art 🎨":
    st.header("🎨 Traditional Art Forms of India")
    st.markdown("Use the filters to explore by region or type of art.")

    art_data = pd.DataFrame({
        "Art Form": ["Kathak", "Madhubani", "Bharatanatyam", "Pattachitra", "Chhau", "Warli"],
        "Region": ["North India", "Bihar", "Tamil Nadu", "Odisha", "Jharkhand", "Maharashtra"],
        "Type": ["Dance", "Painting", "Dance", "Painting", "Dance", "Painting"]
    })

    region = st.selectbox("Select Region", ["All"] + sorted(art_data["Region"].unique().tolist()))
    art_type = st.selectbox("Select Type", ["All"] + sorted(art_data["Type"].unique().tolist()))

    filtered = art_data.copy()
    if region != "All":
        filtered = filtered[filtered["Region"] == region]
    if art_type != "All":
        filtered = filtered[filtered["Type"] == art_type]

    st.dataframe(filtered, use_container_width=True)

# ------------------ TOURISM TRENDS ------------------
elif page == "Tourism Trends 📊":
    st.header("📊 Tourism Trends in India")
    st.markdown("Visualizing footfall across cultural hotspots over time. (Sample data shown here)")

    sample_data = pd.DataFrame({
        "State": ["Rajasthan", "Rajasthan", "Odisha", "Odisha", "Karnataka", "Karnataka"],
        "Month": ["Jan", "Feb", "Jan", "Feb", "Jan", "Feb"],
        "Year": [2023, 2023, 2023, 2023, 2023, 2023],
        "Visitors": [120000, 135000, 70000, 85000, 110000, 130000]
    })

    fig = px.line(sample_data, x="Month", y="Visitors", color="State", title="Monthly Tourist Visitors by State")
    st.plotly_chart(fig, use_container_width=True)

# ------------------ CULTURAL MAP ------------------
elif page == "Cultural Map 🗺️":
    st.header("🗺️ Cultural Hotspots of India")
    st.markdown("Filter by type of cultural experience (craft, temple, heritage site, etc.)")

    # Load cultural spots (from CSV or embedded sample)
    try:
        hotspots = pd.read_csv("cultural_spots.csv")
    except:
        hotspots = pd.DataFrame({
            "name": ["Hampi", "Konark Sun Temple", "Sankheda Furniture", "Channapatna Toys"],
            "state": ["Karnataka", "Odisha", "Gujarat", "Karnataka"],
            "type": ["Heritage Site", "Temple", "Craft", "Craft"],
            "latitude": [15.3350, 19.8876, 22.3702, 12.8755],
            "longitude": [76.4600, 86.0945, 73.1847, 77.2865],
            "description": [
                "UNESCO site of Vijayanagara Empire",
                "13th-century temple dedicated to Sun God",
                "Hand-painted wooden furniture",
                "Wooden toy craft called Gombegala Ooru"
            ]
        })

    hotspot_type = st.selectbox("Select Type", ["All"] + sorted(hotspots["type"].unique().tolist()))
    if hotspot_type != "All":
        hotspots = hotspots[hotspots["type"] == hotspot_type]

    m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)
    for _, row in hotspots.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"<b>{row['name']}</b><br>{row['type']}<br>{row['description']}",
            tooltip=row["name"],
            icon=folium.Icon(color="green" if row["type"] == "Craft" else "blue")
        ).add_to(m)

    st_data = st_folium(m, width=700, height=500)

# ------------------ RESPONSIBLE TOURISM ------------------
elif page == "Responsible Tourism 🌿":
    st.header("🌿 Responsible Tourism")
    st.markdown("""
        Travelling responsibly helps protect India's culture, environment, and communities.
        Take this pledge to travel with respect and care. 🌏
    """)

    st.subheader("✋ Take the Responsible Tourism Pledge")
    with st.form("pledge_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email (optional)")
        pledge = st.checkbox("I pledge to respect local culture, support eco-friendly tourism, and leave no trace.")
        submitted = st.form_submit_button("Take the Pledge")

        if submitted and pledge and name:
            st.success(f"Thank you, {name}, for taking the pledge! 🙌")
            # Optional: Save to file or database
        elif submitted and not pledge:
            st.warning("Please agree to the pledge to submit.")
        elif submitted and not name:
            st.warning("Please enter your name to continue.")
