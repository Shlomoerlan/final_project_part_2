import folium
from folium.plugins import HeatMapWithTime, HeatMap
import os

BASE_PATH = r'C:\Users\1\PycharmProjects\final_project_analyze_part_2\app'
TEMPLATE_PATH = os.path.join(BASE_PATH, 'templates')


def is_valid_coordinate(value):
    try:
        float_val = float(value)
        return (
                float_val is not None and
                float_val != 0 and
                -90 <= float_val <= 90
        )
    except (TypeError, ValueError):
        return False


def save_map(m, map_type='standard', time_range='month'):
    os.makedirs(TEMPLATE_PATH, exist_ok=True)

    filename = f'terror_heatmap_{map_type}_{time_range}.html'
    filepath = os.path.join(TEMPLATE_PATH, filename)

    m.save(filepath)
    return filepath


def create_heatmap(data, map_type='standard', time_range='month'):
    if not data:
        raise ValueError("No valid event locations found")

    m = folium.Map(location=[0, 0], zoom_start=2)

    valid_data = [
        [float(point.latitude), float(point.longitude)]
        for point in data
        if is_valid_coordinate(point.latitude) and
           is_valid_coordinate(point.longitude)
    ]

    if not valid_data:
        raise ValueError("No valid coordinates found in the data")

    if map_type == 'time':
        years = sorted(set(point.iyear for point in data))
        time_layers = []

        for year in years:
            year_data = [
                [float(point.latitude), float(point.longitude)]
                for point in data
                if point.iyear == year and
                   is_valid_coordinate(point.latitude) and
                   is_valid_coordinate(point.longitude)
            ]
            if year_data:
                time_layers.append(year_data)

        if not time_layers:
            raise ValueError("No valid time-based data found")

        HeatMapWithTime(
            time_layers,
            index=[str(year) for year in years],
            auto_play=True,
            max_opacity=0.8
        ).add_to(m)
    else:
        HeatMap(
            valid_data,
            radius=15,
            blur=10,
            max_zoom=1
        ).add_to(m)

    return save_map(m, map_type, time_range)
