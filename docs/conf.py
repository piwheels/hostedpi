import os
import sys
from datetime import datetime
from importlib.metadata import version


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import sphinx_rtd_theme


hostedpi_version = "0.4.1"


# -- General configuration ------------------------------------------------

author = "The piwheels team"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
    "sphinxcontrib.autodoc_pydantic",
]
templates_path = ["_templates"]
source_suffix = ".rst"
# source_encoding = 'utf-8-sig'
master_doc = "index"
copyright = "2020-%s %s" % (datetime.now().year, author)
project = "hostedpi"
version = hostedpi_version
release = version
# language = None
# today_fmt = '%B %d, %Y'
exclude_patterns = ["_build"]
highlight_language = "python3"
# default_role = None
# add_function_parentheses = True
# add_module_names = True
# show_authors = False
pygments_style = "sphinx"
# modindex_common_prefix = []
# keep_warnings = False

# -- Autodoc configuration ------------------------------------------------

autodoc_member_order = "bysource"

# -- Intersphinx configuration --------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.9", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "sphinx_rtd_theme"
# html_theme_options = {}
# html_sidebars = {}
html_title = "%s %s Documentation" % (project, version)
# html_theme_path = []
# html_short_title = None
# html_logo = None
# html_favicon = None
# html_static_path = ["_static"]
# html_extra_path = []
# html_last_updated_fmt = '%b %d, %Y'
# html_use_smartypants = True
# html_additional_pages = {}
# html_domain_indices = True
# html_use_index = True
# html_split_index = False
# html_show_sourcelink = True
# html_show_sphinx = True
# html_show_copyright = True
# html_use_opensearch = ''
# html_file_suffix = None
htmlhelp_basename = "%sdoc" % project

autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_validators = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_field_list_validators = False

nitpicky = True
nitpick_ignore = [
    ("py:class", "pydantic.types.PathType"),
    ("py:class", "file"),
]
