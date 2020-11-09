import logging
 
# ログの出力名を設定
logger = logging.getLogger('LoggingTest')
 
# ログレベルの設定
logger.setLevel(10)
 
# ログのコンソール出力の設定
sh = logging.StreamHandler()
logger.addHandler(sh)
 
# ログのファイル出力先を設定
fh = logging.FileHandler('test.log')
logger.addHandler(fh)
 
# ログの出力形式の設定
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
 
logger.log(20, 'info')
logger.log(30, 'warning')
logger.log(100, 'test')
 
logger.info('info')
logger.warning('warning')