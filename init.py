import os,sys 

initial_config="""
port: 8000
templates: templates
content: content
static: static
static_dest: static
site: site
extensions:
 md: markdown
 htm : html
 html: html
"""

init_dirs=['templates','content','static']

base_template="""
<html>

<h1>Stuff at the top </h1>
{% block content %}
{% endblock %}
<h2>Stuff at the bottom<h2>

</html>
"""

index_html="""
---
layout: base.html
title: The LesStatic Sample Page
author: Mike Zamansky
var: a new variable
l:
 - one
 - two
 - three
d:
 key1: val1
 key2: val2
 key3: val3
block: content
---

<h1> {{title}} </h1>
<h2> by {{author}} </h2>

<hr>
You can use any variable declared in
the yaml up top like here: {{ var }} 
<hr>

You can also use a yaml list:

<ul>
{% for item in l %}
<li>foof {{item}}</li>
{% endfor %}
</ul>

Or dictionary:

<ol>
{% for k in d %}
<li>{{k}} : {{d[k]}}</li>
{% endfor %}
</ol>




"""


def init_project(folder):
    # if folder is none, make sure dir is empty
    # if not, make sure the folder doesn't exist
    # then copy over skeleton structure
    if folder==None or folder=="." :
        if len(os.listdir("."))!=0:
            print "Directory not empty"
            return
    else:    
        if os.path.exists(folder):
            print "Directory already exists"
            return
        else:
            os.mkdir(folder)
            os.chdir(folder)
    f=open("config.yaml","w")
    f.write(initial_config)
    f.close()

    for d in init_dirs:
        os.mkdir(d)
    f = open("content/index.html","w")
    f.write(index_html)
    f.close()
    f = open("templates/base.html","w")
    f.write(base_template)
    f.close()



    

