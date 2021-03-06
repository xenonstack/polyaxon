from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from experiment_groups import views
from experiments import views as experiments_views
from libs.urls import NAME_PATTERN, SEQUENCE_PATTERN, USERNAME_PATTERN

groups_urlpatterns = [
    re_path(r'^{}/{}/groups/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
            views.ExperimentGroupDetailView.as_view()),
    re_path(
        r'^{}/{}/groups/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        experiments_views.GroupExperimentListView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(groups_urlpatterns)
