#!/usr/bin/python
import re
from config import config
import markdown,codecs,jinja2
import os


def separate_front_matter(s):
    """ Separate the yaml in front from the rest of the text

        Args:
          s - a string represeting the whole source document
        Returns:
          (yaml,cotent)
    """
    state="before_yaml"
    yaml_dict={}
    doc=""
    for line in s.split("\n"):
        if line=="---" and state=="before_yaml":
            state="in_yaml"
        elif line=="---" and state=="in_yaml":
            state="after_yaml"
        elif state=="in_yaml":
            (a,b) = re.split(": ?",line)
            yaml_dict[a]=b
        else:
            doc=doc+line+"\n"
    return (yaml_dict,doc)

def markdown_source(s,dict=None):
    """
    just sends the source through markdown for now
    """
    r = markdown.markdown(s,['sane_lists'])
    return r

def htmlize_source(s,dict={}):
    """
    plugs the source html into a dummy jinja template (defined below)
    then does the substitution.
    Most of the work is to get the dummy template to
    extend from the parent specified in the dict (yaml)
    """

    dict['content']=s
    tsource="""
    {%% extends "%(layout)s" %%}
        {%% block %(block)s %%}
    %(content)s
    {%% endblock %%}
    """

    dir = config['base_dir']+"/"+config['templates']
    loader = jinja2.FileSystemLoader([dir])
    env = jinja2.Environment(loader=loader)
    
    t=env.from_string(tsource%dict)

    return t.render(dict)
    #t2 = env.join_path(t,dict['layout'])
    #   return t.render(dict)



def process_file(fname):
    """ Converts file to html by
        1. Reading the file
        2. pulling off yaml front matter
        3. running through processors like markdown etc
        4. using jinja to convert the html (using the
           augmented yaml frontmatter as the substitution dict
        Args:
          fname : full path to a file
        Returns:
          the content of the file converted to html
    """

    (root,ext)=os.path.splitext(fname)
    ext=ext[1:]

    #rawfile = unicode(open(fname).read(),'UTF-8')
    input_file = codecs.open(fname, mode="r", encoding="utf-8")
    rawfile = input_file.read()
    (yaml,source)=separate_front_matter(rawfile)

    # do any preprocessing
    if config['extensions'].has_key(ext) and config['extensions'][ext]!='html':
        source = processors[config['extensions'][ext]](source)

    # and then use jinja to deal with the templates
    result = htmlize_source(source,yaml)

    return result



processors={'markdown':markdown_source,
           'html':htmlize_source}


if __name__=="__main__":
    print process_file("demosite/content/index.html")
    print "\n--------------------\n"
    print process_file("demosite/content/one.md")
