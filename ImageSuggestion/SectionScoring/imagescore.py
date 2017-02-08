class ImageScore(object):
    IMAGE=u"image"
    TABLE=u"table"
    GRAPH=u"graph"
    FLOW=u"flow"
    """description of class"""
    taglist = [IMAGE,TABLE,GRAPH,FLOW]
    def __init__(self,dict):
        self.dict = dict