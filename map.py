import folium
import json
import polyline 

with open("data/clean/segments.json", "r") as f:
    segments = json.load(f)

# Ustvarimo seznam poti iz segmentov
poti = []
for segment in segments:
    pot = polyline.decode(segment["map"].get("polyline", ""))
    # Dodamo točke poti v seznam poti
    poti.append([(point[0], point[1]) for point in pot])


# Ustvarimo osnovni zemljevid
zemljevid = folium.Map(location=[46.0511, 14.5051], zoom_start=13)

# Dodamo poti na zemljevid
for pot in poti:
    folium.PolyLine(pot, color="blue", weight=2.5, opacity=1).add_to(zemljevid)

# Shranimo zemljevid v HTML datoteko
zemljevid.save("zemljevid.html")