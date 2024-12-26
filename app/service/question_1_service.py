import base64
from typing import Optional, List, Tuple, Dict, Any
from toolz import reduce
from app.db.database import session_maker
from app.repository.question_1_repository import create_query_for_attack_types
import plotly.graph_objects as go


def get_attack_types_severity(top_n: Optional[int] = None) -> List[Tuple[str, float]]:
    with session_maker() as session:
        return create_query_for_attack_types(session, top_n)


def display_attack_types_severity(top_n: Optional[int] = None) -> list[dict[Any, Any]]:
    results = get_attack_types_severity(top_n)
    return [{attack_type: score} for attack_type, score in results]


def merge_dicts(dicts: List[Dict]) -> Dict:
    return reduce(lambda x, y: {**x, **y}, dicts, {})


def create_bar_image_src(data: Dict[str, float], title: str = "Attack Types Severity") -> str:
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(data.keys()),
                y=list(data.values()),
                marker_color='darkred'
            )
        ],
        layout=go.Layout(
            title=title,
            xaxis_title="Attack Type",
            yaxis_title="Severity",
            template="plotly_dark"
        )
    )
    img_bytes = fig.to_image(format="png", scale=2)
    base64_img = base64.b64encode(img_bytes).decode('utf-8')
    return f"data:image/png;base64,{base64_img}"
