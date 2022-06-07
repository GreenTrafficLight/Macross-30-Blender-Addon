class MDLH:
    """
    Model Header
    Contains the whole model (duh)
    """

    def __init__(self, br):
        
        self.size = 0
        self.mdl_ = None

        self.read(br)

    def read(self, br):
        
        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        br.readUInt()
        br.readUInt()

        self.mdl_ = MDLH.MDL_(br)

    class MDL_:
        """
        The model itself
        """

        def __init__(self, br):
            
            self.read(br)

        def read(self, br):
            header = br.bytesToString(br.readBytes(4))
            br.readUInt()
