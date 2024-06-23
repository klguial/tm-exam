import streamlit as st
from shared.bigquery_service import BigQueryClient

bq_client = BigQueryClient()

project_name = "tm-exam-project-427209"
dataset_name = "tm_data"
table_name = "dailycheckins"
table_id = f"{project_name}.{dataset_name}.{table_name}"


@st.cache_data(show_spinner=False)
def load_users():
    users_list = bq_client.get_all_users(table_id)
    return users_list


@st.cache_data(show_spinner=False)
def load_data(table_id, user):
    dataset = bq_client.get_checkins_per_user(table_id, user)
    return dataset


@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df



st.set_page_config(layout="centered")
st.header("TM Daily Checkins")
users_list = load_users()
top_menu = st.columns(3)

# TOP MENU
dataset = load_data(table_id, users_list[0])
with top_menu[1]:
    sort_field = st.selectbox("Sort By", options=dataset.columns)
with top_menu[2]:
    sort_direction = st.radio(
        "Direction", options=["⬆️", "⬇️"], horizontal=True
    )

with top_menu[0]:
    user_select = st.selectbox(
        "Select a user",
        users_list
    )
    dataset = load_data(table_id, user_select)
    print(f'Selected user {user_select}.')

    if sort_field and sort_direction:
        dataset = dataset.sort_values(
                by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
            )


pagination = st.container()

# BOTTOM MENU
bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Page Size", options=[25, 50])
with bottom_menu[1]:
    total_pages = (
        int(len(dataset) / batch_size) if int(len(dataset) / batch_size) > 0 else 1
    )
    current_page = st.number_input(
        "Page", min_value=1, max_value=total_pages, step=1
    )
with bottom_menu[0]:
    st.markdown(f"Page **{current_page}** of **{total_pages}** ")



pages = split_frame(dataset, batch_size)
pagination.dataframe(data=pages[current_page - 1], use_container_width=True)
