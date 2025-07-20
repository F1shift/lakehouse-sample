# やってほしいこと
「../01_create_data/output/all_sample_data.csv」からデータを読み込んで、
データを整形した上でタイムスタンプで分単位にファイルを分けるPythonスクリプトを作成してください。
出力ディレクトリはsplit_data.pyと同じ階層のoutputディレクトリにしてください。

## 入力形式
「../01_create_data/README.md」を参照してください。

## 出力形式
- ファイル形式: CSV
- ファイル名: sample_data_yyyy-mm-ddTHH_MM.csv
- カラム:
  
| カラム    | カラム(和名)           | 型       | 説明                                            |
| --------- | ---------------------- | -------- | ----------------------------------------------- |
| id        | 識別ID                 | str      | uuid4の文字列                                   |
| timestamp | イベントが発生した時刻 | datetime | yyyy-mm-ddTHH:MM:SSZ+0900                       |
| direction | 方向                   | int      | 境界線の内側に入り：1<br>境界線の外側に出る：-1 |
| age       | 年齢                   | int      | 0~                                              |
| gender    | 性別                   | str      | male、female                                    |