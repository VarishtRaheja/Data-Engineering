# Importing the req libs
import streamlit as st
import pandas as pd
import plotly.express as ex
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests, logging 
import yfinance as yf
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Creating a logging function
def log_file(message:str):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="Logging.txt",filemode="a",encoding="utf-8",datefmt="%Y-%m-%d %H:%M:%S"
                        ,format="%(asctime)s: %(message)s",level=logging.INFO)
    logger.info(message)
    

@st.cache_data
def extract_data(url,headers):
    """ Extracting the data from url """
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

@st.cache_data
def transform_data(df:pd.DataFrame):
    """ Removing unwanted data """
    df["Revenue"] = df['Revenue'].str.replace('$',"")
    df["Revenue"] = df['Revenue'].str.replace(',',"")
    df = df.dropna()
    df = df[df['Revenue'] != ""]
    return df


# Creating the graph for history stock data.
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    # Save the plot as a JPEG file
    # fig.write_image(f"{stock}.jpeg")
    return st.plotly_chart(fig)


ticker = yf.Ticker("TSLA")
tesla_data = ticker.history(period="max")
tesla_data.reset_index(inplace=True)

ticker_2 = yf.Ticker("GME")
gme_data = ticker_2.history(period="max")
gme_data.reset_index(inplace=True)

st.title('Stock Data Analysis')
st.markdown("""
Extract financial data like historical share price and quarterly revenue reportings from various sources using Python libraries 
and webscraping on popular stocks. After collecting this data you will visualize it in a dashboard to identify patterns or trends.
* **Python libraries:** pandas, streamlit, plotly, bs4.
""")

st.divider()


tsla, gme = st.columns(2)
if tsla.button("Tesla Revenue", use_container_width=True):
    log_file("Initial extraction of data commenced.")
    url_link = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
    tesla_revenue = transform_data(extract_data(url_link,["Date","Revenue"]))
    log_file("Web data extracted. Processing has begun.")
    st.header("Tesla Revenue & Stock")
    make_graph(tesla_data,tesla_revenue,"Tesla")
    log_file("Plot has been generated.")
    # with open("Tesla.jpeg","rb") as f:
    #     btn = st.download_button(label="Download Plot",data=f,file_name="Tesla.jpeg",mime="image/jpeg")
    # if btn:
    #     log_file("Current plot has been downloaded.")
    
        
if gme.button("Game Stop Revenue",use_container_width=True):
    log_file("Initial extraction of data commenced.")
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
    gme_revenue = transform_data(extract_data(url,["Date","Revenue"]))
    log_file("Web data extracted. Processing has begun.")
    st.header("GameStop Revenue & Stock")
    make_graph(gme_data,gme_revenue,"Game Stop")
    log_file("Plot has been generated.")
    # with open("GameStop.jpeg","rb") as f:
    #     btn = st.download_button(label="Download Plot",data=f,file_name="GameStop.jpeg",mime="image/jpeg")
    # if btn:
    #     log_file("Current plot has been downloaded.")

