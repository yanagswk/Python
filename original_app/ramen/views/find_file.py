
import termcolor
import os
import string

import settings

template_dir_path = settings.TEMPLATE_PATH


def get_template_dir_path():
    """
    settingsからディレクトリのpathを返す。
    """
    global template_dir_path
    if template_dir_path:
        return template_dir_path

    else:
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        template_dir_path = os.path.join(base_dir, 'templates')
    return template_dir_path


def find_template(txt_file):
    """
    ファイルが存在するかを確認。
    """
    template_dir_path = get_template_dir_path()
    template_file_path = os.path.join(template_dir_path, txt_file)
    if not os.path.exists(template_file_path):
        raise FileNotFoundError(f'{txt_file}が存在しません。')
    return template_file_path


def get_template(txt_file):
    """
    templateを読み込む。
    """
    template = find_template(txt_file)
    with open(template, encoding='utf-8') as template_file:
        read_template = template_file.read()
        # read_template = read_template.rstrip('\n')
        read_template = termcolor.colored(read_template,
                                          settings.TEMPLATE_COLOR)
        return string.Template(read_template)
