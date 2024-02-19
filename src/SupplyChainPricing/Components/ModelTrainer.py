from src.SupplyChainPricing.logger import logging
from src.SupplyChainPricing.Exception import customexception
import os
import sys
from pathlib import Path
from src.SupplyChainPricing.utils import read_yaml,load_obj,evaluate_model,save_obj
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from src.SupplyChainPricing.constants import *

class ModelTrainingConfig:
    config_file:Path=CONFIG_FILE_PATH
    contents=read_yaml(config_file)
    model_training=contents.get('model_training')
    processor_path=model_training.get('processor')
    model_path=model_training.get('model_path')


class Model_Trainer:
    def __init__(self):
        self.config=ModelTrainingConfig()

    def initiate_model_training(self,train_data_path,test_data_path):
        try:
            logging.info("Model training initiated")
            train_data=pd.read_csv(train_data_path)
            test_data=pd.read_csv(test_data_path)
            drop_cols='Unnamed: 0'
            train_data.drop(columns=drop_cols,inplace=True)
            test_data.drop(columns=drop_cols,inplace=True)
            x_train,x_test,y_train,y_test=(train_data.iloc[:,:-1],
                                           test_data.iloc[:,:-1],
                                           train_data.iloc[:,-1],
                                           test_data.iloc[:,-1])
            

            models={
                'Linear Regression':LinearRegression(),
                'Decision Tree Regression':DecisionTreeRegressor(),
                'Random Forest Regression':RandomForestRegressor(),
                'Adaboost regressor': AdaBoostRegressor(),
                'gradientboost regressor': GradientBoostingRegressor()
            }
            
            result=pd.DataFrame(columns=['Model','test_score','train_score','cross_val_score'])
            best_model_name,best_score,trained_models=evaluate_model(models,x_train,x_test,y_train,y_test,result)
            print(best_model_name)
            print("-------------------------------------------------------------------------------")
            print(trained_models)
            print("-------------------------------------------------------------------------------")
            print(result)
            print("-------------------------------------------------------------------------------")
            print("Best Model: ",best_model_name, "with score of ",best_score)

            logging.info("Best Model found")
            save_obj(trained_models[best_model_name],self.config.model_path)



        except Exception as e:
            logging.info("Error while occuring model training")
            raise customexception(e,sys)

            