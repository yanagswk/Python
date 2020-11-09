# レストラン以外のロボットが作られるかもしれないから、ベースはRobot
import logging

from roboter.models import ranking
from roboter.views import console

from roboter.lib.roboter_enum import RobotNameEnum

import log

# DEFAULT_ROBOT_NAME = 'Roboko'

# logger = log.setup_logger(__name__)
# logger = logging.getLogger(__name__)
logger = logging.getLogger("outputLogging")


class Robot(object):
    """
    ロボットのベースモデル
    """
    def __init__(self, name=RobotNameEnum.DEFAULT_ROBOT_NAME.value,
                 user_name='', speak_color='green'):
        self.name = name
        self.user_name = user_name
        self.speak_color = speak_color

    def hello(self):
        """
        ユーザーに対してあいさつをする。
        """
        while True:
            template = console.get_template('hello.txt', self.speak_color)
            user_name = input(template.substitute({
                'robot_name': self.name
            }))

            logger.info('info {}'.format(self.name))

            if user_name:
                # title()で単語の先頭を大文字、他を小文字
                self.user_name = user_name.title()
                break


class RestaurantRobot(Robot):
    """
    レストランのモデル
    """
    def __init__(self, name=RobotNameEnum.DEFAULT_ROBOT_NAME.value):
        super().__init__(name=name)
        self.ranking_model = ranking.RankingModel()

    def _hello_decorator(func):
        """
        ユーザに挨拶をしていない場合挨拶をするデコレーター
        """
        def warpper(self):
            if not self.user_name:
                self.hello()
            return func(self)
        return warpper

    @_hello_decorator
    def recommend_restaurant(self):
        """
        レストランのおすすめをユーザーに表示
        """
        new_recommend_restaurant = self.ranking_model.get_most_popular()
        if not new_recommend_restaurant:
            return None
        will_recommend_restaurants = [new_recommend_restaurant]
        while True:
            template = console.get_template('greeting.txt', self.speak_color)
            is_yes = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
                'restaurant': new_recommend_restaurant
            }))

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                break

            if is_yes.lower() == 'n' or is_yes.lower() == 'no':
                new_recommend_restaurant = self.ranking_model.get_most_popular(
                    not_list=will_recommend_restaurants
                )
                if not new_recommend_restaurant:
                    break
                will_recommend_restaurants.append(new_recommend_restaurant)

    @_hello_decorator
    def ask_user_favorite(self):
        """
        ユーザーからお気に入りのレストラン情報を収集する
        """
        while True:
            template = console.get_template(
                'which_restaurant.txt', self.speak_color)
            restaurant = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
            }))
            if restaurant:
                self.ranking_model.increment(restaurant)
                break

    @_hello_decorator
    def thank_you(self):
        """
        ユーザにありがとうのメッセージを返す。
        """
        template = console.get_template('good_by.txt', self.speak_color)
        print(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name,
        }))
