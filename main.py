from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation

from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig



import sys

if __name__ == "__main__":
    try:
        # data ingestion
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info(f"Initiating data ingestion config")
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion Completed")
        print(dataingestionartifact)
        # data validation
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        datavalidation = DataValidation(data_ingestion_artifact=dataingestionartifact, data_validation_config= datavalidationconfig)
        logging.info(f"Initiating data validation")
        datavalidationartifact = datavalidation.initiate_data_validation()
        logging.info(f"Data Validation Completed")
        print(datavalidationartifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
