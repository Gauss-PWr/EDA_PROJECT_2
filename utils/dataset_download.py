import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset() -> bool:     #function will return True bool if operation is ended succesfuly
    """function for downloading a dataset from kaggle"""
    
    link = 'https://www.kaggle.com/datasets/parisrohan/credit-score-classification' #just for convinience, not important
    dataset_name = "parisrohan/credit-score-classification"

    #reate 'data' folder if it doesnt exist
    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_folder_path = os.path.join(root_dir, 'data')
    os.makedirs(data_folder_path, exist_ok=True)
    
    #activating kaggle api
    api = KaggleApi()
    api.authenticate()
    
    #self-explainatory
    api.dataset_download_files(dataset_name, path=data_folder_path, unzip=True)
    
    return True