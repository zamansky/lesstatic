import process_source as ps

processors={'markdown':ps.markdown_source,
           'html':ps.htmlize_source}

extensions={'md':'markdown'}

template_dir="templates"

content_dir = 'content'

site_dir = 'site'
