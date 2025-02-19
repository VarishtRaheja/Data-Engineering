# Importing required libs
from bs4 import BeautifulSoup
import pandas as pd
import requests,sqlite3,datetime

# Creating global variables
log_file = "./etl_project_log.txt"
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ["Country", "GDP_USD_millions"]
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './Countries_by_GDP.csv'

# Extraction Process
def extract(url, table_attribs):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
    
    extract = requests.get(url).text
    soup_parsed = BeautifulSoup(extract,"html.parser")
    df = pd.DataFrame(columns=table_attribs)
    t_body_attrs = soup_parsed.find_all("tbody")[2]
    for rows in t_body_attrs.find_all("tr"):
        col = rows.find_all('td')
        if len(col)!=0:
            if col[0].find("a") is not None and "—" not in col[2]:
                data_dict = {table_attribs[0]:col[0].a.get_text(strip=True),
                             table_attribs[1]:col[2].get_text(strip=True)}
                df1 = pd.DataFrame(data_dict,index=[0])
                df = pd.concat([df,df1],ignore_index=True)
    return df

# Transformation Process
def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
    
    df["GDP_USD_millions"] = df["GDP_USD_millions"].apply(lambda x: round(float(x.replace(",",""))*0.001,2))
    df = df.rename(columns={"GDP_USD_millions":"GDP_USD_billions"})
    return df

# Loading to a csv file
def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path,index=False)
    
    
# Loading to a sqlite db
def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''

    df.to_sql(table_name,sql_connection,if_exists="replace",index=False)
    


# Running the query for sql 
def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    # display only the entries with more than a 100 billion USD economy
    print(query_statement)
    query_output = pd.read_sql(query_statement,sql_connection)
    print(query_output)
    sql_connection.close()
    
# Logging the process
def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. Function returns nothing'''
    now = datetime.datetime.now()
    time_stamp_format = '%H:%M:%S-%h-%d-%Y'
    timestamp = now.strftime(time_stamp_format)
    with open(log_file,"a") as f:
        f.write(message+": "+timestamp+"\n")
    

log_progress("Extraction Process Started")
records = extract(url,table_attribs)

log_progress("Transformation Process Started")
transfromed_df = transform(records)

log_progress("Written to CSV file")
to_csv = load_to_csv(transfromed_df,csv_path)

conn = sqlite3.connect(db_name)

log_progress("Written to database")
to_db = load_to_db(transfromed_df,conn,table_name)

log_progress("Queries statements as required from database")
filter_statement = "SELECT * from {} WHERE GDP_USD_billions > 100".format(table_name)

run_query(filter_statement,conn)
log_progress("Logging process completed")