import pandas as pd
import numpy as np
from src.SupplyChainPricing.logger import logging
from src.SupplyChainPricing.Exception import customexception
from src.SupplyChainPricing.constants import *
from sklearn.model_selection import train_test_split
import os
import yaml
import sys
from pathlib import Path
from src.SupplyChainPricing.utils import download_data,read_yaml,unzip_data

class DataIngestionConfig:
    config_path:Path=CONFIG_FILE_PATH
    contents=read_yaml(config_path)
    data_ingestion=contents['data_ingestion']

class DataIngestionWorkflow:
    def __init__(self):
        self.config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info("Data fetching")
            train_data_path:Path=self.config.data_ingestion.get('train_data')
            raw_data_path:Path=self.config.data_ingestion.get('raw_data')
            test_data_path:Path=self.config.data_ingestion.get('test_data')
            data=pd.read_csv(raw_data_path)
            logging.info("Splitting the dataset into train and test")
            train_data,test_data=train_test_split(data,test_size=0.2)
            logging.info("Train Test Split Completed")
            train_data.to_csv(train_data_path)
            test_data.to_csv(test_data_path)
            logging.info("Successfully Saved train and test dataset")
            return train_data_path,test_data_path
        except Exception as e:
            raise customexception(e,sys)
