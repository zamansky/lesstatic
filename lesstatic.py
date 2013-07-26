import config
import process_source as ps
import os,sys
import shutil
import re,time

def build_site():
    if os.path.exists(config.site):
        shutil.rmtree(config.site)
    os.mkdir(config.site)
    if os.path.exists(config.static):
        shutil.copytree(config.static,config.site+"/"+config.static_dest)

    valid_extensions = config.extensions.keys()
    valid_extensions.append('html')
    for (dir,subs,files) in os.walk(config.content):
        dest = re.sub(config.content,config.site,dir)
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
    olds=" ".join([" ".join(["%f"%os.stat(dir+"/"+f).st_mtime for f in files if f[0]!='.']) for (dir,subs,files) in os.walk(config.content)])
    while  True:
        time.sleep(1)
        news=" ".join([" ".join(["%f"%os.stat(dir+"/"+f).st_mtime for f in files if f[0] !='.']) for (dir,subs,files) in os.walk(config.content)])
        if news!=olds:
            print "REBUILDING"
            build_site()
            olds = news



if __name__=="__main__":
    if len(sys.argv)>1:
        os.chdir(sys.argv[-1])
        config.base_dir=os.getcwd()
        build_site()
    if sys.argv[1]=='serve':
        serve()
