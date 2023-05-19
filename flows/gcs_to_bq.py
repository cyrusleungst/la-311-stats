from prefect_gcp.bigquery import bigquery_load_cloud_storage
from prefect import flow, task
from prefect_gcp import GcpCredentials

@flow(name="Divvy trips GCS to BQ")
def gcs_to_bq():
    gcp_credentials_block = GcpCredentials.load("divvy-trips-creds")

    result = bigquery_load_cloud_storage(
        dataset="raw",
        table="la_311_historical",
        uri="gs://la_311/*.parquet",
        location="europe-west2",
        gcp_credentials=gcp_credentials_block,
        job_config={
            "source_format": 'PARQUET'
        }
    )

    return result

if __name__ == "__main__":
    gcs_to_bq()
