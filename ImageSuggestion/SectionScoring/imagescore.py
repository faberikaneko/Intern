class ImageScore(object):
    IMAGE=u"image"
    TABLE=u"table"
    GRAPH=u"graph"
    FLOW=u"flow"
    """description of class"""
    taglist = [IMAGE,TABLE,GRAPH,FLOW]
    def __init__(self,dict):
        self.dict = dict
    def __getitem__(self,key):
        if key in self.taglist:
            return self.dict.get(key)
        else:
            raise IndexError
    def __add__(self,other):
        if not isinstance(other,(ImageScore,dict)):
            raise TypeError
        for tag in taglist:
            if not tag in other:
                raise ValueError
            self.dict[tag] += other.get(tag)
        return self 