from __future__ import annotations
import json
import subprocess
from textwrap import dedent
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.SupplyChainPricing.Pipeline.TrainingPipeline import TrainingPipeline
training_pipeline=TrainingPipeline()



with DAG(
    "Supply_Chain_pipeline",
    default_args={"retries": 2},
    description="it is my training pipeline",
    schedule="@weekly",# here you can test based on hour or mints but make sure here you container is up and running
    start_date=datetime(2024, 2, 21),
    catchup=False,
    tags=["machine_learning ","classification","gemstone"],
) as dag:
    
    dag.doc_md = __doc__
    
    def data_ingestion(**kwargs):
        ti = kwargs["ti"]
        train_data_path,test_data_path=training_pipeline.start_data_ingestion()
        ti.xcom_push("data_ingestion_artifact", {"train_data_path":train_data_path,"test_data_path":test_data_path})

    def data_transformations(**kwargs):
        ti = kwargs["ti"]
        data_ingestion_artifact=ti.xcom_pull(task_ids="data_ingestion",key="data_ingestion_artifact") 
        train_path,test_path=training_pipeline.start_data_transformation(data_ingestion_artifact["train_data_path"],data_ingestion_artifact["test_data_path"])
        ti.xcom_push("data_transformations_artifcat", {"train_path":train_path,"test_path":test_path})

    def model_trainer(**kwargs):
        import numpy as np
        ti = kwargs["ti"]
        data_transformation_artifact = ti.xcom_pull(task_ids="data_transformation", key="data_transformations_artifcat")
        train_path=data_transformation_artifact["train_path"]
        test_path=data_transformation_artifact["test_path"]
        training_pipeline.start_model_training(train_path,test_path)


    def push_images_to_github(**kwargs):


# Command to execute
        cmd_command_1 = "git add ." 
        cmd_command_2= "git commit"
        cmd_command_3= "git " # Example command, you can replace it with any command you want to execute

# Execute the command
        process = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Capture the output and errors
        output, error = process.communicate()

# Print the output and errors
        if output:
            print("Output:")
        print(output.decode("utf-8"))
        if error:
            print("Errors:")
            print(error.decode("utf-8"))

        
    
         
        
        
    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion,
    )
    data_ingestion_task.doc_md = dedent(
        """\
    #### Ingestion task
    this task creates a train and test file.
    """
    )

    data_transform_task = PythonOperator(
        task_id="data_transformation",
        python_callable=data_transformations,
    )
    data_transform_task.doc_md = dedent(
        """\
    #### Transformation task
    this task performs the transformation
    """
    )

    model_trainer_task = PythonOperator(
        task_id="model_trainer",
        python_callable=model_trainer,
    )
    model_trainer_task.doc_md = dedent(
        """\
    #### model trainer task
    this task perform training
    """
    )
    


data_ingestion_task >> data_transform_task >> model_trainer_task