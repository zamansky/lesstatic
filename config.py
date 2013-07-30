import yaml



# config is the "global" configuration dictionary
# Other than storing the base_dir when created, it should be
# treated as read only
config={}

def load_config(file="config.yaml"):
    global config
    try:
        yd = yaml.load(open(file).read())
        for k in yd.keys():
            config[k]=yd[k]
        return True
    except:
        return False


if __name__=="__main__":
    print load_config()
    print config

