import requests
import zipfile
import os
import io
import yaml
import pandas as pd
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


def create_directory_if_not_exists(folderpath):
    if not os.path.exists(folderpath):
        print(f"{folderpath} does not exist, creating folder...")
        os.mkdir(folderpath)


@task(log_prints=True, name="Downloading and zipping from URL")
def download_and_unzip_from_url(url: str, folderpath: str) -> Path:
    create_directory_if_not_exists(folderpath=folderpath)

    print(f"Downloading file from {url}")
    response = requests.get(url)

    print(f"Unzipping file into {folderpath}")
    zip = zipfile.ZipFile(io.BytesIO(response.content))
    listoffiles = zip.infolist()

    for file in listoffiles[:1]:
        unzip_name = file.filename

    csv_path = Path(f"{folderpath}/{unzip_name}")
    zip.extractall(folderpath)
    
    return csv_path


@task(log_prints=True, name="Fixing dtypes")
def fix_dtypes(filepath: Path, schema: dict) -> pd.DataFrame:
    print("Asserting schema")
    df = pd.read_csv(filepath, engine="pyarrow").astype(schema)

    print(df.dtypes)
    print(df.head(10))

    return df


@task()
def load_schemas() -> dict:
    with open("schema.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


@task(log_prints=True, name="Writing to local")
def write_local(df: pd.DataFrame, folderpath: str, filename: str):
    create_directory_if_not_exists(folderpath=folderpath)
    parquet_path = Path(f"{folderpath}/{filename}")

    print("Writing df to parquet")
    df.to_parquet(path=parquet_path, engine="pyarrow")

    return parquet_path


@task()
def write_gcs(filepath: Path, filename: str) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("divvy-trips-gcs")
    gcs_block.upload_from_path(from_path=filepath, to_path=filename)
    

@flow(name="Monthly data to GCS")
def monthly_data_to_gcs(url: str) -> None:
    schemas = load_schemas()
    csv_folderpath = "../downloads/"
    parquet_folderpath = "../cleaned/"
    parquet_filename = f"{url.split('/')[-1].split('.')[0]}.parquet"

    csv_path = download_and_unzip_from_url(url=url, folderpath=csv_folderpath)
    df = fix_dtypes(filepath=csv_path, schema=schemas["divvy-trip"])
    parquet_path = write_local(df=df, folderpath=parquet_folderpath, filename=parquet_filename)
    write_gcs(filepath=parquet_path, filename=parquet_filename)


@flow(name="Divvy trips data to GCS")
def web_to_gcs() -> None:
    year_months = [year_month for year in range(2021, 2023) for year_month in [f"{year}{month:02d}" for month in range(1, 13)]]

    download_urls = [
        f"https://divvy-tripdata.s3.amazonaws.com/{year_month}-divvy-tripdata.zip" for year_month in year_months
    ]

    for url in download_urls:
        monthly_data_to_gcs(url=url)

  
if __name__ == "__main__":
    web_to_gcs()

