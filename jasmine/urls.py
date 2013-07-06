import os

from django.conf import settings
from django.conf.urls import patterns, url
from jasmine_core import Core

from jasmine import Config
from .views import JasmineRunner


def _config_file():
    default_location = os.path.join(settings.PROJECT_PATH, 'spec/javascripts/support/jasmine.yml')

    return settings.JASMINE_YAML if hasattr(settings, 'JASMINE_YAML') else default_location

config = Config(_config_file(), project_path=settings.PROJECT_PATH)

urlpatterns = patterns(
    '',
    url(r'^__spec__/(?P<path>.*)$', 'django.views.static.serve', {'document_root': config.spec_dir(), }, name='jasmine_specs'),
    url(r'^__src__/(?P<path>.*)$', 'django.views.static.serve', {'document_root': config.src_dir(), }, name='jasmine_src'),
    url(r'^__boot__/(?P<path>.*)$', 'django.views.static.serve', {'document_root': Core.boot_dir(), }, name='jasmine_boot'),
    url(r'^__jasmine__/(?P<path>.*)$', 'django.views.static.serve', {'document_root': Core.path(), }, name='jasmine_core'),
    url(r'^(?P<path>.ico)$', 'django.views.static.serve', {'document_root': Core.favicon_path()[:-19]},),
    url(r'^$', JasmineRunner.as_view(template_name="runner.html", config=config)),

)
