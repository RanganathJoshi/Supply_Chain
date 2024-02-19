from src.Supply_Chain_pricing.Exception import customexception
from src.Supply_Chain_pricing.logger import logging
import os
from pathlib import Path
import requests
import zipfile
import io

def download_data(url:str,dest_path:Path):
    logging.info("Downloading started")
    dir_name=os.path.dirname(dest_path)
    os.makedirs(dir_name,exist_ok=True)
    logging.info("Directories Created")
    response=requests.get(url)
    if response.status_code==200:
        zip_file=io.BytesIO(response.contents)
        
        with zipfile.ZipFile(zip_file,'r') as zip_ref:
            zip_ref.extractall(dest_path)

        logging.info("Data downloaded")

def read_yaml(yaml_file_path:Path):
    with open(yaml_file_path, 'r') as file:
    # Load the YAML content
        contents = yaml.safe_load(file)
    return contents