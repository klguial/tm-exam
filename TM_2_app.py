import streamlit as st
from shared.bigquery_service import BigQueryClient

bq_client = BigQueryClient()

project_name = "tm-exam-project-427209"
dataset_name = "tm_data"
table_name = "dailycheckins"
table_id = f"{project_name}.{dataset_name}.{table_name}"
users_list = bq_client.get_all_users(table_id)


st.header("TM Daily Checkins")
user_select = st.selectbox(
    "Select a user",
    users_list
)
print(user_select)
checkins_df = bq_client.get_checkins_per_user(table_id, user_select)
st.table(checkins_df)
