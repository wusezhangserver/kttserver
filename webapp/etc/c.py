from configer import JsonConfiger

def set_up(file):
    configer = JsonConfiger()
    configer.load_file(file)
    attrs = configer.get()
    for k,v in attrs.iteritems():
        confs.__setattr__(k,v)

class C(object):
    pass

confs = C()