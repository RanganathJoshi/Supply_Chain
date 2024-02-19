import os
import sys
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from pathlib import Path
from src.SupplyChainPricing.utils import load_obj,read_yaml
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from src.SupplyChainPricing.logger import logging
from src.SupplyChainPricing.Exception import customexception
from src.SupplyChainPricing.constants import *

class ModelEvaluation:
    def __init__(self):
        self.config:Path=CONFIG_FILE_PATH
        self.contents=read_yaml(self.config)
        self.contents=self.contents.get('model_training')
        self.model_save=self.contents.get('model_path')
        self.processor_save=self.contents.get('processor')
        

    def save_model(self):
        try:
            print(self.model_save)
            model=load_obj(self.model_save)
            preprocessor=load_obj(self.processor_save)

            tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme
            print(tracking_url_type_store)

            with mlflow.start_run():
                mlflow.log_artifacts(Path('artifacts'))
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="Best_obtained_mode")
                else:
                    mlflow.sklearn.log_model(model,"model")




        except Exception as e:
            raise customexception(e,sys)
        

save_model=ModelEvaluation()
save_model.save_model()