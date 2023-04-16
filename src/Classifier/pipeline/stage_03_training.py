from Classifier.components import PrepareCallback, Training
from Classifier import logger


def main():
    logger.info('start training')
    prepare_callbacks = PrepareCallback()
    callback_list = prepare_callbacks.get_tb_chkt_call_backs()
    
    training = Training()
    training.get_base_model()
    training.train_valid_generator()
    training.train(
        callback_list=callback_list
    )
    logger.info(f"x==========     training finish =========X")

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        logger.exception(e)
        raise e