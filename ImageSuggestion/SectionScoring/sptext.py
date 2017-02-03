# -*- encoding:utf-8 -*-

class SpText(object):
    """splited text class"""
    def __init__(self,text,childs = None):
        self.text = text
        self.childs = childs if childs != None else []
        return
    def __str__(self):
        return self.text
    def __getitem__(self,key):
        try:
            return self.childs[key]
        except:
            raise