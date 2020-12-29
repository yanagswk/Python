# UnitTest  

* アサーションメソッド一覧  

| 結果  |                          詳細                           |
| :---: | :-----------------------------------------------------: |
| assertEqual(a, b)   |                          a == b                          |
| assertNotEqual(a, b)  | a != b |
| assertTrue(x) |      bool(x) is True      |
| assertFalse(x) |      bool(x) is False      |
| assertIs(a, b) |      a is b      |
| assertIsNot(a, b) |      a is not b      |
| assertIsNone(x) |      	x is None      |
| assertIsNotNone(x) |      	x is not None      |
| assertIn(a, b) |      	a in b      |
| assertNotIn(a, b) |      	a not in b      |
| assertIsInstance(a, b) |      	isinstance(a, b)      |
| assertNotIsInstance(a, b) |      	not isinstance(a, b)     |
| assertGreater(a, b) |      	-a > b      |
| assertGreaterEqual(a, b) |      		a >= b      |
| assertLess(a, b) |      	a < b      |
| assertLessEqual(a, b) |      		a <= b      |
| assertRegexpMatches(s, r) |      	r.search(s)      |
| assertNotRegexpMatches(s, r) |      	not r.search(s)      |
| assertDictContainsSubset(a, b) |      		all the key/value pairs in a exist in b     |

<br>

* unittestは次の手順でテストケースを作成する。  
  * testで始まる名前でテストモジュールを作成。  
  * unittest.TestCaseクラスのサブクラスを作成。  
  * testで始まる名前でテストメソッドを実装。  
  * テストメソッド内でテスト対象の処理を実行。  
  * テストメソッド内で1つ以上のアサーションメソッドを利用し、実行結果を確認する。  

まずは、テスト対象になるアプリケーションを用意。  
キーワードによる書籍検索ができる。
```python
# bookserch/api.py  

import json
from urllib import request, parse

def get_json(param):
    with request.urlopen(build_url(param)) as f:
        return json.load(f)

def get_data(url):
    with request.urlopen(url) as f:
        return f.read()

def build_url(param):
    query = parse.urlencode(param)
    return ('https://www.googleapis.com'
            f'/books/v1/volumes?{query}')
```  
```python  
# bookserch/core.py 

import sys
import os

import imghdr
import pathlib
from api import get_data, get_json

class Book:
    """APIレスポンスのVolumeInfo要素に対応"""

    def __init__(self, item):
        self.id = item['id']
        volume_info = item['volumeInfo']
        for k, v in volume_info.items():
            setattr(self, str(k), v)

    def __repr__(self):
        return str(self.__dict__)

    def save_thumbnails(self, prefix):
        """サムネイル画像を保存する"""
        paths = []
        for kind, url in self.imageLinks.items():
            thumbnail = get_data(url)
            # 画像データから拡張子を判定
            ext = imghdr.what(None, h=thumbnail)
            # pathlib.Pathは/演算子でパスを追加できる
            base = pathlib.Path(
              prefix) / f'{self.id}_{kind}'
            filename = base.with_suffix(f'.{ext}')
            filename.write_bytes(thumbnail)
            paths.append(filename)
        return paths

def get_books(q, **params):
    """書籍検索を行う"""
    params['q'] = q
    data = get_json(params)
    return [Book(item) for item in data['items']]


if __name__ == "__main__":

    books = get_books(q='python')
    print(books[0])

```  

次のようにキーワードの書籍検索ができる。  
```python
>>>python .\core.py  
{'id': 'NP3yag-zvhAC', 'title': 'Python入門', .......
```  

上記を使って、テストケースを作成してみる。  

以下は、bookserch.api.build_url()関数の正常と失敗のケースである。  

```python  
# bookserch/test_api.py 

import sys
import os

import unittest
from booksearch.api import build_url

class BuildUrlTest(unittest.TestCase):
    # 正常ケース
    def test_build_url(self):
        expected = 'https://www.googleapis.com/books/v1/volumes?q=python'
        # build_url()がテスト対象の処理
        actual = build_url({'q': 'python'})
        # アサーションメソッドの利用
        self.assertEqual(expected, actual)
    
    # 失敗ケース
    def test_build_url_empty_param(self):
        expected = 'https://www.googleapis.com/books/v1/volumes'
        actual = build_url({})
        self.assertNotEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
```  

テスト結果が以下である。正常と失敗の両ケースがある。

```python
>>> python test_api.py  
.F
======================================================================
FAIL: test_build_url_empty_param (__main__.BuildUrlTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_api.py", line 20, in test_build_url_empty_param
    self.assertEqual(expected, actual)
AssertionError: 'https://www.googleapis.com/books/v1/volumes' != 'https://www.googleapis.com/books/v1/volumes?'
- https://www.googleapis.com/books/v1/volumes
+ https://www.googleapis.com/books/v1/volumes?
?                                            +


----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=1)
```
  

* 前処理、後処理が表示なテストケース--setUp(), tearDown()  
例えば、booksearch.core.Bookクラスのメソッドsave_thumbnails()は、取得したサムネを保存するメソッドである。このメソッドの正常をテストするには、テスト実装前に保存先ディレクトリにサムネが存在しないことを保証する必要がある。  
そのような場合に、メソッドsetUp()でテスト実装前に空のディレクトリを作成し、メソッドtearDown()でテスト実装後に、そのディレクトリの後片付けを行う。
 
```python 
# bookserch/test_core.py 

import pathlib
import unittest
# tempfileは一時的にディレクトリやファイルの作成に役立つモジュール
from tempfile import TemporaryDirectory
from booksearch.core import Book

THUMBNAIL_URL = (
    'http://books.google.com/books/content'
    '?id=OgtBw76OY5EC&printsec=frontcover'
    '&img=1&zoom=1&edge=curl&source=gbs_api'
)

class SaveThumbnailsTest(unittest.TestCase):
    def setUp(self):
        # 一時ディレクトリを作成する
        self.tmp = TemporaryDirectory()

    def tearDown(self):
        # 一時ディレクトリを片付ける
        self.tmp.cleanup()

    def test_save_thumbnails(self):
        book = Book({'id': '', 'volumeInfo': {
            'imageLinks': {
                'thumbnail': THUMBNAIL_URL
            }}})
        # 処理を実行し、ファイルが作成されることを確認する
        filename = book.save_thumbnails(self.tmp.name)[0]
        self.assertTrue(pathlib.Path(filename).exists())

if __name__ == '__main__':
    unittest.main()
```  

テスト結果は、以下である。  

```python
>>> python test_core.py
.
----------------------------------------------------------------------
Ran 1 test in 0.151s

OK
```

python -m unittest と実行すると、ディレクトリ内のテストをまとめて実行できる。  

```python
>>> python -m unittest

.F.
======================================================================
FAIL: test_build_url_empty_param (test_api.BuildUrlTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\programing\test\workspace\tests\test_api.py", line 20, in test_build_url_empty_param
    self.assertEqual(expected, actual)
AssertionError: 'https://www.googleapis.com/books/v1/volumes' != 'https://www.googleapis.com/books/v1/volumes?'
- https://www.googleapis.com/books/v1/volumes
+ https://www.googleapis.com/books/v1/volumes?
?                                            +


----------------------------------------------------------------------
Ran 3 tests in 0.145s

FAILED (failures=1)
```  

-vオプションをつけると、より詳しい情報が表示される。  
また、アサーションメソッドの引数にmsgを指定すると、テスト失敗時にメッセージを表示する。
```python
>>> python -m unittest -v
test_build_url (test_api.BuildUrlTest) ... ok
test_build_url_empty_param (test_api.BuildUrlTest) ... FAIL
test_save_thumbnails (test_core.SaveThumbnailsTest) ... ok 

======================================================================
FAIL: test_build_url_empty_param (test_api.BuildUrlTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\programing\test\workspace\tests\test_api.py", line 20, in test_build_url_empty_param
    self.assertEqual(expected, actual, msg='テスト失敗')
AssertionError: 'https://www.googleapis.com/books/v1/volumes' != 'https://www.googleapis.com/books/v1/volumes?'
- https://www.googleapis.com/books/v1/volumes
+ https://www.googleapis.com/books/v1/volumes?
?                                            +
 : テスト失敗

----------------------------------------------------------------------
Ran 3 tests in 0.131s

FAILED (failures=1)
```  

* テスト失敗時の結果を抑制する  

デコレータunittest.expectedFailureをつけると、テストケースが失敗することがわかっている場合、明示することができる。  

```python
# bookserch/test_api.py

# 省略

class BuildUrlTest(unittest.TestCase):
    # 省略
    
    # 失敗ケース
    
    def test_build_url_empty_param(self):
        expected = 'https://www.googleapis.com/books/v1/volumes'
        actual = build_url({})
        self.assertNotEqual(expected, actual)
```

実行結果が、以下である。  

```python
>>> python -m unittest -v

test_build_url (test_api.BuildUrlTest) ... ok
test_build_url_empty_param (test_api.BuildUrlTest) ... expected failure
test_save_thumbnails (test_core.SaveThumbnailsTest) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.149s

OK (expected failures=1)
```  

expected failureと表示され、詳細表示の抑制ができた。    
仮に、意図に反して成功した場合は、unexpected successと表示されるので、異常を早期発見できる。  
あくまで、このデコレータは一時に対応でのみ利用し、可能な限りすべてのテストが成功する状態にすることを推奨する。  

# ユースケース別のテストケースの実装  
* [環境依存のテストをスキップする](#section1)  
* [例外の発生をテストする](#section2)
* [違うパラメータで同じテストを繰り返す](#section3)
* [コンテキストマネージャーをテストする](#section4)

# <h3><a id="section1" href="#section1">環境依存のテストをスキップする</a></h3>  

なんらかの理由でテストケースを残しときたかったり、環境依存の機能を使うなど、テストケースをスキップしたい場合は、デコレータunittest.skip()や、デコレータunittest.skipIf()を使う。  

```python
# bookserch/test_api.py  

# 省略
class BuildUrlTest(unittest.TestCase):
    # 省略  

    # 引数にスキップする理由を渡す
    @unittest.skip('this is a skip test')
    def test_nothing_skip(self):
        pass

    # 実行中のPythonバージョンが3.6より大きければスキップ
    @unittest.skipIf(sys.version_info > (3, 6),
                     'this is a skipIf test')
    def test_nothing_skipIf(self):
        pass

```

実行結果が、以下である。  

```python
.xss
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK (skipped=2, expected failures=1)
PS D:\programing\test\workspace\tests> python test_api.py -v
test_build_url (__main__.BuildUrlTest) ... ok
test_build_url_empty_param (__main__.BuildUrlTest) ... expected failure
test_nothing_skip (__main__.BuildUrlTest) ... skipped 'this is a skip test'
test_nothing_skipIf (__main__.BuildUrlTest) ... skipped 'this is a skipIf test'

----------------------------------------------------------------------
Ran 4 tests in 0.010s

OK (skipped=2, expected failures=1)
```  

テストクラス自体にunittest.skip()やunittest.skipIf()をつけた場合は、そのクラスに定義されているすべてのテストケースがスキップされる。  

# <h3><a id="section2" href="#section2">例外の発生をテストする</a></h3>  

# <h3><a id="section3" href="#section3">違うパラメータで同じテストを繰り返す</a></h3>  

# <h3><a id="section4" href="#section4">コンテキストマネージャーをテストする</a></h3>  



