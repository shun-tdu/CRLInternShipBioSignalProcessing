import pandas as pd
import plotly.express as px


def plot_data(df: pd.DataFrame, title: str = "Signal Data"):
    """
    データフレームをインタラクティブなグラフとして描画する．
    :param df: 描画するデータフレーム [-]
    :param title: グラフのタイトル
    """
    if df.empty:
        return px.line(title="データがありません")

    fig = px.line(df, x=df.index,y=df.columns, title=title)
    fig.update_layout(
        xaxis_title = 'Time',
        yaxis_title = 'Value',
        legend_title = 'Signals'
    )
    return fig
