import streamlit as st
import numpy as np
import pandas as pd
from client import AlphaVantageClient

client = AlphaVantageClient()

st.title('Stock Analyzer')

symbol = "FB"

company_base = ["Exchange" ,"Currency", "Country", "Sector", "Technology", "Industry", "Address",
                "FullTimeEmployees", "MarketCapitalization"]


@st.cache
def load_company_info(symbol):
    return client.company_overview(symbol)


@st.cache
def load_balance_sheet(symbol):
    return client.balance_sheet(symbol)

@st.cache
def look_for_company(keyword):
    return client.search(keyword).get("bestMatches")

user_input = st.text_input("Input key")

if user_input is not None:
    company = look_for_company(user_input)

    names = []
    symbols = []
    for item in company:
        symbols.append(item.get("1. symbol"))
        names.append(item.get("2. name"))

    mapping = dict(zip(names,symbols))

    select_box = st.selectbox(label="Choose stock that you want", options=names)
    symbol = mapping.get(select_box)
    print(symbol)
    data = load_company_info(symbol)
    st.subheader(f'{data.get("Name")} Overview')
    st.write(data.get("Description"))
    table_dict = {k: v for k, v in data.items() if k in company_base}
    for k,v in table_dict.items():
        st.write(f"* {k}: {v}")



# st.subheader('Key Metrics')
#
# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)
#



st.empty()


#
# data2 = load_balance_sheet("FB")
#
# st.subheader("Balance Sheet")
# st.write(data2)


