import logging


def get_logger(name, LIGFILE="LOGFILE.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ハンドラ設定(DEBUG)
    fh = logging.FileHandler(LIGFILE)
    fh.setLevel(logging.DEBUG)
    fh_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_format)

    # loggerにハンドラ設定とコンソール設定を追加
    logger.addHandler(fh)

    return logger
