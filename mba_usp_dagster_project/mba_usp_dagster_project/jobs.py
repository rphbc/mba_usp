from dagster import job, define_asset_job
from mba_usp_dagster_project.assets import rabbitmq_listener

@job
def rabbitmq_pipeline():
    """Pipeline do Dagster que escuta a fila e processa mensagens"""
    rabbitmq_listener()

my_job = define_asset_job("my_job", [rabbitmq_listener])