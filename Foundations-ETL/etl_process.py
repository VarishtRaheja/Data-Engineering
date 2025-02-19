import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime
from zipfile import ZipFile 
import os


# Unzipping files in this directory

with ZipFile(os.getcwd()+"\data_source.zip","r") as zip_object:
    zip_object.extractall(path=os.getcwd())

log_save_file = "log.txt"
target_save_file = "transformed_file.csv"

def extract_from_csv(file_to_process): 
    dataframe = pd.read_csv(file_to_process) 
    return dataframe


def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process,lines=True)
    return dataframe


def extract_from_xml(file_to_process):

    dataframe = pd.DataFrame(columns=['car_model','year_of_manufacture','price', 'fuel'])

    tree = ET.parse(file_to_process) 

    root = tree.getroot() 

    for person in root: 

        car_model = person.find("car_model").text 

        year_of_manufacture = int(person.find("year_of_manufacture").text)

        price = float(person.find("price").text) 

        fuel = person.find("fuel").text 

        dataframe = pd.concat([dataframe,pd.DataFrame({"car_model":car_model, "year_of_manufacture":year_of_manufacture,\
            "price":price, "fuel":fuel},index=[0,1,2,3])], ignore_index=True) 

    return dataframe
    
def extract():
    extraced_data = pd.DataFrame(columns=["car_model","year_of_manufacture","price","fuel"])
    for csv_files in glob.glob("*.csv"):
        dataframe = pd.concat([extraced_data,pd.DataFrame(extract_from_csv(csv_files))],ignore_index=True)
        
    for json_files in glob.glob("*.json"):
        dataframe = pd.concat([extraced_data,pd.DataFrame(extract_from_json(json_files))],ignore_index=True)
        
    for xml_files in glob.glob("*.xml"):
        dataframe = pd.concat([extraced_data,pd.DataFrame(extract_from_xml(xml_files))],ignore_index=True)
    
    return dataframe

def transform(data):
    data["price"] = round(data["price"],2)
    return data
    
def load_data(target_save_file,transformed_data):
    transformed_data.to_csv(target_save_file)
    
    
def log(message):
    curr_time = datetime.now()
    time_stamp_format = '%H:%M:%S-%h-%d-%Y'
    timestamp = curr_time.strftime(time_stamp_format)
    with open(log_save_file,"a") as f:
        f.write(message + ": " + timestamp + "\n")
        


log("Logging Process started------")
extracted_data = extract()
log("Extraction Process Completed------")
transform_data = transform(extracted_data)
log("transformation Process Completed------")
load_data(target_save_file,transform_data)
log("Load Process Completed------")