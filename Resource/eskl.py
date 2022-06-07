from ..Utilities import *

from mathutils import *

class ESKL:
    """
    Skeleton Header Informations\n
    Contains :
    - 
    """
 
    def __init__(self, br, frah):
        
        self.size = 0

        self.es00 = None

        self.read(br, frah)

    def read(self, br, frah):
        
        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        br.readUInt()
        br.readUInt()

        position = br.tell()

        self.es00 = ESKL.ES00(br, position, frah)

        br.seek(position + self.size, 0)

    class ES00:
        """
        Skeleton Informations\n
        Contains :
        - Bones matrices
        - Bones indices
        """

        def __init__(self, br, position, frah):
            
            self.size = 0

            self.unknowns1 = []
            self.matrices = []
            self.indices = []
            self.unknowns2 = []

            self.read(br, position, frah)

        def read(self, br, position, frah):
            
            header = br.bytesToString(br.readBytes(4))
            end_offset1 = br.readUInt() # end indices data
            end_offset2 = br.readUInt() 
            
            count1 = br.readUShort() # number of matrices and indices
            count2 = br.readUShort()
            count3 = br.readUShort()
            count4 = br.readUShort()
            
            count1_end_offset = br.tell() + br.readUInt() 
            count2_end_offset = br.tell() + br.readUInt() 
            count3_end_offset = br.tell() + br.readUInt()
            count4_end_offset = br.tell() + br.readUInt() 
            
            br.readUInt() # unknown 
            br.readUInt() # unknown
            br.readUInt() #  0x00000000

            self.read_unknowns1(br, count3)
            self.read_matrices(br, count1, frah)
            self.read_indices(br, count1)

            br.seek(position + end_offset1)

            self.read_unknowns2(br, count1)
            self.read_unknowns3(br, count2)
            print(br.tell())

        def read_unknowns1(self, br, count):

            for i in range(count):

                self.unknowns1.append(Vector4.fromBytes(br.readBytes(16)))
    
        def read_matrices(self, br, count, frah):
            """
            Read the matrices of bones
            """

            for i in range(count):

                quaternion = (br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat())
                frah.fram_list[i].quaternion = Quaternion((quaternion[3], -quaternion[0], quaternion[2], quaternion[1]))
                translation = (br.readFloat(), br.readFloat(), br.readFloat())
                frah.fram_list[i].translation = Vector((-translation[0], translation[2], translation[1]))
                br.readBytes(4)
                scale = (br.readFloat(), br.readFloat(), br.readFloat())
                frah.fram_list[i].scale = Vector((scale[0], scale[2], scale[1]))
                br.readBytes(4)

        def read_indices(self, br, count):
            """
            Read the indices of bones
            """

            for i in range(count):

                self.indices.append(br.readUShort())

        def read_unknowns2(self, br, count):

            for i in range(count):

                self.unknowns2.append(br.readUInt())              

        def read_unknowns3(self, br, count):

            for i in range(count):

                br.readUInt()
                br.readUInt()

            for i in range(count):

                br.readUByte()
    
                      