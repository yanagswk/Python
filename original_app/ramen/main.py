import logging
import settings
from robot import hello_robot
from api.get_api_data import GetApi

from log.logger import get_logger

logger = get_logger(__name__)


def rest(restrants, serch_word, page_count_test, flag=False):
    """
    レストラン一覧表示
    """
    rest_lists = [restrant["name"] for restrant in restrants[
        0 + page_count_test:10 + page_count_test]]

    if flag:
        flag = False
        hello_robot.rest_hit(serch_word, len(restrants))

    for index, rest_name in enumerate(rest_lists):
        print('{}: {}'.format(index + page_count_test, rest_name))

    page = hello_robot.next_page()

    next_page(restrants, serch_word, page, page_count_test)


def detail_info(restrants, serch_word, page, page_count_test):
    """
    レストラン一覧ページ
    """
    result = hello_robot.detail_info(int(page),
                                     restrants[int(page)]["name"], restrants)
    if result.lower() == "b":
        rest(restrants, serch_word, page_count_test)

    else:
        print("レストラン一覧ページに戻りたい場合は「b」を押してください。")
        detail_info(restrants, serch_word, page, page_count_test)


def next_page(restrants, serch_word, page, page_count_test):
    """
    お店の番号 or nextページ
    """
    try:
        if page.lower() == "n":
            hello_robot.next_rest()
            print("次の10件を表示します。")
            page_count_test += 10
            rest(restrants, serch_word, page_count_test)

        elif page.lower() == "b":
            if page_count_test - 10 < 0:
                print("お店は存在しません。")
                rest(restrants, serch_word, page_count_test)
            else:
                page_count_test -= 10
                rest(restrants, serch_word, page_count_test)

        else:
            detail_info(restrants, serch_word, page, page_count_test)

    except Exception:
        print("お店の番号か、「n」か「b」を押してください")
        rest(restrants, serch_word, page_count_test)


def main():

    page_count_test = 0
    uesr_name = hello_robot.hello()
    birth_place = hello_robot.birth_place(uesr_name)
    keyword = hello_robot.keyword(birth_place)
    serch_word = '{},{}'.format(birth_place, keyword)

    logger.debug("キーワード「{}」で、ぐるなびAPI取得開始".format(serch_word))
    # ぐるなびAPIにてキーワードを投げて、レストラン情報を取得する。
    restrants = GetApi(serch_word, birth_place, keyword).get_rest()

    logger.debug("ぐるなびAPI取得完了")

    rest(restrants, serch_word, page_count_test, flag=True)


if __name__ == "__main__":
    main()
