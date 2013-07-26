import config 
import process_source as ps
import os
import shutil
import re,time

def build_site():
    if os.path.exists(config.site):
        shutil.rmtree(config.site)
    os.mkdir(config.site)
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
    build_site()

if __name__=="__main__":
    config.base_dir=os.getcwd()
    print "HELLO"
    serve()



