from Classifier.components import Validation
from Classifier.utils import save_json
from pathlib import Path

from Classifier import logger


def main():
    logger.info('start training')
    valid = Validation()
    score=valid.predict()
    save_json(path=Path("score.json"),data={"score":float(score)})
    logger.info(f"x============     evaluation finish =========X")

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        logger.exception(e)
        raise e