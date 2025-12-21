from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys



if __name__=='__main__':
    try:
        TrainingPipelineConfig = TrainingPipelineConfig()
        data_ingestion = DataIngestion()
        data_ingestion =data_ingestion(data_ingestion)
        logging.info("Initiate the data Ingestion")
        datingestionartifact = data_ingestion.initiate_data_ingestion()
        print(datingestionartifact)


    except Exception as e:
        raise NetworkSecurityException(e,sys)
