from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from problems.models import UserSolution

from .views import download_protected_file

urlpatterns = patterns('',
    url(_(r'^solutions/(?P<path>.*)$'), download_protected_file,
        dict(path_prefix='solutions/', model_class=UserSolution),
        name='download_solution'),
    url(_(r'^corrected_solutions/(?P<path>.*)$'), download_protected_file,
        dict(path_prefix='corrected_solutions/', model_class=UserSolution),
        name='download_corrected_solution'),
    # Include non-translated versions only since Admin ignores lang prefix
    url(r'^solutions/(?P<path>.*)$', download_protected_file,
        dict(path_prefix='solutions/', model_class=UserSolution),
        name='download_solution'),
    url(r'^corrected_solutions/(?P<path>.*)$', download_protected_file,
        dict(path_prefix='corrected_solutions/', model_class=UserSolution),
        name='download_corrected_solution'),
)
