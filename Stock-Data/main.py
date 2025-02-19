# Importing the req libs
import streamlit as st
import pandas as pd
import plotly.express as ex
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests, logging
import numpy as np
import yfinance as yf
from bs4 import BeautifulSoup


# Creating a logging function
def log_file(message:str):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="Logging.txt",filemode="a",encoding="utf-8",datefmt="%Y-%m-%d %H:%M:%S"
                        ,format="%(asctime)s: %(message)s",level=logging.INFO)
    logger.info(message)
    

st.title('Stock-Data-Analysis')
st.sidebar.header('User Input Features')

# log_file("Initial extraction of data commenced.")
@st.cache_data
def extract_data(url,headers):
    html_data = requests.get(url).text
    parsed_data = BeautifulSoup(html_data,"html.parser")
    table_data = parsed_data.find_all("tbody")[1]
    tesla_revenue = pd.DataFrame(columns=headers)
    for rows in table_data.find_all("tr"):
        cols = rows.find_all("td")
        if len(cols)!=0:
            data_dict = {headers[0]:cols[0].get_text(strip=True),
                         headers[1]:cols[1].get_text(strip=True)}
        df1 = pd.DataFrame(data_dict,index=[0])
        tesla_revenue = pd.concat([tesla_revenue,df1],ignore_index=True)
    return tesla_revenue

def transform_data(df):
    pass

url_link = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
tesla_revenue = extract_data(url_link,["Date","Revenue"])

# log_file("Web data extracted. Processing has begun.")
st.header('Displaying date and revenues of Tesla stock.')
st.dataframe(tesla_revenue)