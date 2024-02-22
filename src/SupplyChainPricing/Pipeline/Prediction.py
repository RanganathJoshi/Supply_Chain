from src.SupplyChainPricing.logger import logging
from src.SupplyChainPricing.Exception import customexception
import os
import pandas as pd
import sys
from pathlib import Path
from src.SupplyChainPricing.utils import load_obj,read_yaml,change_columns_names
from src.SupplyChainPricing.constants import *
import mlflow.pyfunc

model_name="Best_obtained_mode"
model_version=2

class PredictPipeline:

    def __init__(self):
        self.config_path=CONFIG_FILE_PATH
        self.contents=read_yaml(self.config_path)
        self.model_contents=self.contents.get('model_training')
        self.model_path:Path=self.model_contents.get('model_path')
        self.processor_path:Path=self.model_contents.get('processor')
        
 
    def predict(self,data):
        try:
            processor=load_obj(self.processor_path)
            model=load_obj(self.model_path)

            scaled_data=processor.transform(data)
            prediction=model.predict(scaled_data[:,:-1])

            return prediction
        
        except Exception as e:
            raise customexception(e,sys)
        


class CustomData:
    try:
        def __init__(self):
            self.config_path=CONFIG_FILE_PATH
            self.contents=read_yaml(self.config_path)
            self.model_contents=self.contents.get('data_ingestion')
            self.model_path:Path=self.model_contents.get('train_data')
        def get_data_as_dataframe(self,*features):
            data=pd.read_csv(self.model_path)
            data.drop(columns=['Unnamed: 0','Unnamed: 0.1'],inplace=True)
            column_names=data.columns
            input_data=dict(zip(column_names,features))
            df=pd.DataFrame(features,columns=column_names)
            print(df.columns)
            return df

    except Exception as e:
        raise customexception(e,sys)

