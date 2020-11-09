
import logging

def setup_logger(name, logfile='LOGFILENAME.txt'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ハンドラ設定(DEBUG)
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)

    # コンソール出力設定(INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    # loggerにハンドラ設定とコンソール設定を追加
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

