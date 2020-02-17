'''
MagAO-X Custom Sphinx Bits
'''
import os.path
import re
from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes

def static_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Link to a file under ``_static`` (or the first entry in
    conf.py ``html_static_path``, if different)

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    app = inliner.document.settings.env.app
    try:
        static_folder = os.path.join(app.confdir, app.config.html_static_path[0])
    except AttributeError as err:
        static_folder = os.path.join(app.confdir, '_static')

    # example: text = "foo bar baz <ref/foo/bar/baz.txt>"
    #          link_path = "ref/foo/bar/baz.txt"
    #          link_text = "foo bar baz"
    link_parts = re.match(r'([^<]+) ?(?:<(.+)>)?', text).groups()
    link_path = link_parts[1] if link_parts[1] is not None else link_parts[0]
    link_text = link_parts[0]
    current_src_dir = os.path.dirname(inliner.document.current_source)
    relpath_to_static = os.path.relpath(static_folder, current_src_dir)
    ref = os.path.join(relpath_to_static, link_path)

    node = nodes.reference(rawtext, link_text, refuri=ref, **options)
    return [node], []

def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """
    app.add_role('static', static_role)
    return
