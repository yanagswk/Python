import requests
import pprint
import unittest

import sys
import os
sys.path.append(os.path.abspath(
    r"/Users/yanagswk/個人用/Python/original_app/ramen"))

import settings
from api.get_api_data import GetApi


class TestGetTest(unittest.TestCase):
    """ apiを取得するテスト
    """
    def test_get_rest(self):
        """ 指定したキーワードのapiを取得するテスト
        """
        get_api = GetApi("松本,肉", "松本", "肉")
        self.assertTrue(get_api,
                        msg='apiを取得したのにFalseを返しました。')

    def test_get_request(self):
        """ api取得
        """
        pass
