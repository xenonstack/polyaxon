from django.apps import AppConfig


class PipelinesConfig(AppConfig):
    name = 'pipelines'
    verbose_name = 'Pipelines'

    def ready(self):
        from pipelines.signals import (  # noqa
            new_pipeline_run,
            new_operation_run,
            new_pipeline_run_status,
            new_operation_run_status,
            operation_run_deleted
        )
