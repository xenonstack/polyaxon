# Generated by Django 2.0.3 on 2018-04-14 07:40

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import libs.models
import libs.spec_validation
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('jobs', '0001_initial'),
        ('experiment_groups', '0001_initial'),
        ('repos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('sequence', models.PositiveSmallIntegerField(editable=False, help_text='The sequence number of this experiment within the project.')),
                ('dockerfile', models.TextField(blank=True, help_text='The dockerfile used to train this experiment.', null=True)),
                ('declarations', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='The parameters used for this experiment.', null=True)),
                ('config', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='The compiled polyaxon with specific values for this experiment.', null=True, validators=[libs.spec_validation.validate_experiment_spec_config])),
                ('code_reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='repos.CodeReference')),
                ('experiment_group', models.ForeignKey(blank=True, help_text='The experiment group that generate this experiment.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to='experiment_groups.ExperimentGroup')),
            ],
            options={
                'ordering': ['sequence'],
            },
            bases=(models.Model, libs.models.LastStatusMixin),
        ),
        migrations.CreateModel(
            name='ExperimentJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('definition', django.contrib.postgres.fields.jsonb.JSONField(help_text='The specific values for this job.')),
                ('role', models.CharField(default='master', max_length=64)),
                ('sequence', models.PositiveSmallIntegerField(editable=False, help_text='The sequence number of this job within the experiment.')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='experiments.Experiment')),
            ],
            options={
                'ordering': ['sequence'],
            },
            bases=(models.Model, libs.models.LastStatusMixin),
        ),
        migrations.CreateModel(
            name='ExperimentJobStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('message', models.CharField(blank=True, max_length=256, null=True)),
                ('status', models.CharField(blank=True, choices=[('Created', 'Created'), ('Building', 'Building'), ('Running', 'Running'), ('Succeeded', 'Succeeded'), ('Failed', 'Failed'), ('Stopped', 'Stopped'), ('UNKNOWN', 'UNKNOWN')], default='Created', max_length=64, null=True)),
                ('details', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='experiments.ExperimentJob')),
            ],
            options={
                'abstract': False,
                'ordering': ['created_at'],
                'verbose_name_plural': 'Experiment Job Statuses',
            },
        ),
        migrations.CreateModel(
            name='ExperimentMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('values', django.contrib.postgres.fields.jsonb.JSONField()),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='experiments.Experiment')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ExperimentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('message', models.CharField(blank=True, max_length=256, null=True)),
                ('status', models.CharField(blank=True, choices=[('Created', 'Created'), ('Resuming', 'Resuming'), ('Building', 'Building'), ('Scheduled', 'Scheduled'), ('Starting', 'Starting'), ('Running', 'Running'), ('Succeeded', 'Succeeded'), ('Failed', 'Failed'),('Stopped', 'Stopped'), ('UNKNOWN', 'UNKNOWN')], default='Created', max_length=64, null=True)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='experiments.Experiment')),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name_plural': 'Experiment Statuses',
            },
        ),
        migrations.AddField(
            model_name='experimentjob',
            name='job_status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='experiments.ExperimentJobStatus'),
        ),
        migrations.AddField(
            model_name='experimentjob',
            name='resources',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='jobs.JobResources'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='experiment_metric',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='experiments.ExperimentMetric'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='experiment_status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='experiments.ExperimentStatus'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='original_experiment',
            field=models.ForeignKey(blank=True, help_text='The original experiment that was cloned from.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clones', to='experiments.Experiment'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='experimentjob',
            unique_together={('experiment', 'sequence')},
        ),
        migrations.AlterUniqueTogether(
            name='experiment',
            unique_together={('project', 'sequence')},
        ),
    ]
