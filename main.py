from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig



import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info(f"Initiating data ingestion config")
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
