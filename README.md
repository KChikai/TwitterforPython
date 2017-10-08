# Twitter for Python

Twitter API を使って，データクロールするサンプル．
使用言語はPython

事前に，自分で`local_info.py`をクローラと同じディレクトリに置く．
内容は以下のように，自身のアプリケーションのAPIの内容を記述する．
```python
API_key = 'your api key'
API_secret = 'your api secret'
```

<br>

## screen_name から REST API を用いたツイートの収集 


`tweet_crawler.py`を用いてクロールする．
手順は以下の通り．

1. `main`関数内に`screen_name`があるので，
そこで欲しいユーザのスクリーンネームを記述．
2. `python tweet_crawler.py`でクロール
3. `data`ディレクトリ内に指定したスクリーンネームのフォルダが生成され，
その中にクロールしたテキストファイルが生成される．

**appendix:**

生成されたテキストは200件毎のツイートを取得している．
被っているツイートは二つ以上は取得しない (botの登録ツイートなど) ．
デフォルトは200×10回分取得するようになっているが，10回以上が必要な場合
`main`関数の`for`文の回数を適宜変える．

<br>


## Stream API を用いて検索単語を含んだ会話文を収集

`stream_crawler.py`を用いて，クロールする．
手順は以下の通り．

1. `main`関数内の`dir_name`（保存先）と
`filter_words`（検索したい単語，カンマは論理和で，半角スペースは論理積）を指定
2. `python stream_crawler.py`で実行．
3. ディレクトリ内にテキストファイルが取れる．


<br>


## Learning on FastText

おまけ．
取得データから，ネガポジ判定を行う．

1. `screen_name`を指定して，クロールする．

```
    python tweet_crawler.py
```

2. 'cat'等でデータをまとめる and 形態素解析 and タグをつける．
`negaposi_label.txt`が学習データ．`negaposi`が出力ファイル（拡張子は`bin`で出力される）．

```
    python learing.py data/negaposi_label.txt negaposi

```

3.`predict.py`に日本語文を引数として渡すと，評価ラベルが返される（MeCabが必要）．