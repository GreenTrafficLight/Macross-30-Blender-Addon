class TEX:
    """
    Textures informations\n
    Contains :
    - How many texture is used by the model
    - The textures names
    """
 
    def __init__(self, br):
        
        self.size = 0

        self.tex_list = []

        self.read(br)

    def read(self, br):
        
        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        texture_name_count = br.readUInt()
        texture_name_size = br.readUInt()

        for i in range(texture_name_count):

            self.tex_list.append(br.bytesToString(br.readBytes(texture_name_size)).replace("\0", ""))