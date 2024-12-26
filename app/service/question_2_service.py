from typing import List, Tuple
import folium


def create_map_with_regions(data: List[Tuple[str, float]]):
    REGION_COORDINATES = {
        "Middle East & North Africa": [26.0, 29.0],
        "South Asia": [28.0, 77.0],
        "Sub-Saharan Africa": [-1.5, 30.0],
        "Europe": [54.0, 15.0],
        "North America": [37.1, -95.7],
    }

    m = folium.Map(location=[0, 0], zoom_start=2)

    for region, avg_casualties in data:
        coords = REGION_COORDINATES.get(region, [0, 0])
        folium.CircleMarker(
            location=coords,
            radius=avg_casualties / 10,
            popup=f"{region}: {avg_casualties:.2f} casualties",
            color='blue',
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

    m.show_in_browser()
