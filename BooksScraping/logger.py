import logging


def get_logger(name):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.DEBUG,
        filename='logs.txt'
    )

    return logging.getLogger(name)
