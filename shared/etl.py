import pandas as pd
from dateutil import parser
import re
import uuid
import itertools
import numpy as np


month_mappings = {
       'января': 'Jan',
       'февраля': 'Feb',
       'марта': 'Mar',
       'апреля': 'Apr',
       'мая': 'May',
       'июня': 'Jun',
       'июля': 'Jul',
       'августа': 'Aug',
       'сентября': 'Sep',
       'октября': 'Oct',
       'ноября': 'Nov',
       'декабря': 'Dec',
}

month_regex = re.compile('|'.join(month_mappings.keys()))


def replace_month_names(date_str):
    def replace_match(match):
        return month_mappings[match.group(0).lower()]
    return month_regex.sub(replace_match, date_str)

def parse_date(date_str):
    try:
        date_str = replace_month_names(date_str)
        return parser.parse(date_str).replace(tzinfo=None)
    except Exception as error:
        return pd.NaT

def read_data_file(file_path):
    return pd.read_csv(file_path)

def clean_dailycheckin_dataset(file_path):
    df = read_data_file(file_path)
    cond = df['user'].isna()
    df.loc[cond, 'user'] = 'unknown'
    df['timestamp'] = df['timestamp'].apply(parse_date)
    df['id'] = df.index.map(lambda _: uuid.uuid4().__str__())
    return df
