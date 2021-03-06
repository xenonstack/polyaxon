from django.contrib import admin

from experiment_groups.models import (
    ExperimentGroup,
    ExperimentGroupIteration,
    ExperimentGroupStatus
)
from libs.admin import DiffModelAdmin


class ExperimentGroupAdmin(DiffModelAdmin):
    pass


class ExperimentGroupStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ExperimentGroupIterationAdmin(DiffModelAdmin):
    pass


admin.site.register(ExperimentGroup, ExperimentGroupAdmin)
admin.site.register(ExperimentGroupStatus, ExperimentGroupStatusAdmin)
admin.site.register(ExperimentGroupIteration, ExperimentGroupIterationAdmin)
