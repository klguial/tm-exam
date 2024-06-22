from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
import pandas as pd

class BigQueryClient:

    def __init__(self, key_path=''):

        self.key_path = key_path
        self.client = None
        self.credentials = None
        self.setup()


    def setup(self):
        try:
            self.credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"]
            )
            # self.credentials = service_account.Credentials.from_service_account_file(
            #     self.key_path,
            #     scopes = ["https://www.googleapis.com/auth/bigquery"]
            # )

            self.client = bigquery.Client(
                credentials=self.credentials,
                project=self.credentials.project_id
            )

        except Exception as error:
            raise(Exception(error))


    def run_query(self, query):
        query_job = self.client.query(query)
        return query_job.result()


    def load_checkins_data(self, dataframe, table_id):
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("id", bigquery.enums.SqlTypeNames.STRING, mode="REQUIRED"),
                bigquery.SchemaField("user", bigquery.enums.SqlTypeNames.STRING, mode="REQUIRED"),
                bigquery.SchemaField("timestamp", bigquery.enums.SqlTypeNames.TIMESTAMP, mode="REQUIRED"),
                bigquery.SchemaField("hours", bigquery.enums.SqlTypeNames.FLOAT64, mode="REQUIRED"),
                bigquery.SchemaField("project", bigquery.enums.SqlTypeNames.STRING, mode="REQUIRED")
            ],
        )
        job = self.client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)
        job.result()

        table = self.client.get_table(table_id)
        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), table_id
            )
        )


    def create_checkins_table(self, table_id):
        query = """
        CREATE OR REPLACE TABLE `{}` (
            id STRING NOT NULL,
            user STRING NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            hours FLOAT64 NOT NULL,
            project STRING NOT NULL,
            
            PRIMARY KEY (id) NOT ENFORCED
        );
        """.format(table_id)
        result = self.run_query(query)
        

    def get_all_users(self, table_id):
        try:
            sql = """SELECT DISTINCT user FROM `{}` ORDER BY user;""".format(table_id)
            rows = self.run_query(sql)
            return [row[0] for row in rows]
        except Exception as error:
            print('Failed to get users.')


    def get_checkins_per_user(self, table_id, user):
        sql = f"""
        SELECT user,timestamp,hours,project
        FROM `{table_id}`
        WHERE user='{user}'
        ORDER BY timestamp desc
        ;
        """
        query_job = self.client.query(sql)
        rows = query_job.result()
        df = pd.DataFrame([dict(row.items()) for row in rows])
        return df
