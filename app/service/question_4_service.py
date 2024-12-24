from typing import List, Tuple
from toolz import pipe, curry
from toolz.curried import filter
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_matrix(data: List[Tuple[str, str, int]]) -> pd.DataFrame:
    filtered_data = pipe(
        data,
        curry(filter)(lambda x: 'Unknown' not in (x[0], x[1]))
    )

    matrix_dict = defaultdict(lambda: defaultdict(int))

    for attack_type, target, count in filtered_data:
        matrix_dict[attack_type][target] = count

    df = pd.DataFrame(matrix_dict).fillna(0)

    return df


def calculate_correlation(df: pd.DataFrame) -> pd.DataFrame:
    return df.corr()


def create_heatmap(corr_matrix: pd.DataFrame) -> plt.Figure:
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap='coolwarm',
        vmin=-1,
        vmax=1,
        center=0
    )
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    return plt.gcf()

def analyze_correlation(data: List[Tuple[str, str, int]]) -> Tuple[pd.DataFrame, plt.Figure]:
    matrix = pipe(
        data,
        create_matrix,
        calculate_correlation
    )

    fig = create_heatmap(matrix)
    return matrix, fig

