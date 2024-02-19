import sys
import os
import pandas as pd
from pathlib import Path
from src.SupplyChainPricing.logger import logging
from src.SupplyChainPricing.Exception import customexception
from src.SupplyChainPricing.utils import read_yaml,save_obj,change_columns_names
from src.SupplyChainPricing.constants import *
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

class DataTransomationConfig:
    config_file:Path=CONFIG_FILE_PATH
    contents=read_yaml(config_file)
    data_transformation=contents.get('data_transformation')
    os.makedirs(data_transformation.get('root_path'),exist_ok=True)

class DataTransformation:
    def __init__(self):
        self.config_file=DataTransomationConfig()
    
    def prepare_data_transformation(self,num_cols,cat_cols):
        try:
            num_pipeline=Pipeline(
                steps=[
                ['MinMaxscalar',MinMaxScaler()]

            ])

            cat_pipeline=Pipeline(
                steps=[
                ['Onehotcoder',OneHotEncoder(drop='first')]
            ])

            processor=ColumnTransformer([
                ('numericalpipeline',num_pipeline,num_cols),
                ('categoricalpipeline',cat_pipeline,cat_cols)
            ],remainder='passthrough')



            return processor
        
        except Exception as e:
            raise(e,sys)
        
    def initiate_data_transform(self,train_path,test_path):
        try:
            logging.info("Data Transformation started")
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            drop_cols=['Unnamed: 0.1', 'Unnamed: 0']
            train_df.drop(columns=drop_cols,inplace=True)
            test_df.drop(columns=drop_cols,inplace=True)
            num_cols=[i for i in train_df.columns if train_df[i].dtype!=object]
            num_cols.remove('line_item_value')
            cat_cols=[i for i in train_df.columns if train_df[i].dtype==object]

            processor_obj=self.prepare_data_transformation(num_cols,cat_cols)
            train_data=pd.DataFrame(processor_obj.fit_transform(train_df))
            test_data=pd.DataFrame(processor_obj.transform(test_df))


            train_path=self.config_file.data_transformation.get('train_data')
            test_path=self.config_file.data_transformation.get('test_data')

            train_data.columns=processor_obj.get_feature_names_out()
            test_data.columns=train_data.columns
    
            train_data.columns=change_columns_names(train_data)
            test_data.columns=change_columns_names(test_data)
        


            train_data.to_csv(train_path)
            test_data.to_csv(test_path)



            logging.info("Data Transformation completed")
            processor_obj_path=Path(self.config_file.data_transformation.get('processor'))
            save_obj(processor_obj,processor_obj_path)

            logging.info("Processor Object Successfully Saved")


            return train_path,test_path

        except Exception as e:
            logging.info("Error occured while applying transformation")
            raise customexception(e,sys)
        









