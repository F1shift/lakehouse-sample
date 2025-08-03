# AWS SAM CLI + Terraformのローカルデバッグ手順

## 前提条件

1. SAMがstateを参照できるように、`terraform apply`を実施して、Lambda関数が構築済みであるのこと。（Lambdaのコードは未完成のものでも構わない）

2. Lambdaのpythonでptvsdのリモートデバッグを有効にしていること。※環境にデプロイする時は無効にすること。

```python
import ptvsd

ptvsd.enable_attach(address=('0.0.0.0', 9999), redirect_output=True)
ptvsd.wait_for_attach()
```



## デバッグのステップ

1. pipパッケージのインストール(初回もしくはrequirements.txt変更がある場合のみ実施)

```bash
cd dummy_data_source/demo_external_system/data_injection/lambda/dummy_data_injector/src
pip install -r requirements.txt -t .
```

2. Lambdaが含まれているTerraformディレクトリに移動

```bash
cd infra/aws-terraform/envs/dev/01_stack01
```

3. Lambdaのzipを更新

以下コマンドを実行してLambdaコードアップロード用のzipファイルを更新する。

zipファイルの更新はコード変更があるたびに実施する必要がある。また、terraform介さずにzipコマンドなどで自分で更新しても構わない。


```bash
terraform plan
```


4. LambdaのTerraform stateを確認

以下コマンドで該当Lambdaのstateのキーを確認する。（Lambdaのstateキーが変わっていなければ毎回調べる直す必要はありません。）

```bash
terraform state list | grep lambda
```

例：

```bash
terraform state list | grep lambda
module.stack01.aws_iam_role.lambda_role
module.stack01.aws_lambda_function.lambda_dummy_data_generator # <- これが該当 
```

5. SAM CLIでローカルでLambdaを実行

```bash
sam local invoke <Lambdaのstate名> --debug-port <ptvsdのデバッグポート>
``` 

例：
```bash
sam local invoke module.stack01.aws_lambda_function.lambda_dummy_data_generator --debug-port 9999
```

6. VSCodeのdebuggerで接続

`launch.json`の例：

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach to SAM CLI",
            "type": "python",
            "request": "attach",
            "address": "localhost",
            "port": 9999,
            "localRoot": "${workspaceRoot}/dummy_data_source/demo_external_system/data_injection/lambda/dummy_data_injector/src",
            "remoteRoot": "/var/task",
            "protocol": "inspector",
            "stopOnEntry": false
        }
    ]
}
```

上記`launch.json`の場合、`run and debug`メニューで`Attach to SAM CLI`を選択して実行。