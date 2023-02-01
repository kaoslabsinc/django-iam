# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import django
from django.conf import settings, global_settings

settings.configure(
    SECRET_KEY='1234',
    INSTALLED_APPS=[
        *global_settings.INSTALLED_APPS,
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ]
)
django.setup()

project = 'Django Identity and Access Management'
copyright = '2022, Kaos Labs Inc.'
author = 'Kaos Labs Inc.'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
