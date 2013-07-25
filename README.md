lesstatic
==========

A simple Python based Static Site generator

### Config options
 extensions={'md':'markdown,'html':html}
 post_dirs=['posts']
 content_dirs=['content']
 templates_dir='tempalates' # note - only one of these

### Optional Markdown in content files:

If blog_dir is present, treat page as a blog. You can optionally specify 
the other keywords as well

 * blog_dir : DIR // directory to find posts for this page
 * paginate : n // use the paginator? If so, how many posts per page
 * blurb : True/False // use blurb (rather than full post)

Any unspecified definition in the YAML topmatter is sent to the page
as a key/value pair in the dictionary that goes to the template.
