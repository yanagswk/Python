import requests
import pprint

import settings
from views import find_file


class GetApi:
    """
    apiを取得するクラス
    """
    freeword = ''
    api_key = 'rest'

    def __init__(self, freeword, birth_place, keyword):
        self.birth_place = birth_place
        self.keyword = keyword
        self.freeword = freeword
        self.hit_per_page = settings.HIT_PER_PAGE
        self.url = settings.API_URL
        self.keyid = settings.KEYID
        self.restrants_dict = self.get_requests()

    def get_requests(self):
        params = {}
        params['keyid'] = self.keyid
        params['hit_per_page'] = self.hit_per_page
        params['freeword'] = self.freeword
        response = requests.get(self.url, params)
        return response.json()

    def get_rest(self):
        """
        レストラン情報を取得
        """
        try:
            return self.restrants_dict[self.api_key]
        except KeyError:
            template = find_file.get_template('error_keyword.txt')
            keyword = input(template.substitute({'error_keyword':
                                                 self.keyword}))
            return GetApi('{},{}'.format(self.birth_place, keyword),
                          self.birth_place, keyword).get_rest()


# response = requests.get(url, params)

# # print(response)
# # pprint.pprint(response.json())

# results = response.json()
# restrants = results['rest']

# # pprint.pprint(restrants[0]['name'])
# # pprint.pprint(len(restrants))
