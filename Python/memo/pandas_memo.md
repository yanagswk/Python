# pandas
* inplace=True
  * 元のDataFrameが変更される。デフォルトでは変更されず、新しいDataFrameが返される。 

* df.empty  
  * データフレームが空の時    

* axis  
  * axis=0('index') →列ごとに処理を行う。つまり、垂直方向に次元が圧縮される。結果、行が残る
  * axis=1('columns')→行ごとに処理を行う。つまり、水平方向に次元が圧縮される。結果、列が残る  
  ![サンマの塩焼き](https://qiita-user-contents.imgix.net/https%3A%2F%2Fi.stack.imgur.com%2FDL0iQ.jpg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=738e577fd04e707cc16bea4a1f5a84d5)   

* データ結合  
  * concat  
    * DataFrameオブジェクトを一つのリストに格納して、concat関数に渡す。
    * axis=0(デフォルト)が縦方向に結合。axis=1が横方向に結合。
  * append  
    * 一つのオブジェクトを既存のDataFrameに追加するときは、appendでもOK。  
  * merge  
    * 共通列名で結合。  
      on="列名"で指定列をキーとして結合。指定なしならすべての共通列名がキーになる。  
      how="inner" (デフォルト) キーを見て、両方のテーブル共通してあるデータのみ残す。  
      how="left" キーを見て、左テーブル(第一引数)のデータは全て残す。　　
      how="right"　キーを見て、右テーブル(第二引数)のデータは全て残す。  
      how="outer"  キーを見て、片方のテーブルにしかないデータも全て残す。  
    * 異なる列名で結合  
      left_on, right_onを使う。この場合、2つの列が残るので、必要ない場合はdrop()メソッドで削除する。  

* ignore_index=True  
  * concatやappendをするとき、元の行番号のまま追加が行われるが、ignore_index=Trueを入れると、パラメータを指定することで、新たな行番号を割り当てることができる。  

* join
  * デフォルト値は'outer'ですべての列を残す。'join='inner'とするとデータセットの間で共通する列だけを残すことが出来る。

* 欠損値  
  * isnull() 
    * 欠損値をTrue/Falseで返してくれる。Trueがあれば欠損値あり。 sum()を付けるとTrue/Falseの結果の数を返してくれる。  
  * fillna()  
    * 引数に値を入れると欠損値の穴埋めができる。  
    * fillna(method='ffill')とすると、欠損値を前方の値で置き換える。'bfill'とすると後方の値で置換える。
  * dropna()  
    * 欠損値を削除する。  
  * interpolate()
    * 欠損値を等間隔で補間する。  
  * skipnaパラメータ
    * meanやsumの引数にskipna＝Trueで、欠損値をスキップして計算する。skipnaを入れないで計算すると、計算する値に謙遜地があった場合はNanになる。

* 日付、時間  
  * to_datetime()を用いると文字列を、datetime型に変換できる。datetime型は「dt」を使うことで、年のみなどを抽出するなどが可能。
  dt.strftime("%Y%m")など。  
  * to_timedeltaは、シリアル値をdatetimeに統一できる。
  * strftime  
    * datetime型から文字列  
  * strptime  
    * 文字列からdatetime型。timedeltaを使って演算することが可能。  
  * relativedeltaモジュールを使うと、日や時間の計算が楽。  

* groupby
  * groupby("XXXX").sum()で、まとめたい列と集計方法(sumなど)を指定する。  
  * まとめたい列が複数ある場合は、リスト形で指定することが出来る。  
  * groupbyを使うと、デフォルトでグループラベルが index になる。index にしたく無い場合は as_index=False を指定する。
  * pd.Grouperは、数日おきなど特定の周期/間隔でグループ分けするときに用いる。    

* pd.pivot_table  
  * pd.pivot_table(join_data, index="item_name", columns="payment_month", values=["price", "quantity"], aggfunc="sum",fill_value=0)  
  index,columnsを指定し、valuesで集計する項目、aggfuncで集計方法を指定して、表を作れる。  fill_valueは欠損値を保管する値。  

* pd.unique()  
  * 引数で指定した物の重複を除外したユニークなデータを抽出する。

* pd.nunique()  
  * 引数で指定した物の重複を除外したユニークな数を抽出する。

* sort_values(by=[""], ascending=True)  
  * by=[""]にソートしたい列名を入れ、ascending=Trueで昇順(デフォルト)。Falseで降順になる。  
  * sort_indexで行(縦方向)に対して、ソートを行う。  

* any()  
  * デフォルト(axis=0)で列に対してTrueが一つでもあれば、Trueと判定するメソッド。
  axis=1とすれば行に対して行う。  
  * isnull().any()とすることで、欠損値があるかを判断できる。  

* loc  

* 否定演算子  
  * ~flg_is_nullは「flg_is_null == False」と同義。  

* 関数(skipna=False)  
  * sumなどの関数の引数にskipnaを入れることで、NaNデータを無視するかを設定できる。skipna=Falseの場合、NaNが存在するときは、NaNと表示される。  

* str.isdigit()  
  * すべての文字が数値ならTrue、そうでなければFalse。  

* agg()  
  * 一度に複数の処理ができる。  
  agg(["mean", "median", "max", "min"]）のような書き方。  

* weekday  
  * 月曜日が0、日曜日が6で数値が取得できる。  

* 型がobject  
  * pandasの文字列は、objectと呼ばれる。  

* reset_index  
  * 引数に何もして何も指定しいないと、連番が新たなindexとなり、元のindexが新たな列として残る。  
    reset_index(drop=True)とすると、元のインデックスは削除され残らない。  

* astype()  
  * NumPy配列ndarrayのメソッドastype()でデータ型dtypeを変換（キャスト）することができる。  

* to_numeric()
  * 列を数値に変換する。
  * csvから数字を読み込んだはずなのに、型がfloat64でなくobjectとなってしまう場合、数字以外に文字列が含まれてしまっている。to_numeric(errors='ignore')を使うと、数値以外の値を強制的に NaN にすることができる。errors='raise'はデフォルトで、エラーを起こす。errors='ignore'は列を数字に変換する事なく、そのまま。

* shape  
  * DateFrameの行と列の数を教えてくれる。タプルで(行、列)と表示される。

* set_option







   
  
