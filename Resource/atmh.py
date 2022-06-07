from ..Utilities import *

class ATMH:
    """
    ??? Header Informations
    Contains :
    - ??? Informations
    """

    def __init__(self, br):
        
        self.size = 0

        self.atmc_list = []

        self.read(br)

    def read(self, br):
        
        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        atmc_count = br.readUInt()
        br.readUInt()

        for i in range(atmc_count):

            self.atmc_list.append(ATMH.ATMC(br))

    class ATMC :
        """
        ??? Informations
        Contains :
        - Mesh Index
        - Material Index
        - Frame Index\n
        Used to build the whole model
        """

        def __init__(self, br):
        
            self.size = 0

            # Mesh Index
            self.gm2_index = 0

            # Material Index
            self.mtrl_index = 0

            # Frame Index
            self.fram_index = 0

            self.read(br)

        def read(self, br):
            
            header = br.bytesToString(br.readBytes(4))
            self.size = br.readUInt()
            br.readUInt()
            br.readUInt()

            position = br.tell()

            br.readUInt() # ???
            self.gm2_index = br.readUShort()
            self.mtrl_index = br.readUShort()
            self.fram_index = br.readUShort()
            br.readUShort() # ???
            br.readUInt() # ???

            br.seek(position + self.size, 0)