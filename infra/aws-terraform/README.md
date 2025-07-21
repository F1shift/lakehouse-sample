# 注意事項

## 1. 必要な事前手動構築
2025/07/21時点にTerraformがまだまず、SageMaker Unified Studioにサポートしていないため、
まず、SageMaker Unified Studioドメインの構築は手動になります。

Terraform構築を開始する前に、まずマネージメントコンソールで「SageMaker」を検索し、SageMaker Unified Studioドメイン、プロジェクトを手動で構築する必要があります。作成したドメインの情報を`locals-<env>.tf`の`sagemaker_unified_studio`変数を書き換えてください。


※ 「SageMaker」のSageMaker Unified Studioドメインと「SageMaker AI」のドメインは違うものとなるため、間違わないように注意してください。  
「SageMaker」のSageMaker Unified Studioは次世代のSageMakerであり、「SageMaker AI」のSageMaker Studioよりも新しいサービスになります。

### 必要なLakeformation権限

Lakeformationから以下権限をTerraform実行ロールに付与する必要があります。

- SageMaker Unified StudioのGlueデータベースに対しての「Create Table」権限