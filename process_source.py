#!/usr/bin/python
import re

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
            doc=doc+line
    return (yaml_dict,doc)

if __name__=="__main__":
    print separate_front_matter(open("demosite/content/index.html").read())
    print separate_front_matter(open("demosite/content/one.md").read())

