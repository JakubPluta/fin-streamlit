import datetime, time
from requests import HTTPError
import logging
import numpy as np
import streamlit as st
import plotly.express as px


def data_cleaner(data):
    data.drop(["reportedCurrency"], inplace=True)
    cols = data.select_dtypes(exclude='int').columns.to_list()
    data[cols] = data[cols].astype('str')
    data = data.replace(['None', "0", 0], np.nan).dropna(how='all')
    return data


def financial_statement_chart(chart, data, categories):
    if chart:
        chosen_category = st.selectbox("What category, do you want to analyze ? ", categories)
        if chosen_category:
            category_df = data.loc[chosen_category].values
            year = data.loc["fiscalDateEnding"].values
            chart = px.bar(x=year, y=category_df, text=category_df, color=year,
                           color_discrete_sequence=px.colors.qualitative.Antique, labels={"x":"Year", "y": chosen_category})
            chart.update_traces(texttemplate='%{text:.2s}', textposition='outside')

            chart.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.531,
                title="",
                font_size=10
            ))
            st.plotly_chart(figure_or_data=chart)


def create_unix_timestamps(days=365):
    today = datetime.date.today()
    unixtime_today = time.mktime(today.timetuple())
    years_before = today - datetime.timedelta(days=days)
    unix_time_before = time.mktime(years_before.timetuple())
    return int(unixtime_today), int(unix_time_before)


def create_time_period_in_ymd_format(days=365):
    today = datetime.date.today().strftime("%Y-%m-%d")
    year_before = datetime.date.today() - datetime.timedelta(days)
    year_before = year_before.strftime("%Y-%m-%d")
    return today, year_before


def create_logger():
    logging.basicConfig(level="INFO")
    logger = logging.getLogger(__name__)
    return logger


def validate_http_status(response) -> None:
    """
    Validate if Request Status = 200 else Raise an Exception.
    """
    logger = create_logger()
    status_code = response.status_code
    message = response.text

    if response.status_code != 200:
        raise HTTPError(message)
    logger.debug("Request Successful: {}".format(status_code))
