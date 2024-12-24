from collections import defaultdict
import folium
import numpy as np
from app.repository.question_6_repository import get_region_attack_data, get_region_centers


def calculate_attack_changes(region_data):
    region_changes = defaultdict(list)
    for result in region_data:
        region_changes[result.region_name].append({
            'year': result.year,
            'count': result.attack_count
        })

    change_results = []
    for region, data in region_changes.items():
        if len(data) > 1:
            previous_year = data[-2]
            current_year = data[-1]
            change_percentage = (
                (current_year['count'] - previous_year['count']) / previous_year['count']
            ) * 100

            change_results.append({
                'region': region,
                'previous_year': previous_year['year'],
                'current_year': current_year['year'],
                'previous_count': previous_year['count'],
                'current_count': current_year['count'],
                'change_percentage': round(change_percentage, 2)
            })
    return sorted(change_results, key=lambda x: abs(x['change_percentage']), reverse=True)

def generate_map(region_changes, region_centers):
    m = folium.Map(location=[0, 0], zoom_start=2)
    for change in region_changes:
        region_center = next((center for center in region_centers if center.region_name == change['region']), None)

        if region_center and not np.isnan(region_center.avg_latitude) and not np.isnan(region_center.avg_longitude):
            color = 'green' if change['change_percentage'] > 0 else 'red'
            popup_text = f"""
            Region: {change['region']}
            Previous Year: {change['previous_year']} (Attacks: {change['previous_count']})
            Current Year: {change['current_year']} (Attacks: {change['current_count']})
            Change: {change['change_percentage']}%
            """

            folium.CircleMarker(
                location=[region_center.avg_latitude, region_center.avg_longitude],
                radius=abs(change['change_percentage']) / 2,
                popup=popup_text,
                color=color,
                fill=True,
                fillColor=color
            ).add_to(m)
    return m

def save_map(m, filename=r'C:\Users\1\PycharmProjects\final_project_analyze_part_2\app\templates\terror_attack_changes_map.html'):
    m.save(filename)

def create_region_attack_change_map(session, display_type='all'):
    region_data = get_region_attack_data(session)
    region_changes = calculate_attack_changes(region_data)
    if display_type == 'top5':
        region_changes = region_changes[:5]

    region_centers = get_region_centers(session)

    m = generate_map(region_changes, region_centers)

    save_map(m)
