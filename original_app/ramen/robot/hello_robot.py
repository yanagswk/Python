from views.find_file import GetTemplate
import settings


def hello():
    """
    ユーザーに挨拶をする
    """
    template = GetTemplate().get_template('hello.txt')
    user_name = input(template.substitute({'robot_name': settings.ROBOT_NAME}))
    return user_name


def birth_place(user_name):
    """
    ユーザーに出身地を聞く
    """
    template = GetTemplate().get_template('birth_place.txt')
    birth_place = input(template.substitute({'user_name': user_name}))
    return birth_place


def keyword(birth_place):
    """
    ユーザーにkeywordを聞く
    """
    template = GetTemplate().get_template('keyword.txt')
    keyword = input(template.substitute({'birth_place': birth_place}))
    return keyword


def rest_hit(serch_word, hit_per_page):
    """
    件数表示
    """
    template = GetTemplate().get_template('store_info.txt')
    hit_tmp = template.substitute({'serch_word': serch_word,
                                   'hit_per_page': hit_per_page})
    print(hit_tmp)


def next_page():
    """
    次の件数に移動
    """
    template = GetTemplate().get_template('next_page.txt')
    next_page = input(template.substitute())
    return next_page


def next_rest():
    """
    次の件数に移動
    """
    template = GetTemplate().get_template('next_rest.txt')
    next_rest = template.substitute()
    return next_rest


def detail_info(index, rest_name, restrants):
    """
    レストランの詳細情報を表示
    """
    template = GetTemplate().get_template('detail_info.txt')
    detail = input(template.substitute({
        'index': index,
        'rest_name': rest_name,
        'name': restrants[index]['name'],
        'address': restrants[index]['address'],
        'opentime': restrants[index]['opentime'],
        'tel': restrants[index]['tel'],
        'access_station': restrants[index]['access']['station'],
        'budget': restrants[index]['budget'],
    }))
    return detail
