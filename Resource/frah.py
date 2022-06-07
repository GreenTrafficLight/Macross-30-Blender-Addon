class FRAH:
    """
    Frame(?) Header Informations\n
    Contains :
    - How many frames there are in the model
    """
 
    def __init__(self, br):
        
        self.size = 0

        self.fram_list = []

        self.read(br)

    def read(self, br):

        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        br.readUInt()
        br.readUInt()
        
        position = br.tell()

        fram_count = br.readUInt()

        for i in range(fram_count):

            self.fram_list.append(FRAH.FRAM(br))

        br.seek(position + self.size, 0) # Scale ?

    class FRAM :
        """
        Frame(?) Informations\n
        Contains :
        - Name of frame
        - Parent of frame
        - Mesh Position, Rotation, Quaternion and Scale
        """

        def __init__(self, br):
            
            self.size = 0
            self.name = ""

            self.index = 0
            self.parent_index = 0

            self.translation = None
            self.rotation = None
            self.quaternion = None
            self.scale = None

            self.read(br)

        def read(self, br):
        
            header = br.bytesToString(br.readBytes(4))
            self.size = br.readUInt()
            br.readUInt()
            br.readUInt()

            position = br.tell()

            self.index = br.readInt() # unknown index
            self.name = br.bytesToString(br.readBytes(36)).replace("\0", "") # 36 ?
            self.parent_index = br.readInt() # unknown index
            br.readInt() # unknown index
            br.readInt() # unknown index

            br.readBytes(16) # Quaternion ?
            br.readBytes(12) # Scale ?

            br.seek(position + self.size, 0) # Scale ?