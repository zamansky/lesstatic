import process_source as ps

processors={'markdown':ps.markdown_source,
           'html':ps.htmlize_source}

extensions={'md':'markdown'}

templates="templates"
static="static"
static_dest="static"
content = 'content'

site = 'site'
