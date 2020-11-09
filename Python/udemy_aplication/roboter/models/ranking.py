# csvに書き込むためのランキングモデルを作成

import collections
import csv
import logging
import os
import pathlib

from roboter.lib.roboter_enum import RankingEnum

logger = logging.getLogger(__name__)

# RANKING_COLUMN_NAME = 'NAME'
# RANKING_COLUMN_COUNT = 'COUNT'
# RANKING_CSV_FILE_PATH = 'ranking.csv'


class CsvModel(object):
    """
    csvのベースモデル
    """
    def __init__(self, csv_file):
        self.csv_file = csv_file
        if not os.path.exists(csv_file):
            # 既存ファイルの日時更新、存在しない場合は空のファイルを作成(touch)
            pathlib.Path(csv_file).touch()


class RankingModel(CsvModel):
    """
    CSVに書き込むランキングモデルを生成するクラス
    """
    def __init__(self, csv_file=None, *args, **kwargs):
        if not csv_file:
            csv_file = self.get_csv_file_path()
        super().__init__(csv_file, *args, **kwargs)
        self.column = [RankingEnum.RANKING_COLUMN_NAME.value,
                       RankingEnum.RANKING_COLUMN_COUNT.value]
        self.data = collections.defaultdict(int)
        self.load_data()

    def get_csv_file_path(self):
        """
        settingsで設定されている場合はcsvパスを使用し、そうでない場合はデフォルト
        """
        csv_file_path = None
        try:
            import settings
            if settings.CSV_FILE_PATH:
                csv_file_path = settings.CSV_FILE_PATH
        except ImportError:
            pass

        if not csv_file_path:
            csv_file_path = RankingEnum.RANKING_CSV_FILE_PATH.value
        return csv_file_path

    def load_data(self):
        """
        csvを読み込む
        """
        with open(self.csv_file, 'r+') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.data[row[RankingEnum.RANKING_COLUMN_NAME.value]] = int(
                    row[RankingEnum.RANKING_COLUMN_COUNT.value])
        return self.data

    def save(self, force=True):
        """
        csvファイルにデータをセーブする。
        """

        # logger.info({
        #     'action': 'save',
        #     'csv_file': self.csv_file
        #     'force': force
        #     'status': 'run'
        # })

        with open(self.csv_file, 'w+') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.column)
            writer.writeheader()

            for name, count in self.data.items():
                writer.writerow({
                    RankingEnum.RANKING_COLUMN_NAME.value: name,
                    RankingEnum.RANKING_COLUMN_COUNT.value: count
                })

        # logger.info({
        #     'action': 'save',
        #     'csv_file': self.csv_file,
        #     'force': force
        #     'status': 'success'
        # })

    def get_most_popular(self, not_list=None):
        """
        ランキング上位のデータを取得する。
        """
        if not_list is None:
            not_list = []

        if not self.data:
            return None

        sorted_data = sorted(self.data, key=self.data.get, reverse=True)
        for name in sorted_data:
            if name in not_list:
                continue
            return name

    def increment(self, name):
        """
        ランキングを上げる。
        """
        # データをプラスして、入れている。
        self.data[name.title()] += 1
        self.save()
