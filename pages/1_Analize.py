import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import plotly.express as px
from PIL import Image

# -- Nastavitve strani --
st.set_page_config(page_title="Analiza in vizualizacije podatkov", layout="wide")

# -- Nalaganje podatkov --
with open("data/clean/segments_with_surface.json", "r", encoding="utf-8") as f:
    segments = json.load(f)
segments_df = pd.DataFrame(segments)

# -- Izračuni za osnovne metrike --
total_effort_count = sum(segment.get("effort_count", 0) for segment in segments)
average_effort_count = total_effort_count / len(segments)
top_segments = sorted(segments, key=lambda x: x.get("effort_count", 0), reverse=True)[:10]
top_segments_df = pd.DataFrame(top_segments)[["name", "effort_count"]]
top_segments_df.columns = ["Segment Name", "Effort Count"]
top_segments_df.index += 1
top_segments_df.index.name = "Rank"

region_effort_counts = {}
for segment in segments:
    region_list = segment.get("regija")
    effort_count = segment.get("effort_count", 0)
    for region in region_list:
        if region not in region_effort_counts:
            region_effort_counts[region] = {"total_effort": 0, "segment_count": 0}
        region_effort_counts[region]["total_effort"] += effort_count
        region_effort_counts[region]["segment_count"] += 1

region_effort_counts_df = pd.DataFrame.from_dict(region_effort_counts, orient="index")
region_effort_counts_df.reset_index(inplace=True)
region_effort_counts_df.columns = ["Region", "Total Effort Count", "Segment Count"]
region_effort_counts_df["Average Effort Count"] = region_effort_counts_df["Total Effort Count"] / region_effort_counts_df["Segment Count"]
region_effort_counts_df.sort_values(by="Average Effort Count", ascending=False, inplace=True)
region_effort_counts_df.reset_index(drop=True, inplace=True)
region_effort_counts_df.index += 1
region_effort_counts_df.index.name = "Rank"

# -- Priprava slik (če so že generirane) --
def load_image(path):
    return Image.open(path)

# -- Začetek aplikacije --
st.title("Geografska analiza rekreativnega kolesarjenja v Sloveniji")

st.markdown("""
Ta stran prikazuje ključne analize in vizualizacije podatkov o kolesarskih segmentih pridobljenih iz aplikacije Strava.
""")

# -- Prva vrstica: osnovne metrike in top segmenti --
col1, col2 = st.columns(2)

with col1:
    st.subheader("Skupno število voženj")
    st.metric("Total effort count", f"{total_effort_count:,}")
    st.metric("Povprečno na segment", f"{average_effort_count:.1f}")

with col2:
    st.subheader("Top 10 segmentov po številu voženj")
    st.dataframe(top_segments_df, use_container_width=True)

# -- Druga vrstica: boxplot in histogram --
col3, col4 = st.columns(2)

with col3:
    st.subheader("Boxplot števila voženj na segment")
    st.image("data/plots/boxplot_effort_count.png", use_container_width=True)

with col4:
    st.subheader("Histogram povprečnega števila voženj po občinah")
    st.image("data/plots/histogram_avg_effort_count.png", use_container_width=True)

# -- Tretja vrstica: zemljevid in eksponentna porazdelitev --
col5, col6 = st.columns(2)

with col5:
    st.subheader("Zemljevid: povprečno število voženj po občinah")
    st.image("data/plots/avg_effort_map_by_municipality.png", use_container_width=True)

with col6:
    st.subheader("Eksponentna porazdelitev povprečnega števila voženj")
    st.image("data/plots/effort_count_exponential_fit.png", use_container_width=True)

# -- Četrta vrstica: povprečje po kategorijah in površinah --
col7, col8 = st.columns(2)

with col7:
    st.subheader("Povprečno število voženj po kategorijah vzponov")
    st.image("data/plots/avg_effort_per_category.png", use_container_width=True)

with col8:
    st.subheader("Povprečno število voženj po površini")
    st.image("data/plots/avg_effort_per_surface.png", use_container_width=True)

# -- Peta vrstica: število segmentov po površini in regiji --
col9, col10 = st.columns(2)

with col9:
    st.subheader("Število segmentov po površini")
    st.image("data/plots/segments_count_per_surface.png", use_container_width=True)

with col10:
    st.subheader("Segmenti po regijah")
    st.dataframe(region_effort_counts_df, use_container_width=True)

# -- Šesta vrstica: povprečno število voženj po regijah --
col11, col12 = st.columns(2)

with col11:
    st.subheader("Povprečno število voženj po regijah")
    st.image("data/plots/avg_effort_per_region.png", use_container_width=True)

with col12:
    st.subheader("Segmenti po climb_score in effort_count")
    st.image("data/plots/climb_score_vs_effort_count.png", use_container_width=True)

# -- Dodatne možnosti: prikaz surovih podatkov --
with st.expander("Prikaži surove podatke (JSON)"):
    st.json(segments)
