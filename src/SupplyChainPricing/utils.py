from src.SupplyChainPricing.Exception import customexception
from src.SupplyChainPricing.logger import logging
import os
from pathlib import Path
import requests
import zipfile
import io
import pickle
import yaml
import urllib.request as request 
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score

def read_yaml(path_to_yaml:Path):
    with open(path_to_yaml,'r') as file:
        contents=yaml.safe_load(file)

        return contents
    
def download_data(url_path:str,destination:Path):
    if not (os.path.exists(destination)):
        file,headers=request.urlretrieve(url=url_path,filename=destination)
    return destination

def unzip_data(zip_file_path,destination):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination)

    return destination

def read_yaml(yaml_file_path:Path):
    with open(yaml_file_path, 'r') as file:
    # Load the YAML content
        contents = yaml.safe_load(file)
    return contents

def save_obj(obj,file_path):
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    with open(file_path,'wb') as f:
        pickle.dump(obj,f)
 

def change_columns_names(df):
    new_column=[]
    for i in df.columns:
        split=i.split('__')
        new_column.append(split[1])
    return new_column
        

def load_obj(obj_path:Path):
    with open(obj_path,'rb') as f:
        return pickle.load(f)


def evaluate_model(models,x_train,x_test,y_train,y_test,result):
    trained_models={}
    for key,model in models.items():
        gs=cross_val_score(model,x_train,y_train,cv=5)
        max_cross_val_score=max(gs)
        model.fit(x_train,y_train)
        y_pred_train=model.predict(x_train)
        y_pred=model.predict(x_test)
        score_test=e=r2_score(y_test,y_pred)
        score_train=r2_score(y_train,y_pred_train)
        result.loc[len(result)]=[key,score_test,score_train,round(max_cross_val_score,4)]
        trained_models[key]=model
    
    max_score=result['cross_val_score'].max()
    max_id=result[result['cross_val_score']==max_score].index
    best_model_name=result.loc[max_id,'Model'].values[0]
    best_score=result.loc[max_id,'cross_val_score'].values[0]

    return best_model_name,best_score,trained_models



