# fin-streamlit

Using streamlit as a tool for Financial Statement Analysis


![stock.gif](stock.gif)

### Prerequisites

```
visit https://www.alphavantage.co/ and get your API key
```

### Installing

### Clone repository
```bash
# clone repository
git clone https://github.com/JakubPluta/fin-streamlit.git
```
```bash
# navigate to cloned project and create virtual environment
python -m venv env
```
```bash
# activate virtual environment
source env/Scripts/activate # or source env/bin/activate
```

```python
# install poetry
pip install poetry
```

```python
# install packages
poetry install
```

```
* Visit https://www.alphavantage.co/ and get your API key
* And then set ALPHA_VANTAGE_API_KEY in .env file in root directory
```

```python
# run application
streamlit app.py

# or use makefile
make run
```



## Built With

* [pandas](https://pandas.pydata.org/docs/) - For data manipulation
* [requests](https://requests.readthedocs.io/en/master/) - To communicate with API
* [streamlit](https://docs.streamlit.io/en/stable/) - web app


## Authors

* **Jakub Pluta** - [github](https://github.com/JakubPluta)


