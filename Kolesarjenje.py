import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import Popup
import polyline

st.set_page_config(layout="wide")
st.title("Kje danes kolesarim?")
# Opis strani
st.markdown("""

            
Na tej strani lahko raziskujete interaktivni zemljevid segmentov kolesarjenja v Sloveniji. 
Segmenti so prikazani kot modre črte, ki jih lahko kliknete za več informacij.
Vsak segment vsebuje podatke o dolžini, povprečnem naklonu in višinski razliki.
Za podrobnejšo analizo in vizualizacije podatkov o segmentih, si oglejte [Analiza in vizualizacije podatkov].
Če želite raziskati priporočene povezane segmente, pojdite na [Priporočeni segmenti].
""")

# Naloži podatke s segmenti
@st.cache_data
def load_data():
    return pd.read_json("data/clean/segments_with_surface.json")

data = load_data()
# Kontejner za prikaz interaktivnega zemljevida
with st.container():
    st.subheader("Zemljevid segmentov")

    m = folium.Map(location=[46.15, 14.995], zoom_start=8, tiles="CartoDB positron")

    for _, row in data.iterrows():
        if "map" in row and "polyline" in row["map"]:
            try:
                coords = polyline.decode(row["map"]["polyline"])
                popup_html = f"""
                    <strong>{row['name']}</strong><br>
                    Dolžina: {round(row['distance']/1000, 2)} km<br>
                    Povprečen naklon: {row['average_grade']} %<br>
                    Višinska razlika: {round(row['elevation_high'] - row['elevation_low'], 1)} m<br>
                    <a href='{row['elevation_profiles']['light_url']}' target='_blank'>Profil vzpona</a>
                """
                folium.PolyLine(coords, color="blue", weight=3, popup=Popup(popup_html, max_width=300)).add_to(m)
            except Exception as e:
                continue

    st_folium(m, width=1200, height=600)

