# -*- coding: utf-8 -*-

import pkg_resources
import sphinx_rtd_theme

from sphinx.domains.python import PythonDomain

needs_sphinx = '1.6'

# The 'girder' package must be installed
_girder_package = pkg_resources.get_distribution('girder')
_girder_client_package = pkg_resources.get_distribution('girder_client')
_girder_requirements = {
    _requirement.project_name.lower()
    for _package in [_girder_package, _girder_client_package]
    for _requirement in _package.requires(_package.extras)
}
# Add importable module names that are different from package names
_girder_requirements |= {
    'botocore',
    'bson',
    'dateutil',
    'requests_toolbelt',
    'yaml'
}

master_doc = 'index'

project = u'Girder'
copyright = u'2014-2018, Kitware, Inc.'
release = _girder_package.version
version = '.'.join(release.split('.')[:2])

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_favicon = 'favicon.ico'

latex_documents = [
    ('index', 'Girder.tex', u'Girder Documentation', u'Kitware, Inc.', 'manual'),
]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode'
]

autodoc_mock_imports = list(_girder_requirements)

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pymongo': ('https://api.mongodb.com/python/current/', None)
}


# Override the resolution of some targets
class PatchedPythonDomain(PythonDomain):
    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        # References to "list" may ambiguously resolve to several Girder methods named "list",
        # instead of just the built-in Python 'list' (due to the mechanism described at
        # http://www.sphinx-doc.org/en/stable/domains.html#role-py:obj ). This results in incorrect
        # xrefs and causes Sphinx to emit warnings. So, rather than require all references to
        # explicitly name ":py:obj:`list`", override this method to do the right thing.
        if target == 'list':
            # References to built-in symbols natively return None
            return None
        return super(PatchedPythonDomain, self).resolve_xref(
            env, fromdocname, builder, typ, target, node, contnode)


def setup(sphinx):
    sphinx.override_domain(PatchedPythonDomain)
