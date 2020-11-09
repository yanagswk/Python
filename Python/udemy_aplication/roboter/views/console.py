# テンプレートのtxtを探して、robotに返してあげる。
import os
import string

import termcolor


def get_template_dir_path():
    """
    templareのディレクトリーのpathを返す
    """
    template_dir_path = None
    try:
        import settings
        if settings.TEMPLATE_PATH:
            template_dir_path = settings.TEMPLATE_PATH
    except ImportError:
        pass

    if not template_dir_path:
        # dirnameとabspathを使い, 実行中のスクリプトのディレクトリ名を取得する
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir_path = os.path.join(base_dir, 'templates')

    return template_dir_path


def find_template(temp_file):
    """
    テンプレートが存在するか確認する。
    """
    template_dir_path = get_template_dir_path()
    # hello.txtがあるか確認
    temp_file_path = os.path.join(template_dir_path, temp_file)
    if not os.path.exists(temp_file_path):
        raise NoTemplateError('Could not find {}'.format(temp_file))
    return temp_file_path


def get_template(template_file_path, color=None):
    """
    templateをgetする
    """
    template = find_template(template_file_path)
    with open(template, 'r', encoding="utf-8") as template_file:
        contents = template_file.read()
        # rstripで文字列の右を削除
        contents = contents.rstrip('\n')
        contents = '{spliter}\n{contents}\n{spliter}\n'.format(
            contents=contents, spliter="=" * 60)
        contents = termcolor.colored(contents, color)
        return string.Template(contents)
