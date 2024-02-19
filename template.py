from pathlib import Path
import os

package_name="Supply_Chain_pricing"

list_file=[
    "github/workflows/.gitkeep",
    f"src/{package_name}/Components/__init__.py",
    f"src/{package_name}/Components/DataIngestion.py",
    f"src/{package_name}/Components/FeatureEngineering.py",
    f"src/{package_name}/Components/ModelTrainer.py",
    f"src/{package_name}/Pipeline/__init__.py",
    f"src/{package_name}/Pipeline/Training.py",
    f"src/{package_name}/Pipeline/Prediction.py",
    f"src/{package_name}/constants/__init__.py",
    "requirements.txt",
    "setup.py",
    "notebooks/research.ipynb",
    "notebooks/data.gitkeep"
]

for file_name in list_file:
    file=Path(file_name)
    folder,file=os.path.split(file)

    if folder!='':
        os.makedirs(folder,exist_ok=True)
    if (not os.path.exists(file_name)) or (os.path.getsize(file_name)==0):
        with open(file_name,'w') as f:
            pass
    else:
        print("File already exists") 
