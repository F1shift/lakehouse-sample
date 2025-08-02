# AWS SAM CLI + Terraformのローカルデバッグ手順

## 前提条件

SAMがstateを参照できるように、`terraform apply`を実施して、Lambda関数が構築済みであるのこと。（Lambdaのコードは未完成のものでも構わない）

## デバッグのステップ

1. Lambdaが含まれているTerraformディレクトリに移動

```bash
cd infra/aws-terraform/envs/dev/01_stack01
```

2. LambdaのTerraform stateを確認

以下コマンドで該当Lambdaのstateのキーを確認する

```bash
terraform state list | grep lambda
```

例：

```bash
terraform state list | grep lambda
module.stack01.aws_iam_role.lambda_role
module.stack01.aws_lambda_function.lambda_dummy_data_generator # <- これが該当 
```

3. SAM CLIでローカルでLambdaを実行

```bash
sam local invoke <Lambdaのstate名>
``` 

例：
```bash
sam local invoke module.stack01.aws_lambda_function.lambda_dummy_data_generator
``` 