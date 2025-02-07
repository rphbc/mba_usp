from dagster import Definitions, load_assets_from_modules
from .jobs import rabbitmq_pipeline, my_job
import dagster as dg

from mba_usp_dagster_project import assets  # noqa: TID252

all_assets = load_assets_from_modules([assets])

@dg.schedule(cron_schedule="* * * * *", job=my_job)
def trigger_dagster_run(_context):
    return dg.RunRequest()


defs = Definitions(
    assets=all_assets,
    jobs=[rabbitmq_pipeline],
    schedules=[trigger_dagster_run],
)
