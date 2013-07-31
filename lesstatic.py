from config import config, load_config
import process_source as ps
import os,sys
import shutil
import re,time
import server


def build_site():
    """
    Walk the content tree and build the entire site.
    """

    # Either empty the existing entire site folder
    if os.path.exists(config['site']):
        # We don't want to just remove the entire folder  - if we do and we're running a
        # server, it will lose it's directory and will have to be re-run
        # by just emptying the folder, the server will automatically find the new site
        for f in os.listdir(config['site']):
            filename = config['site']+"/"+f
            if os.path.isfile(filename):
                os.remove(filename)
            else:
                # We can safely remove entire subtrees of the site folder
                shutil.rmtree(filename)
    else: # or make a new site folder if one doesn't exist
        os.mkdir(config['site'])

    # Copy any static stuff over
    if os.path.exists(config['static']):
        shutil.copytree(config['static'],config['site']+"/"+config['static_dest'])

    # Generate the content
    valid_extensions = config['extensions'].keys()

    # Walk through the content folder (making subdirectories as needed
    # and process each file
    # We'll have to revisit this when we do the posts stuff
    # but for now it works
    for (dir,subs,files) in os.walk(config['content']):
        dest = re.sub(config['content'],config['site'],dir)
        for sub in subs:
            if not os.path.exists(dest+"/"+sub):
                os.mkdir(dest+"/"+sub)
        for f in files:
            (name,ext)=os.path.splitext(f)
            if name[0] != '.' and ext[1:] in valid_extensions:
                result = ps.process_file(dir+"/"+f)
                outfilename=dest+"/"+name+".html"
                outfile = open(outfilename,"w")
                outfile.write(result)
                outfile.close()


def serve():
    """
    Start the server (see server.py) and then check every second to see
    if a file changes, if so,  rebuild the site.

    It's not efficient, it just sees if ANY file that isn't hidden changes.
    """
    olds=" ".join([" ".join(["%f"%os.stat(dir+"/"+f).st_mtime for f in files if f[0]!='.']) for (dir,subs,files) in os.walk(config['content'])])
    pid = server.start_server()
    while  True:
        time.sleep(1)
        news=" ".join([" ".join(["%f"%os.stat(dir+"/"+f).st_mtime for f in files if f[0] !='.']) for (dir,subs,files) in os.walk(config['content'])])
        if news!=olds:
            print "REBUILDING"
            build_site()
            olds = news


initial_config="""
port: 5544
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
    print "Ok making init stuff in current directory"



    


import argparse
def parse_args():
    
    parser = argparse.ArgumentParser(description="LesStatic Argument")
    parser.add_argument('-i','--init',action='store_true',help='initialize new project')
    parser.add_argument('folder',metavar='FOLDER',nargs="?",help='Folder for project (undefined = current folder)')
    parser.add_argument('-p','--port',nargs='?')
    parser.add_argument('-s','--serve',action='store_true',help='Run server and rebuild on change')
    args=parser.parse_args()
    if args.init:
        init_project(args.folder)
        sys.exit(0)

    if args.folder != None:
        os.chdir(args.folder)
    has_config=load_config()
    config['base_dir']=os.getcwd()
    if args.port!=None:
        config['port']=args.port
    if args.serve:
        serve()
    else:
        build_site()

            
    


if __name__=="__main__":
    parse_args()
    # load_config()
    # if len(sys.argv)>1:
    #     os.chdir(sys.argv[-1])
    #     config['base_dir']=os.getcwd()
    #     build_site()
    # if sys.argv[1]=='serve':
    #     serve()


