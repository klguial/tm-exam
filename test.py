from shared.bigquery_service import BigQueryClient

bq_client = BigQueryClient()

project_name = "tm-exam-project-427209"
dataset_name = "tm_data"
table_name = "dailycheckins"
table_id = f"{project_name}.{dataset_name}.{table_name}"
checkins_df = bq_client.get_checkins_per_user(table_id, 'arya')
