from shared.bigquery_service import BigQueryClient
import shared.etl as etl


def main():

    data_path = './data/dailycheckins.csv'
    schema_path = './schema/dailycheckins_schema.json'
    project_name = "tm-exam-project-427209"
    dataset_name = "tm_data"
    table_name = "dailycheckins"
    table_id = f"{project_name}.{dataset_name}.{table_name}"

    try:
        bq_client = BigQueryClient()
        bq_client.create_table_from_schema(table_id, schema_path)
        df = etl.clean_dailycheckin_dataset(data_path)
        bq_client.load_data(df, table_id, schema_path)
    except Exception as error:
        raise Exception(error)



if __name__ == '__main__':
    main()
