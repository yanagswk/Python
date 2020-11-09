import logging.config

# ログ設定ファイルからログ設定を読み込み
logging.config.fileConfig('logging.conf')

logger = logging.getLogger()

logger.log(20, 'info')
logger.log(30, 'warning')
logger.log(100, 'test')

logger.info('info')
logger.warning('warning')
