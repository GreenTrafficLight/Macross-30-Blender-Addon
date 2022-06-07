from ..Utilities import *

class BDM2:
    """
    ??? Informations
    """

    def __init__(self, br):
        
        self.size = 0

        self.read(br)

    def read(self, br):
        
        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        br.readUInt()
        br.readUInt()

        for i in range(4):

            Vector3.fromBytes(br.readBytes(12))