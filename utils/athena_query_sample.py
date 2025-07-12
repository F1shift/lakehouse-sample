
import boto3
import time

# --- 設定 ---
DATABASE_NAME = "lakehouse_sample_glue_db"
TABLE_NAME = "traffic_data_2"
# Athenaのクエリ結果が出力されるS3パスを必ず指定してください
QUERY_OUTPUT_LOCATION = "s3://lakehouse-sample-s3-bucket/athena_results/" 
REGION_NAME = "ap-northeast-1" # ご自身のリージョンに合わせて変更してください

# --- クエリ ---
# テーブル名はバッククォート(`)ではなく、ダブルクォーテーション(")で囲む必要があります
QUERY = f'SELECT * FROM "{DATABASE_NAME}"."{TABLE_NAME}" LIMIT 10;'

def run_athena_query():
    """
    Athenaにクエリを実行し、結果を取得して表示する
    """
    client = boto3.client("athena", region_name=REGION_NAME)

    # 1. クエリの実行を開始
    try:
        response = client.start_query_execution(
            QueryString=QUERY,
            QueryExecutionContext={"Database": DATABASE_NAME},
            ResultConfiguration={
                "OutputLocation": QUERY_OUTPUT_LOCATION,
            },
        )
        query_execution_id = response["QueryExecutionId"]
        print(f"クエリを開始しました。実行ID: {query_execution_id}")

    except Exception as e:
        print(f"クエリの開始に失敗しました: {e}")
        return

    # 2. クエリの完了を待つ
    while True:
        try:
            query_status = client.get_query_execution(
                QueryExecutionId=query_execution_id
            )
            state = query_status["QueryExecution"]["Status"]["State"]

            if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
                if state == "SUCCEEDED":
                    print("クエリが成功しました。")
                else:
                    error_message = query_status["QueryExecution"]["Status"].get("StateChangeReason")
                    print(f"クエリが {state} しました。理由: {error_message}")
                break
            
            print("クエリ実行中...")
            time.sleep(5) # 5秒待機

        except Exception as e:
            print(f"クエリ状態の取得に失敗しました: {e}")
            return
            
    # 3. クエリが成功した場合、結果を取得して表示
    if state == "SUCCEEDED":
        try:
            result_response = client.get_query_results(QueryExecutionId=query_execution_id)
            
            # ヘッダーの表示
            columns = [col['Label'] for col in result_response['ResultSet']['ResultSetMetadata']['ColumnInfo']]
            print("--- クエリ結果 ---")
            print(", ".join(columns))

            # 結果の表示 (ヘッダー行を除く)
            for row in result_response["ResultSet"]["Rows"][1:]:
                print(", ".join([item.get('VarCharValue', 'NULL') for item in row['Data']]))

        except Exception as e:
            print(f"結果の取得に失敗しました: {e}")


if __name__ == "__main__":
    run_athena_query()
