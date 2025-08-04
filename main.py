from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation

from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
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
        # data transformation
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        datatransformation = DataTransformation(datavalidationartifact,data_transformation_config)
        logging.info("Initiate data transformation")
        data_tranformation_artifact = datatransformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(data_tranformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
