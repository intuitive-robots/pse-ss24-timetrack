# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'IntuitiveTimeTracking'
copyright = '2024, IntuitiveTimeTracking'
authors = [
    'Dominik Pollok',
    'Phil Gengenbach',
    'Alina Petri',
    'José Ayala',
    'Johann Kohl'
]
author = '\n'.join(authors)
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.viewcode", "sphinx.ext.autodoc",
              "sphinx.ext.napoleon", 'sphinx.ext.intersphinx']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'flask': ('https://flask.palletsprojects.com/en/latest/', None)
}

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'show-inheritance': True,
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
