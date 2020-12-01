# [参考動画](https://www.udemy.com/course/unscared_git/)

# gitコマンド一覧  

|項目                         |コマンド                                     |備考                                                                                     |
| ---                         | ---                                         | ---                                                                                     |
|ステージへ追加               |git add .                                    |.(ピリオド)ですべて追加                                                                  |
|コミット                     |git commit                                   | git config --global core.editor 'code --wait'で登録したエディタ起動                     |
|                             |git commit -m "コメント"                     |                                                                                         |
|                             |git commit -v                                | 変更内容も表示                                                                          |
|変更差分を確認               |git diff (<ファイル名>)                                    | addする前の変更分。ステージに追加する前にどのような変更を行ったかを確認。                          |
|                             |git diff --staged                            | addした後の変更分。コミットする前にどのような変更を行ったかを確認。                        |
|変更したファイルを確認       |git status                                   | addできるファイルとcommitできるファイルを確認できる                                          |
|                         |git status -s                                   | <span style="color: green; ">M</span>→git add されているけどまだ git commit されていないファイルの一覧    |
|                         |                                                | <span style="color: red; ">M</span>→編集・変更・削除されているが、まだ git add されていないファイルの一覧    |
|                         |                                                | <span style="color: red; ">??</span>→Git管理されていない、かつ .gitignore で管理除外対象にもされていないものの一覧 |
|リポジトリをクローンする     |git clone <githubのurl>                      |                                                                                         |
|コミット履歴を確認           |git log                                      |   --decorateでどのブランチがどのコミットを指しているかを確認できる。                                      |
|                             |git log --oneline                            | 一行でログを表示                                                                        |
|                             |git log -p <ファイル名>                      | ファイルの変更差分を表示。ファイルの中身が開く                                          | 
|                             |git log -n <コミット数>                      | 表示するコミット数を引数に入れる。直前のコミットをみたいなら1をいれる。                                 |
|ファイルの削除               |git rm <ファイル名>                          | リポジトリから削除(コミットしたもの)。ファイルも削除。削除された状態がステージに記録される。            |
|                             |git rm -r <ディレクトリ名>                      | リポジトリから削除(コミットしたもの)。ディレクトリも削除。                                                        |
|                             |git rm --cached                              | リポジトリのみ削除(コミットしたもの)。ファイルは残る。                                                      |
|ファイルの移動　　　　　　　　　   |git mv <旧ファイル名> <新ファイル名>         | ワークツリーの移動+ステージにも追加。　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　 |
|ファイル名変更　　　　　　　　　   |git mv <ファイル名> <移動先>                | ワークツリーの変更+ステージにも追加。　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　 |
|githubを登録                 |git remote add origin <githubのurl>          | originというショートカットでurlのリモートリポジトリを登録する。今後はoriginでリモートリポジトリにアップしたり、取得したりできる。リモートリポジトリは複数登録できて、originとは別の名前のショートカットで登録する。        |
|                             |git remote add <リモート名>                  |リモートリポジトリを新規追加                                                             |
|リモートリポジトリ確認           |git remote                                   |  -vでURL表示。 git remote show originでさらに詳しく表示。                            |
|リモート名変更               |git remote rename <旧リモート> <新リモート>  |                                                                                         |
|リモート名削除               |git remote rm <リモート>                     |                                                                                         |
|リモートリポジトリへ送信     |git push <リモート名><ブランチ名>            | git push origin master                                                                  |
|                             |git push -u origin master                    | -uで次回以降はgit pushでorigin fmasterにpushする                                         |
|コマンドにエイリアス         |git config --global alias st status          | 省略したい単語、コマンドの順番。--globalでpc全体の設定になる。                          |
|addを取り消す                |git reset HEAD <ファイル名>                  | HEADは自分が作業しているブランチ名。                                                             |
|                             |git reset HEAD <ディレクトリ名>              |                                                                                         |
|                             |git reset HEAD .                             | addしたものすべて取り消す                                                               |
|ファイルの変更を取り消す     |git checkout -- <ファイル名>                 | "--"はブランチ名とファイル名が被ったときに、どちらを指してるか明確にするためにつける    |
|                             |git checkout -- <ディレクトリ名>             |                                                                                         |
|                             |git checkout -- .                            |                                                                                         |
|直前のコミットをやり直す     |git commit --amend                           | 実行するとエディタが表示される。中身もかえるなら、ファイルを直してaddした後に実行する。 |
|情報を取得す                 |git fetch <リモート名>                       |  git fetch origin                                                                       |
|ブランチを作成               |git branch <ブランチ名>                      |  ブランチを作成するだけで、切り替わらない。                                                            |
|ブランチ一覧                 |git branch                                   | git branch -a すべてのブランチを表示                                                         |
|ブランチを切り替える         |git checkout <既存ブランチ名>                  |                                                                                         |
|                             |git checkout -b <新ブランチ名>                 | ブランチを新規作成して切り替える                                                        |
|ブランチ名を変更             |git branch -m <新ブランチ名>                   |  現在いるブランチ名を変更                                                                      |
|ブランチ削除                 |git branch -d <ブランチ名>                   |                                                                                         |
|変更履歴をマージする         |git merge <ブランチ名>                       | コンフリクトが起きた場合は、git statusで確認                                                   |
|                             |git merge <リモート名/ブランチ名>            | git merge origin master                                                              |
|
|リモートから取得する (fetch)    |git fetch <リモート名>                       | リモートリポジトリからローカルリポジトリに取得。ワークツリーには反映されない。反映するには、git merge origin/masterをする。  |
|プルのマージ型               |git pull <リモート名> <ブランチ名>           | git pull origin master  リモートリポジトリからローカルリポジトリに取得して、ワークツリーにも反映する。|
|プルのリベース型             |git pull --rebase <リモート名> <ブランチ名>  | git pull --rebase origin master master                                                  |
|タグ作成(軽量版タグ)         |git tag [タグ名]                             |                                                                                         |
|タグを作成(注釈付きタグ)     |git tag -a [タグ名] -m "[メッセージ]"        |                                                                                         |
|                             |git push [リモート名] [タグ名]               | タグをリモートリポジトリに送信する                                                      |
|作業を一次非難する           |git stash save                               | saveは省略可                                                                            |
|一時避難                     |git stash list                               | 非難した作業を確認する                                                                  |
|                             |git stash apply                              | 最新の作業を復元する                                                                    |
|                             |git stash apply --index                      | ステージの状況も復元する                                                                |


# gitignore書き方   
* 指定したファイルを除外  
  * index.html  
* ルートディレクトリを指定  
  * /root.html  
* ディレクトリ以下を除外  
  * dir/  
* /以下の文字列にマッチ「＊」  
  * /\*/\*.css  


# プルリクエストの流れ  
* 変更をGitHubへプッシュ(自分が開発していたブランチで)したら、GitHubでプルリクエストを作る。  
* 作成したら、チームメンバーにコードレビューをお願いする。  
* レビューが通ったら、GitHubでマージボタンを押す。  
* マージをしたら、それまで開発していたブランチを削除する。  

# リベース  
* git branch rebase <ブランチ名>  
* リベースで履歴を整えた形で変更を統合する (他のブランチのコミット履歴を自分に取り込めることが出来る。)(マージとリベースの違いは履歴が一直線なのか、枝分かれしてるかの違い。)




