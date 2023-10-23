import streamlit as st

from fin_streamlit.charts import financial_statement_chart, quotes_chart


def home_page_view(symbol: str):
    st.markdown(
        f"""
        Application uses [AlphaVantage API](https://www.alphavantage.co/documentation/) to fetch financial data like 
        financial statements, company basic information, KPI's and Quotes.

        On the Left side you have a panel where you can provide stock's
        ticker and navigate to page that you are interested int. 
        You can analyze financial data like:
            * Income Statement 
            * Balance Sheet  
            * Cash Flow  
            * Quotes  
            * Company Overview  
            
        If you want to search for a company ticker you can use search box below. 
        If you find company that you are interested at, just provide the ticker
        on the panel at left side of screen and press enter. 
        Now you can analyze all of the elements of report. 
        
        Chosen symbol: {symbol}
        
        """
    )


def company_info_view(symbol, data):
    st.subheader(f'*{data.get("Name")} Overview*')
    st.markdown(
        f"""
        This view display basic information about {data.get("Name", symbol)}.
        You can see there statistics like:
        
    """
    )
    st.write(data.get("Description"))
    filtered_data = {k:v for k,v in data.items() if k not in ["Name","Description"]}
    for k, v in filtered_data.items():
        st.write(f"* {k}: {v}")


def balance_sheet_view(symbol, data):
    st.subheader(f"*{symbol} Balance Statement*")
    st.write(data)


def balance_sheet_chart_view(chart, data, categories):
    financial_statement_chart(chart, data, categories)


def income_statement_view(symbol, data):
    st.subheader(f"*{symbol} Income Sheet*")
    st.write(data)


def income_statement_chart_view(chart, data, categories):
    financial_statement_chart(chart, data, categories)


def cash_flow_view(symbol, data):
    st.subheader(f"*{symbol} Cash Flow*")
    st.write(data)


def cash_flow_chart_view(chart, data, categories):
    financial_statement_chart(chart, data, categories)


def quotes_view(symbol, data):
    st.subheader(f"*{symbol} Daily Quotes*")
    st.write(data)


def quotes_chart_view(data):
    quotes_chart(data)


def kpi_view(symbol, data):
    st.subheader(f"*{symbol} KPIs*")
    st.table(data)
