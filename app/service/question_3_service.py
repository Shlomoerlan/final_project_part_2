from typing import Optional, List, Tuple

from app.repository.question_3_repository import get_top_groups_by_casualties
import plotly.graph_objects as go
import base64

def display_top_groups_by_casualties(top_n: Optional[int] = None) -> list[tuple[str, float]]:
    return get_top_groups_by_casualties(top_n)


def create_bar_chart(data, title="Attack Types Severity"):
    # Extract keys and values from the list of tuples
    keys = [item[0] for item in data]
    values = [item[1] for item in data]

    # Create the bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=keys,
                y=values,
                marker_color='darkred'
            )
        ],
        layout=go.Layout(
            title=title,
            xaxis_title="Organizations",
            yaxis_title="Attack Counts",
            template="plotly_dark"
        )
    )
    img_bytes = fig.to_image(format="png", scale=2)
    base64_img = base64.b64encode(img_bytes).decode('utf-8')
    return f"data:image/png;base64,{base64_img}"



if __name__ == "__main__":
    display_top_groups_by_casualties(top_n=5)
