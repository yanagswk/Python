import logging.config

import logtest

# main(一番初めに)でlogging.basicConfigを設定したら、あとはloggerを使う。

logging.basicConfig(level=logging.INFO)

class NonPassFilter(logging.Filter):
  def filter(self, recod):
    log_message = recod.getMessage()
    # passwordが入っていなければ、ログメッセージ出力
    return 'password' not in log_message

logger = logging.getLogger(__name__)
logger.addFilter(NonPassFilter())
logger.info('from main')
logger.info('from main password = "test"')

# logtest.do_something()


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.debug


# # 高い
# logging.critical('critical')
# logging.error('error')
# logging.warning('warning')
# logging.info('info')
# logging.debug('debug')
# # 低い