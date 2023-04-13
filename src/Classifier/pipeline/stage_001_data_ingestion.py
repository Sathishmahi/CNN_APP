from src.Classifier.components import DataIngestion
from Classifier import logger

def main():
    logger.info(f'>>>> start data ingestion ')
    data_inge=DataIngestion()
    data_inge.download_data()
    data_inge.extract_data()
    logger.info(f'x=========  data ingestion finish  =========X')

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        logger.exception(msg=e)
        raise e 