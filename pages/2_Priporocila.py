import streamlit as st
import json
import random
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
import polyline

st.set_page_config(page_title="Priporočeni segmenti", layout="wide")
st.title("🚴 Priporočeni povezani segmenti")

st.markdown("""
Na tej strani lahko najdete priporočene povezane segmente kolesarjenja glede na vaše želje.
Izberite regijo, maksimalno zahtevnost vzpona, skupno maksimalno dolžino izbranih segmentov in tip površine po kateri bi kolesarili (asfaltirana - površine kjer je mogoče kolesariti s cestnim kolesom, mešano - tudi makadamske poti), nato pa kliknite gumb za iskanje.
Izbrani segmenti bodo prikazani na zemljevidu in pod zemljevidom pa podrobnosti o njih.""")


@st.cache_data
def load_segments():
    with open("data/clean/segments_with_surface.json", "r", encoding="utf-8") as f:
        return json.load(f)

segments = load_segments()

# --- Sidebar ---
st.sidebar.header("Filtri za priporočila")
all_regions = sorted(set(r for s in segments for r in s["regija"]))
selected_region = st.sidebar.selectbox("Izberi regijo:", all_regions)
max_climb = st.sidebar.slider("Največja zahtevnost (težavnost vzpona)", 0, 5, 2)
max_distance = st.sidebar.slider("Največja dolžina skupnih segmentov (v metrih)", 10000, 100000, 10000, step=2000)

surface_type = st.sidebar.selectbox(
    "Izberi tip površine:",
    options=["Asfaltirana", "Mešana"],
    index=0
)

ALLOWED_SURFACES_ASPHALT = {"asphalt", "paved", "concrete"}

def is_surface_acceptable(segment, surface_type):
    surfaces = {segment.get("surface", "")}
    if surface_type == "Asfaltirana":
        return all(s in ALLOWED_SURFACES_ASPHALT for s in surfaces)
    return True  # "Mešana" dovoljuje vse

def are_segments_connectable(seg1, seg2, max_km=10.0):
    end = tuple(seg1["end_latlng"])
    start = tuple(seg2["start_latlng"])
    return geodesic(end, start).km <= max_km

def find_nearby_segments(segments, region, max_climb, max_distance, surface_type):
    candidates = [
        s for s in segments
        if region in s["regija"]
        and s["custom_climb_category"] <= max_climb
        and is_surface_acceptable(s, surface_type)
    ]
    random.shuffle(candidates)

    for start_seg in candidates:
        route = [start_seg]
        total_dist = start_seg["distance"]
        used_ids = {start_seg["id"]}

        while total_dist < max_distance - 5000:
            nearby = [
                s for s in candidates
                if s["id"] not in used_ids
                and s["custom_climb_category"] <= max_climb
                and is_surface_acceptable(s, surface_type)
                and are_segments_connectable(route[-1], s)
            ]
            if not nearby:
                break
            next_seg = random.choice(nearby)
            route.append(next_seg)
            used_ids.add(next_seg["id"])
            total_dist += next_seg["distance"]

        if len(route) >= 2:
            return route

    return None

if st.sidebar.button("🔍 Poišči povezane segmente"):
    recommended = find_nearby_segments(segments, selected_region, max_climb, max_distance, surface_type)
    if recommended:
        st.session_state["recommended_route"] = recommended
    else:
        st.session_state["recommended_route"] = None

if "recommended_route" in st.session_state:
    recommended = st.session_state["recommended_route"]
    if recommended:
        total_km = sum(s["distance"] for s in recommended) / 1000
        st.subheader(f"🔁 Najdeni segmenti – skupna dolžina: {total_km:.1f} km")

        m = folium.Map(location=recommended[0]["start_latlng"], zoom_start=13)
        for seg in recommended:
            points = seg["map"]["polyline"]
            try:
                coords = polyline.decode(points)
                folium.PolyLine(coords, tooltip=seg["name"], color="blue", weight=5).add_to(m)
            except Exception as e:
                continue

        st_folium(m, width=800, height=600)

        with st.expander("📋 Podrobnosti poti"):
            for seg in recommended:
                st.markdown(f"**{seg['name']}**  ")
                st.markdown(f"- Razdalja: `{seg['distance']:.1f} m`  ")
                st.markdown(f"- Povprečen naklon: `{seg['average_grade']}%`  ")
                st.markdown(f"- Višinska razlika: `{seg['elevation_high'] - seg['elevation_low']:.1f} m`  ")
                st.markdown(f"- Težavnost: `{seg['custom_climb_category']}`  ")
                st.markdown(f"- Površina: `{seg['surface']}`  ")

                if seg.get("elevation_profiles") and seg["elevation_profiles"].get("light_url"):
                    st.image(seg["elevation_profiles"]["light_url"], caption="Višinski profil")

                st.markdown("---")
    else:
        st.warning("Ni bilo mogoče najti povezane skupine segmentov za dane parametre.")
