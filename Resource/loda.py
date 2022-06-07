from ..Utilities import *

class LODA:
    """
    LOD Informations\n
    """

    def __init__(self, br):
        
        self.size = 0

        self.read(br)

    def read(self, br):
        
        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        br.readUInt()
        br.readUInt()