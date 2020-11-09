
import termcolor
import os
import string

import settings


class GetTemplate():
    """
    templateを読み込むクラス
    """

    def __init__(self):
        self.template_dir = self.get_template_dir_path()

    def get_template_dir_path(self):
        """
        settingsからディレクトリのpathを返す。
        """
        template_dir_path = None
        try:
            import settings
            template_dir_path = settings.TEMPLATE_PATH
        except ImportError:
            # TODO logger導入
            print('settingsが存在しません。')

        if not template_dir_path:
            base_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            template_dir_path = os.path.join(base_dir, 'templates')
        return template_dir_path

    def find_template(self, txt_file):
        """
        ファイルが存在するかを確認。
        """
        # template_dir_path = get_template_dir_path()
        template_file_path = os.path.join(self.template_dir, txt_file)
        if not os.path.exists(template_file_path):
            raise FileNotFoundError(f'{txt_file}が存在しません。')
        return template_file_path

    def get_template(self, txt_file):
        """
        templateを読み込む。
        """
        template = self.find_template(txt_file)
        with open(template, encoding='utf-8') as template_file:
            read_template = template_file.read()
            # read_template = read_template.rstrip('\n')
            read_template = termcolor.colored(read_template,
                                              settings.TEMPLATE_COLOR)
            return string.Template(read_template)
