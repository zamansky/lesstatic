import yaml




config={}
def load_config(file="config.yaml"):
    yamldict = yaml.load(open(file).read())
    for k in yamldict:
        config[k]=yamldict[k]


if __name__=="__main__":
    load_config()
    print config
