import pandas as pd
import numpy as np
from src.supplychainpricing.logger import logging
from src.supplychainpricing.Exception import customexception
from src.supplychainpricing.constants import *
import os
import yaml
import sys
from pathlib import Path
from src.supply_chain_pricing.utils import download_data,read_yaml

class DataIngestionConfig:
    config_path:Path=CONFIG_FILE_PATH
    contents=read_yaml(config_path)
    data_ingestion=contents['data_ingestion']

class DataIngestionWorkflow:
    def __init__(self):
        self.config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            source_file:Path=self.config.data_ingestion.get('source')
            raw_data_path:Path=self.config.data_ingestion.get('raw_data')
            download_data(source_file,raw_data_path)
        except Exception as e:
            raise customexception(e,sys)
