import requests
import os
from __future__ import absolute_import, unicode_literals

# 環境変数(.bash_profile)に設定されているLINEのトークンを取得
LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')

headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}

data = {"message": "テストでメッセージ送るよ～"}

requests.post("https://notify-api.line.me/api/notify",
              headers=headers,
              data=data)
