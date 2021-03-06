# -*- coding: utf-8 -*-
import datetime
import os
import sys
from pathlib import Path

import git
import better_apidoc
import sphinx_rtd_theme

import cypack

DOCS_SOURCES = Path(__file__).parent
ROOT = DOCS_SOURCES / '..' / '..'  # project root

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('_extensions'))

# -- Generate API documentation -----------------------------------------------


def run_apidoc(app):
    """Generate API documentation."""

    better_apidoc.APP = app
    better_apidoc.main(
        [
            'better-apidoc',
            '-t',
            str(DOCS_SOURCES / '_templates'),
            '--force',
            '--no-toc',
            '--separate',
            '-o',
            str(DOCS_SOURCES / 'API'),
            os.path.join(ROOT / 'src' / 'cypack'),
        ]
    )


# -- General configuration ----------------------------------------------------

# Report broken links as warnings
nitpicky = True
nitpick_ignore = [('py:class', 'callable')]

extensions = [
    'doctr_versions_menu',
    'graphviz_ext',
    'inheritance_diagram',
    'recommonmark',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
]


if os.getenv('SPELLCHECK'):
    extensions.append('sphinxcontrib.spelling')
    spelling_show_suggestions = True
    spelling_lang = os.getenv('SPELLCHECK')
    spelling_word_list_filename = 'spelling_wordlist.txt'
    spelling_ignore_pypi_package_names = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.8', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'
project = 'Cython Package Example'
year = str(datetime.datetime.now().year)
author = 'Michael Goerz'
copyright = '{0}, {1}'.format(year, author)
version = cypack.__version__
release = version
git_tag = "v%s" % version
if version.endswith('dev'):
    try:
        last_commit = str(git.Repo(ROOT).head.commit)[:7]
        release = "%s (%s)" % (version, last_commit)
        git_tag = str(git.Repo(ROOT).head.commit)
    except git.exc.InvalidGitRepositoryError:
        git_tag = "master"
numfig = True

pygments_style = 'friendly'
extlinks = {
    'issue': (
        'https://github.com/goerz-testing/cython-package-example/issues/%s',
        '#',
    ),
    'pr': (
        'https://github.com/goerz-testing/cython-package-example/pull/%s',
        'PR #',
    ),
}

# autodoc settings
autoclass_content = 'class'
autodoc_member_order = 'bysource'
autodoc_mock_imports = []  # e.g.: 'numpy', 'scipy', ...


html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {'**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html']}
html_short_title = '%s-%s' % (project, version)


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True


# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'collapse_navigation': True,
    'display_version': True,
}

inheritance_graph_attrs = dict(size='""')
graphviz_output_format = 'svg'

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

doctr_versions_menu_conf = {
    'menu_title': 'Docs'
}

# -----------------------------------------------------------------------------


def setup(app):
    """Set up Sphinx hooks."""
    app.connect('builder-inited', run_apidoc)
