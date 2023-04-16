from Classifier.components import PreapareBaseModel
from Classifier import logger

def main():
    logger.info(f">>>> start data ingestion ")
    preapare_base_model = PreapareBaseModel()
    preapare_base_model.update_base_model()
    logger.info(f"x========  prepare base model finish finish  =========X")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(msg=e)
        raise e
