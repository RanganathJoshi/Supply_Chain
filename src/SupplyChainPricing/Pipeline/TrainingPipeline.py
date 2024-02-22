import os
import pandas as pd
from src.SupplyChainPricing.Components.DataIngestion import DataIngestionWorkflow
from src.SupplyChainPricing.Components.FeatureEngineering import DataTransformation
from src.SupplyChainPricing.Components.ModelTrainer import Model_Trainer
import sys
from src.SupplyChainPricing.logger import logging
from src.SupplyChainPricing.Exception import customexception

class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion=DataIngestionWorkflow()
            train_path,test_path=data_ingestion.initiate_data_ingestion()
            return train_path,test_path
        except Exception as e:
            raise customexception(e,sys)


    def start_data_transformation(self,train_path,test_path):
        try:
            data_transformation=DataTransformation()
            train_path,test_path=data_transformation.initiate_data_transform(train_path,test_path)
            return train_path,test_path
        except Exception as e:
            raise customexception(e,sys)
        

    def start_model_training(self,train_path,test_path):
        try:
            model_trainer=Model_Trainer()
            model_trainer.initiate_model_training(train_path,test_path)
            

        except Exception as e:
            raise customexception(e,sys)
        
    
    def start_training(self):

        try:
            train_path,test_path=self.start_data_ingestion()
            train_path,test_path=self.start_data_transformation(train_path,test_path)
            self.start_model_training(train_path,test_path)

        except Exception as e:
            raise customexception(e,sys)


     