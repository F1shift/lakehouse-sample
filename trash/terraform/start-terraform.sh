# docker-compose.ymlを実行し、terraformコンテナのBashに入る
#!/bin/bash

docker-compose up -d
docker-compose exec terraform bash
