from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.artifact_entity import DataValidationArtifact



if __name__=='__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logger.info("Initiate the data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logger.info("Completed the data Ingestion")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logger.info("Initiate the data Validation")
        data_validation.initiate_data_validation()
        logger.info("Completed the data Validation")






    except Exception as e:
        raise NetworkSecurityException(e,sys)
