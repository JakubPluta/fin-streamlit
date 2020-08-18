import streamlit as st
import numpy as np
import pandas as pd
from client import FinnhubClient
from settings.default import TOKEN

client = FinnhubClient(TOKEN)


st.title('Test')


@st.cache
def load_company_info(symbol):
    data = client.fetch_company(symbol)
    return pd.Series(data).to_frame().reset_index()


@st.cache
def load_balance_sheet(symbol):
    data = client.fetch_financial_statement_as_reported(symbol)
    return pd.DataFrame(data['data'][0]['report']['bs'])[['label','value']]


@st.cache
def load_income_statement(symbol):
    data = client.fetch_financial_statement_as_reported(symbol)
    return pd.DataFrame(data['data'][0]['report']['ic'])[['label','value']]

@st.cache
def load_img(symbol):
    data = client.fetch_company(symbol)
    return data.get('logo')


data = load_company_info("FB")
# Notify the reader that the data was successfully loaded.
st.markdown('Streamlit is **_really_ cool**.')



st.subheader('Company Info')
st.write(data)

st.image(load_img("FB"))


st.empty()

data2 = load_balance_sheet("FB")
data3 = load_income_statement("FB")


st.subheader("Balance Sheet")
st.table(data2)

st.subheader("Income Statement")
st.table(data3)
