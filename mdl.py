from .Blender import *
from .Resource import *
from .Utilities import *

class MDL:

    def __init__(self, br):

        self.mdlh = MDLH(br)
        print(br.tell())
        self.mtrh = MTRH(br)
        print(br.tell())
        self.tex  = TEX(br)
        print(br.tell())
        self.frah = FRAH(br)
        print(br.tell())
        self.eskl = ESKL(br, self.frah)
        print(br.tell())
        self.bdm2 = BDM2(br)
        print(br.tell())
        self.gmh2 = GMH2(br)
        print(br.tell())
        self.atmh = ATMH(br)
        print(br.tell())
        self.loda = LODA(br)
        print(br.tell())
        self.end  = END(br)
        print(br.tell())
        
        