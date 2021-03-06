# fin-streamlit

Using streamlit as a tool for Financial Statement Analysis


![Alt Text](https://github.com/JakubPluta/fin-streamlit/blob/master/stock.gif)


### Running on heroku

```
https://fin-streamlit.herokuapp.com/
```



### Prerequisites

```
visit https://www.alphavantage.co/ and get your API key
```

### Installing


```
git clone https://github.com/JakubPluta/fin-streamlit.git
pip install -r requirements
```

## Running script with command line

```
you need to setup your api_key first in src/main/settings/default
streamlit run src/main/python/application.py
```

## Running the tests

```
pytest src/main/python/tests
```

## Built With

* [pandas](https://pandas.pydata.org/docs/) - For data manipulation
* [requests](https://requests.readthedocs.io/en/master/) - To communicate with API
* [streamlit](https://docs.streamlit.io/en/stable/) - web app


## Authors

* **Jakub Pluta** - [github](https://github.com/JakubPluta)


