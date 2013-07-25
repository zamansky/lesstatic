#!/usr/bin/python
import re
import markdown,codecs
import os

processors={'markdown':markdown_source,
           'html':htmlize_source}

extensions={'md':'markdown',
            'html':'html'}



def separate_front_matter(s):
    """ Separate the yams in front from the rest of the text

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

def markdown_source(s):
    print s
    r = markdown.markdown(s,['sane_lists'])
    return r

def htmlize_source(s):
    
    return s

def process_file(fname):
    (root,ext)=os.path.splitext(fname)
    ext=ext[1:]

    #rawfile = unicode(open(fname).read(),'UTF-8')
    input_file = codecs.open(fname, mode="r", encoding="utf-8")
    rawfile = input_file.read()
    (yaml,source)=separate_front_matter(rawfile)
    # do any preprocessing
    result = ""
    if extensions.has_key(ext):
        result = processors[extensions[ext]](source)


    return result


if __name__=="__main__":
    #print process_file("demosite/content/index.html")
    #print "\n--------------------\n"
    print process_file("demosite/content/one.md")
