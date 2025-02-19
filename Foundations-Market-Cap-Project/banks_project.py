# Importing the required libs

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests,datetime,sqlite3

# Creating the log function
def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    curr_now = datetime.datetime.now()
    time_format = '%H:%M:%S-%h-%d-%Y'
    time_stamp = curr_now.strftime(time_format)
    with open(log_file,"a") as f:
        f.write(time_stamp+" : "+message+"\n")

# Crating the extract function
def extract(url,table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    
    df = pd.DataFrame(columns=table_attribs)
    page = requests.get(url).text
    soup = BeautifulSoup(page,"html.parser")
    webpage_table = soup.find_all("table",class_="wikitable")[0]
    table = webpage_table.find_all("tr")
    for rows in table:
        cols = rows.find_all("td")
        if len(cols)!=0:
            data_dict = {table_attribs[0]:cols[1].get_text(strip=True),
                         table_attribs[1]:cols[2].get_text(strip=True)}
            df1 = pd.DataFrame(data_dict,index=[0])
            df = pd.concat([df,df1],ignore_index=True)
    return df


# Creating the transformation function.
def transform(df,csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    
    exchange_rate_df = pd.read_csv(csv_path)
    df["MC_USD_Billion"] = df["MC_USD_Billion"].astype(float)
    exchange_rate = exchange_rate_df.set_index('Currency').to_dict()['Rate']
    df['MC_GBP_Billion'] = [np.round(x*exchange_rate["GBP"],2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x*exchange_rate["EUR"],2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x*exchange_rate["INR"],2) for x in df['MC_USD_Billion']]
    return df

# Crated a function to output to csv
def load_to_csv(df,output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    
    df.to_csv(output_path,index=False)
    
# Loading to a sqlite db
def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    
    df.to_sql(table_name,sql_connection,if_exists="replace",index=False)

def run_query(query_statement,sql_connection):
    ''' This function runs the query on the database table and
        prints the output on the terminal. Function returns nothing. '''
        
    print(query_statement)
    query_output = pd.read_sql(query_statement,sql_connection)
    print(query_output)
    

# Calling the functions

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs = ["Name","MC_USD_Billion"]
csv_path = "./Largest_banks_data.csv"
db_name = "Banks.db"
table_name = "Largest_banks"
log_file = "code_log.txt"

log_progress("Preliminaries complete. Initiating ETL process")

extraction = extract(url,table_attribs)
log_progress("Data extraction complete. Initiating Transformation process")

transformed = transform(extraction,"exchange_rate.csv")
log_progress("Data transformation complete. Initiating Loading process")

load_to_csv(transformed,csv_path)
log_progress("Data saved to CSV file")

conn = sqlite3.connect(db_name)
log_progress('SQL Connection initiated.')

to_db = load_to_db(transformed,conn,table_name)
log_progress('Data loaded to Database as a table, Executing queries')

run_query("SELECT * FROM Largest_banks",conn)
run_query("SELECT AVG(MC_GBP_Billion) FROM Largest_banks",conn)
run_query("SELECT Name from Largest_banks LIMIT 5",conn)

log_progress('Process Complete.')

conn.close()
log_progress("Server Connection closed")