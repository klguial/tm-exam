from shared.bigquery_service import BigQueryClient
import shared.etl as etl


def main():

    data_file_path = './data/dailycheckins.csv'
    project_name = "tm-exam-project-427209"
    dataset_name = "tm_data"
    table_name = "dailycheckins"
    table_id = f"{project_name}.{dataset_name}.{table_name}"
    
    bq_client = BigQueryClient()
    print('Create or Replace table...')
    bq_client.create_checkins_table(table_id)
    print('Cleaning data...')
    df = etl.clean_dailycheckin_dataset(data_file_path)
    print('Loading data to BigQuery...')
    result = bq_client.load_checkins_data(df, table_id)





if __name__ == '__main__':
    main()
