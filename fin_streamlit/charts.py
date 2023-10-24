import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_candle_chart(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data["Date"],
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                increasing_line_color="green",
                decreasing_line_color="red",
            )
        ]
    )
    fig.update_layout(title="Stock Quotes")
    return fig


def get_barchart(data: pd.DataFrame, category: str) -> go.Figure:
    category_values = data.loc[category].values
    year_values = data.columns.values
    fig = px.bar(
        x=year_values,
        y=category_values,
        text=category_values,
        color=year_values,
        color_discrete_sequence=px.colors.qualitative.Antique,
        labels={"x": "Year", "y": category},
    )
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.531,
            title="",
            font_size=10,
        )
    )
    return fig
