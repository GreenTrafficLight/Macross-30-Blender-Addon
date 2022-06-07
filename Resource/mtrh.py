class MTRH:
    """
    Materials informations header\n
    Contains :
    - How many material there is in the model
    """
 
    def __init__(self, br):
        
        self.size = 0
        
        self.mtrl_count = 0
        self.mtrl_list = []

        self.read(br)

    def read(self, br):
        
        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        br.readUInt()
        br.readUInt()
        self.mtrl_count = br.readUInt()

        self.read_MTRL(br)

    def read_MTRL(self, br):

        for i in range(self.mtrl_count):

            self.mtrl_list.append(MTRH.MTRL(br))

    class MTRL:
        """
        Material informations\n
        Contains :
        - The shader used
        - The texture used
        - The properties of the material
        """

        def __init__(self, br):
        
            self.size = 0

            self.name = ""
            self.shader_name = ""
            self.tex_index = None

            self.read(br)

        def read(self, br):
        
            header = br.bytesToString(br.readBytes(4))
            self.size = br.readUInt()
            br.readUInt()
            br.readUInt()

            position = br.tell()

            # TO DO
            self.name = br.bytesToString(br.readBytes(256)).replace("\0", "")
            br.readUInt() # ?
            self.shader_name = br.bytesToString(br.readBytes(32)).replace("\0", "") # ?
            br.readBytes(88) # Material Properties ?
            unknown_count = br.readUInt()
            br.readBytes(40)
            for i in range(unknown_count):
                if i == 0 and unknown_count < 5:
                    self.tex_index = br.readUInt()
                    br.readBytes(16)
                elif i == 1 and unknown_count == 5: # TEST
                    self.tex_index = br.readUInt()
                    br.readBytes(16)
                else:
                    br.readBytes(20)  

            br.seek(position + self.size, 0) 

