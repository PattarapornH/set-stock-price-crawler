from http import client
from google.cloud import bigquery
from config import GCP_PROJECT, BQ_DATASET


def write_dataframe_to_bq(dataframe, table_name, dataset=BQ_DATASET, job_config=None):
    client = bigquery.Client()
    if job_config is None:
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    table_id = f"{GCP_PROJECT}.{dataset}.{table_name}"

    job = client.load_table_from_dataframe(
        dataframe=dataframe, destination=table_id, job_config=job_config
    )
    job.result()


def query_table(query, job_config=None):
    client = bigquery.Client()
    job = client.query(query=query,job_config=job_config)
    return job.to_dataframe()