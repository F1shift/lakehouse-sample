# 本スタックの目的

コスト抑えるために、Sagemaker unified studioのプロジェクトのNATを削除し、必要の場合terraformで再構築する。

※`aws_route_table.private_subnet_route_table`は`terraform import`コマンドでプライベートサブネット用のルーティングテーブルをインポートする。