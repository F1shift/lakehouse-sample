"""
# やってほしいこと
pythonでall_sample_data.csvを読み込んで以下グラフを作成してください。

## グラフ1
ファイル名: all_sample_data_timestamp.png
図のタイプ：ヒストグラフ
横軸: timestamp。最小値は「yyyy-mm-ddT00:08:00Z+0900」、最大値は「yyyy-mm-ddT21:00:00Z+0900」
縦軸: 時間帯ごとの人数(時間ごとにまとめる)
データシリーズ1: enter_timestamp
データシリーズ2: exit_timestamp

## グラフ2
ファイル名: all_sample_data_age.png
図のタイプ：ヒストグラフ
横軸: age。最小値は「0」、最大値は「100」
縦軸: 年齢別の人数合計(10歳ごとにまとめる)

## グラフ3
ファイル名: all_sample_data_age.png
図のタイプ：ヒストグラフ
横軸: gender。
縦軸: 性別ごとの人数合計

# インストールしているライブラリ
@dummy_data_source/demo_external_system/sample_data/requirements.txt に参照すること。
必要であればpipパッケージをインストールしてrequirements.txtを更新してください
"""