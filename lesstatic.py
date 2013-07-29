from config import config, load_config
import process_source as ps
import os,sys
import shutil
import re,time
import server
def build_site():
    if os.path.exists(config['site']):
        for f in os.listdir(config['site']):
            filename = config['site']+"/"+f
            if os.path.isfile(filename):
                os.remove(filename)
            else:
                shutil.rmtree(filename)
    else:
        os.mkdir(config['site'])
    if os.path.exists(config['static']):
        shutil.copytree(config['static'],config['site']+"/"+config['static_dest'])

    valid_extensions = config['extensions'].keys()
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

    print "HELLO"
    olds=" ".join([" ".join(["%f"%os.stat(dir+"/"+f).st_mtime for f in files if f[0]!='.']) for (dir,subs,files) in os.walk(config['content'])])
    pid = server.start_server()
    while  True:
        time.sleep(1)
        news=" ".join([" ".join(["%f"%os.stat(dir+"/"+f).st_mtime for f in files if f[0] !='.']) for (dir,subs,files) in os.walk(config['content'])])
        if news!=olds:
            print "REBUILDING"
            time.sleep(3)
            build_site()
            olds = news



if __name__=="__main__":
    load_config()
    if len(sys.argv)>1:
        os.chdir(sys.argv[-1])
        config['base_dir']=os.getcwd()
        build_site()
    if sys.argv[1]=='serve':
        serve()