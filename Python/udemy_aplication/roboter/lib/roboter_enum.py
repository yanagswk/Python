from enum import Enum

class RobotNameEnum(Enum):
    DEFAULT_ROBOT_NAME = 'Roboko'


class RankingEnum(Enum):
    RANKING_COLUMN_NAME = 'NAME'
    RANKING_COLUMN_COUNT = 'COUNT'
    RANKING_CSV_FILE_PATH = 'ranking.csv'