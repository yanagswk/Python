# import logging
import logging.config

# filenameでログファイルを指定
# logging.basicConfig(level=logging.INFO, filename='test.log')

# formatでフォーマットを指定できる。%sで変数をいれることもできる。
# formatter = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(message)s'
# logging.basicConfig(level=logging.INFO, format=formatter)
# logging.info('info {} {}', format("a", "b"))

# fileConfig
# logging.config.fileConfig('logging.ini')

# dictConfig
logging.config.dictConfig({
    'version': 1,
    # フォーマットの設定
    'formatters': {
        'customFormat': {
            'format': '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(message)s'
        },
    },
    # ハンドラの設定
    'handlers': {
        'customStreamHandler': {
            'class': 'logging.StreamHandler',
            'formatter': 'customFormat',
            'level': logging.DEBUG
        }
    },
    # ロガーの対象一覧
    'root': {
        'handlers': ['customStreamHandler'],
        'level': logging.WARNING,
    },
    'loggers': {
        'outputLogging': {
            'handlers': ['customStreamHandler'],
            'level': logging.DEBUG,
            'propagate': 0
        }
    }
})

# logger = logging.getLogger(__name__)
# logger = logging.getLogger("outputLogging")

# logger.critical('critical')
# logger.error('error')
# logger.warning('warning')
# logger.info('info')
# logger.debug('debug')


def setup_logger(name, logfile="LOGFILE.txt"):
    # getLogger(__name__)でこのファイル名取得
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ファイルハンドラ設定
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter(
        '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(message)s')
    fh.setFormatter(fh_formatter)

    # コンソール出力設定
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter(
        '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(message)s')
    ch.setFormatter(ch_formatter)

    # loggerに追加
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
