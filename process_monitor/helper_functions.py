import json
import os
from datetime import datetime

import pandas as pd
from tabulate import tabulate


def create_data_csv_files(csv_data, output_csv_file):
    df = pd.DataFrame(csv_data)

    if os.path.isfile(output_csv_file):
        existing_df = pd.read_csv(output_csv_file)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        combined_df = df

    combined_df.to_csv(output_csv_file, index=False)


def get_current_time():
    return datetime.now()


def print_processes_data_as_a_table(table_data, headers=None):
    if isinstance(table_data[0], dict):
        headers = headers or "keys"
    else:
        headers = headers or []

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def load_config(json_file_path):
    with open(json_file_path, 'r') as f:
        return json.load(f)
