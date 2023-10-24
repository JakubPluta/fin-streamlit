import pandas as pd


def _prepare_statement_df(data: dict) -> pd.DataFrame:
    """Prepares a Pandas DataFrame from a JSON dictionary containing financial statement data.

    Args:
        data: A JSON dictionary containing financial statement data.

    Returns:
        A Pandas DataFrame containing the financial statement data.
    """
    df = pd.json_normalize(data).T
    df.columns = df.iloc[0]
    df = df[1:]
    return df
