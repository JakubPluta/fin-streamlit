import streamlit as st
import numpy as np
import pandas as pd
from client import AlphaVantageClient

client = AlphaVantageClient()


st.title('Stock Analyzer')

symbol = "FB"

company_base = ["Exchange" ,"Currency", "Country", "Sector", "Technology", "Industry", "Address",
                "FullTimeEmployees", "MarketCapitalization"]

not_needed_elements = ['Symbol','AssetType','Description',"Name","FiscalYearEnd"]

@st.cache
def load_company_info(symbol):
    return client.company_overview(symbol)


@st.cache
def load_balance_sheet(symbol):
    return client.balance_sheet(symbol)

@st.cache
def look_for_company(keyword):
    return client.search(keyword).get("bestMatches")


@st.cache
def load_income_statement(symbol):
    return client.income_statement(symbol)


user_input = st.text_input("Input key")

company = look_for_company(user_input)

if company is not None:

    names = []
    symbols = []

    for item in company:
        symbols.append(item.get("1. symbol"))
        names.append(f"{item.get('2. name')} --> ({item.get('1. symbol')})")

    mapping = dict(zip(names,symbols))

    select_box = st.selectbox(label="Choose stock that you want", options=names)
    symbol = mapping.get(select_box)

data = load_company_info(symbol)
st.subheader(f'{data.get("Name")} Overview')
st.write(data.get("Description"))
table_dict = {k: v for k, v in data.items() if k in company_base}

for k, v in table_dict.items():
    st.write(f"* {k}: {v}")


st.subheader('Key Metrics')

table_dict2 = {k: v for k, v in data.items() if k not in (company_base + not_needed_elements)}
df2 = pd.DataFrame(table_dict2.items())
df2.columns = ["Label", "Value"]
st.dataframe(df2)


if st.checkbox('Show Balance Sheet'):
    st.subheader('Balance Sheet')
    data2 = load_balance_sheet(symbol).get("annualReports")
    data2 = pd.json_normalize(data2).T
    data2.columns = data2.iloc[0]
    st.write(data2)

if st.checkbox('Show Income Statement'):
    st.subheader('Income Statement')
    data2 = load_income_statement(symbol).get("annualReports")
    data2 = pd.json_normalize(data2).T
    data2.columns = data2.iloc[0]
    st.write(data2)

if st.checkbox('Show Cash Flow'):
    st.subheader('Cash Flow')
    data2 = load_income_statement(symbol).get("annualReports")
    data2 = pd.json_normalize(data2).T
    data2.columns = data2.iloc[0]
    st.write(data2)

st.empty()




