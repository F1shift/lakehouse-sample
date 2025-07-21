import json
import boto3
import logging
from typing import Dict, Any, List
from botocore.exceptions import ClientError

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirehoseClient:
    """AWS Firehoseにデータを送信するクライアントクラス"""
    
    def __init__(self, stream_name: str, region_name: str = 'ap-northeast-1'):
        """
        FirehoseClientの初期化
        
        Args:
            stream_name (str): Firehoseストリーム名
            region_name (str): AWSリージョン名
        """
        self.stream_name = stream_name
        self.firehose_client = boto3.client('firehose', region_name=region_name)
    
    def put_record(self, data: Dict[str, Any]) -> bool:
        """
        単一のJSONレコードをFirehoseに送信
        
        Args:
            data (Dict[str, Any]): 送信するJSONデータ
            
        Returns:
            bool: 送信成功時True、失敗時False
        """
        try:
            # JSONデータをバイトに変換
            record_data = json.dumps(data).encode('utf-8')
            
            response = self.firehose_client.put_record(
                DeliveryStreamName=self.stream_name,
                Record={'Data': record_data}
            )
            
            logger.info(f"レコード送信成功: RecordId={response['RecordId']}")
            return True
            
        except ClientError as e:
            logger.error(f"レコード送信失敗: {e}")
            return False
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            return False
    
    def put_record_batch(self, data_list: List[Dict[str, Any]]) -> bool:
        """
        複数のJSONレコードをバッチでFirehoseに送信
        
        Args:
            data_list (List[Dict[str, Any]]): 送信するJSONデータのリスト
            
        Returns:
            bool: 送信成功時True、失敗時False
        """
        try:
            # レコードを準備
            records = []
            for data in data_list:
                record_data = json.dumps(data).encode('utf-8')
                records.append({'Data': record_data})
            
            # バッチ送信（最大500レコードまで）
            batch_size = 500
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                
                response = self.firehose_client.put_record_batch(
                    DeliveryStreamName=self.stream_name,
                    Records=batch
                )
                
                # 失敗したレコードがあるかチェック
                if response['FailedPutCount'] > 0:
                    logger.error(f"バッチ送信で{response['FailedPutCount']}件のレコードが失敗")
                    return False
                
                logger.info(f"バッチ送信成功: {len(batch)}件のレコード")
            
            return True
            
        except ClientError as e:
            logger.error(f"バッチ送信失敗: {e}")
            return False
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            return False