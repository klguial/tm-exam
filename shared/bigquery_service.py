from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
import pandas as pd
import json



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
            self.client = bigquery.Client(
                credentials=self.credentials,
                project=self.credentials.project_id
            )

        except Exception as error:
            raise(Exception(error))


    def run_query(self, query):
        query_job = self.client.query(query)
        return query_job.result()


    def create_table_from_schema(self, table_id, schema_path):
        self.client.delete_table(table_id, not_found_ok=True)
        schema = self.client.schema_from_json(schema_path)
        table = bigquery.Table(table_id, schema=schema)
        table = self.client.create_table(table)
        print(f"Created table {table_id}.")


    def load_data(self, dataframe, table_id, schema_path):
        schema = self.client.schema_from_json(schema_path)
        job_config = bigquery.LoadJobConfig(schema=schema)
        job = self.client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)
        job.result()
        table = self.client.get_table(table_id)
        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), table_id
            )
        )


    def get_all_users(self, table_id):
        try:
            sql = """SELECT DISTINCT user FROM `{}` ORDER BY user;""".format(table_id)
            rows = self.run_query(sql)
            return [row[0] for row in rows]
        except Exception as error:
            print('Failed to get list of users.')
            raise Exception(error)


    def get_checkins_per_user(self, table_id, user):
        try:
            sql = f"""
                SELECT user,timestamp,hours,project
                FROM `{table_id}`
                WHERE user='{user}'
                ORDER BY timestamp desc
            ;
            """
            rows = self.run_query(sql)
            df = pd.DataFrame([dict(row.items()) for row in rows])
            df.style.format(precision=2)
            return df
        except Exception as error:
            print(f'Failed to get checkins for user {user}.')
            raise Exception(error)
