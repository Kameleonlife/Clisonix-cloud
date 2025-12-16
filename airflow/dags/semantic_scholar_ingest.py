from datetime import datetime
import os
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from weaviate import Client as WeaviateClient

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
DEFAULT_QUERY = os.getenv("S2_QUERY", "EEG neuroacoustics")
FIELDS = "title,abstract,year,authors"


def load_batch():
    client = WeaviateClient(WEAVIATE_URL)
    response = requests.get(
        SEMANTIC_SCHOLAR_API,
        params={"query": DEFAULT_QUERY, "fields": FIELDS, "limit": 100},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json().get("data", [])

    if not data:
        client.close()
        return

    with client.batch as batch:
        batch.batch_size = 50
        for paper in data:
            batch.add_data_object(
                {
                    "title": paper.get("title"),
                    "abstract": paper.get("abstract", ""),
                    "published": f"{paper.get('year', 2020)}-01-01",
                    "authors": [author.get("name") for author in paper.get("authors", [])],
                    "source": "semantic_scholar",
                },
                class_name="Paper",
            )
    client.close()


with DAG(
    dag_id="semantic_scholar_ingest",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@weekly",
    catchup=False,
) as dag:
    PythonOperator(task_id="load_batch", python_callable=load_batch)

