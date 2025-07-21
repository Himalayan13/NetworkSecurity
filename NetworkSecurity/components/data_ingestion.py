from NetworkSecurity.exception.exception import NetworkSecurityException

from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact

from NetworkSecurity.logging.logger import logging

import os
import sys
import numpy as np 
import pandas as pd 
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_collection_as_dataframe(self):
        """
        reading data from mongo db
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL) 
            collection  = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_data_into_feature_store(self,dataframe:pd.DataFrame): 
        """"
        we store the data from the mongodb to the feature store 
        so that we dont have to keep on accessing the db server
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #creating the folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            #storing the dataframs as csv in the feature store
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info(
               f"Performed train test split on dataframe"
            )
            logging.info(
                f"Exited train test split method of data ingestion class"
                )
            
            # Since both train.csv and test.csv are in the same ingested folder, 
            # this single call to os.makedirs ensures the folder exists for both files.
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train test file path")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index = False, header = True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index = False, header = True
            )

            logging.info(f"Export of train test file path complete")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)
            
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
