* datetime.dateクラス
  * 日付を扱うためのクラス。datatime.date(2016, 7, 8)のように指定する。 
  * dateクラスのインスタンスに「year, month, day」があり、d.yearのようにすると年の要素が取り出せる。

* datetime.timeクラス
  * 時間を扱うためのクラス。datetime.time(10, 20, 0)のように指定する。  
  * timeクラスのインスタンスに「hour, minute, secound」があり、t.hourのようにすると時の要素が取り出せる。

* datetime.datetime
  * 日付と時間を扱うためのクラス。datetime.datetime(2016, 7, 8, 10, 20, 0)のように指定する。  
  * dateクラス,timeクラスのインスタンスがあり、d.yearやt.hourのように各要素が取り出せる。  
  * d.date()でdateクラスに変換可能。

* datetime.timedeltaクラス  
  * 日付や時刻の差を扱うクラス。日時の演算などに使用する。timedelta(days=3)のようにすると3日分を表す。足すと3日後、引くと3日前になる。  

* strftime  
    * datetime型から文字列  
    * datetime型から文字列の場合、「　f{datetime:%Y%m%d}　」が使える。
* strptime  
    * 文字列からdatetime型。timedeltaを使って演算することが可能。datetimeにするからpoint=数字にすると覚えるようにする。


    