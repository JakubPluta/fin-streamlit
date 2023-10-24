import pandas as pd
import streamlit as st

from fin_streamlit.charts import get_candle_chart, get_barchart


def _write_view(symbol: str, header: str, data: pd.DataFrame) -> None:
    """
    Writes a subheader and a DataFrame to the Streamlit app.

    Args:
        symbol: A symbol to be used in the subheader.
        header: A header to be displayed above the DataFrame.
        data: A Pandas DataFrame to be displayed.

    Returns:
        None.
    """
    st.subheader(f"*{symbol} {header}*")
    st.write(data)


def home_page_view(symbol: str) -> None:
    """Displays the home page of the Streamlit app.

    Args:
        symbol: The symbol of the company to display.
    """
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


def search_results_view(keyword: str, data: pd.DataFrame) -> None:
    """
    Searches for a keyword in a Pandas DataFrame and displays the results.

    Args:
        keyword: The keyword to search for.
        data: A Pandas DataFrame containing the data to be searched.

    Returns:
        None.
    """

    st.write(f"Here are results for searched keyword {keyword}")
    st.write(data)


def company_info_view(symbol: str, data: dict) -> None:
    """Displays the company information page of the Streamlit app.

    Args:
        symbol: The symbol of the company to display.
        data: A dictionary containing the company information data.
    """
    st.subheader(f'*{data.get("Name")} Overview*')
    st.markdown(
        f"""
        This view display basic information about {data.get("Name", symbol)}.
        You can see there statistics like:
        
    """
    )
    st.write(data.get("Description"))
    filtered_data = {k: v for k, v in data.items() if k not in ["Name", "Description"]}
    for k, v in filtered_data.items():
        st.write(f"* {k}: {v}")


def balance_sheet_view(symbol: str, data: pd.DataFrame) -> None:
    """Displays the balance sheet page of the Streamlit app.

    Args:
        symbol: The symbol of the company to display.
        data: A pd.DataFrame containing the balance sheet data.
    """
    _write_view(symbol, "Balance Sheet", data)


def income_statement_view(symbol: str, data: pd.DataFrame) -> None:
    """Displays the Income Statement page of the Streamlit app.

    Args:
        symbol: The symbol of the company to display.
        data: A pd.DataFrame containing the Income Statement data.
    """
    _write_view(symbol, "Income Statement Sheet", data)


def cash_flow_view(symbol: str, data: pd.DataFrame) -> None:
    """Displays the cash flow page of the Streamlit app.

    Args:
        symbol: The symbol of the company to display.
        data: A pd.DataFrame containing the cash flow.
    """
    _write_view(symbol, "Cash Flow", data)


def quotes_view(symbol: str, data: pd.DataFrame) -> None:
    """Displays the quotes page of the Streamlit app.

    Args:
        symbol: The symbol of the company to display.
        data: A pd.DataFrame containing the quotes data.
    """
    _write_view(symbol, "Daily Quotes", data)


def kpi_view(symbol: str, data: pd.DataFrame) -> None:
    """Displays the kpis page of the Streamlit app.

    Args:
        symbol: The symbol of the company to display.
        data: A pd.DataFrame containing kpis data.
    """
    _write_view(symbol, "KPI's", data)


def quotes_chart_view(data: pd.DataFrame) -> None:
    """Displays a candle chart of the quotes data.

    Args:
        data: A Pandas DataFrame containing the quotes data.
    """

    fig = get_candle_chart(data)
    st.plotly_chart(figure_or_data=fig)


def financial_assets_chart_view(data: pd.DataFrame) -> None:
    """Displays a bar chart of the financial assets data.

    Args:
        data: A Pandas DataFrame containing the financial assets data.
    """

    categories = data.index.to_list()
    chosen_category = st.selectbox(
        "What category, do you want to analyze ? ", categories
    )
    fig = get_barchart(data, chosen_category)
    st.plotly_chart(figure_or_data=fig)
