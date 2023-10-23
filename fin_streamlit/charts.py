import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def quotes_chart(data):
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
    st.plotly_chart(figure_or_data=fig)


def financial_statement_chart(chart, data, categories):
    if chart:
        chosen_category = st.selectbox(
            "What category, do you want to analyze ? ", categories
        )
        if chosen_category:
            category_df = data.loc[chosen_category].values
            year = data.columns.values
            chart = px.bar(
                x=year,
                y=category_df,
                text=category_df,
                color=year,
                color_discrete_sequence=px.colors.qualitative.Antique,
                labels={"x": "Year", "y": chosen_category},
            )
            chart.update_traces(texttemplate="%{text:.2s}", textposition="outside")

            chart.update_layout(
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
            st.plotly_chart(figure_or_data=chart)
