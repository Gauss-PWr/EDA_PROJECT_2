import os
from kaggle.api.kaggle_api_extended import KaggleApi
from typing import Literal
from dotenv import load_dotenv


def download_dataset() -> Literal[True]:
    """function for downloading a dataset from kaggle

    Returns:
        Literal[True]: 
    """
    
    load_dotenv()
    dataset_name = os.getenv("dataset_name")

    #create 'data' folder if it doesnt exist
    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_folder_path = os.path.join(root_dir, 'data')
    os.makedirs(data_folder_path, exist_ok=True)
    
    #activating kaggle api
    api = KaggleApi()
    api.authenticate()
    
    #self-explainatory
    api.dataset_download_files(dataset_name, path=data_folder_path, unzip=True)
    
    return True

if __name__ == '__main__':
    download_dataset()