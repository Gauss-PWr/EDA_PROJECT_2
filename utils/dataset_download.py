import os
from kaggle.api.kaggle_api_extended import KaggleApi

link = 'https://www.kaggle.com/datasets/parisrohan/credit-score-classification' #just for convinience, not important
download_path = "./data"
dataset_name = "parisrohan/credit-score-classification"

def download_dataset():
    """create 'data' folder if it doesnt exist"""
    os.makedirs(download_path, exist_ok=True)
    
    """activating kaggle api"""
    api = KaggleApi()
    api.authenticate()
    
    """self-explainatory"""
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)

download_dataset()