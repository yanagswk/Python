# nems_memo
* datetime  
  * モジュールには日時（日付と時刻）を表すdatetime型、日付を表すdate型があるが、それらのオブジェクト同士を引き算して差分を求めると、時間差を表す**timedelta型**のオブジェクトが生成される。日時の差分をkウィ産するときは、timedeltaを使う。  

* df.empty  
  * データフレームが空の時  

* inplace=True
  * 元のDataFrameが変更される。デフォルトでは変更されず、新しいDataFrameが返される。    

* axis  
  * axis=0('index') →列ごとに処理を行う。つまり、垂直方向に次元が圧縮される。結果、行が残る
  * axis=1('columns')→行ごとに処理を行う。つまり、水平方向に次元が圧縮される。結果、列が残る  
  ![サンマの塩焼き](https://qiita-user-contents.imgix.net/https%3A%2F%2Fi.stack.imgur.com%2FDL0iQ.jpg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=738e577fd04e707cc16bea4a1f5a84d5)  

* groupby  
  * pd.Grouperは、数日おきなど特定の周期/間隔でグループ分けするときに用いる。  

* get()  
  * get()は引数に辞書のkeyをいれると値が取得できる。第二引数には、キーが存在しな買った場合に返すデフォルト値を入れる。

  