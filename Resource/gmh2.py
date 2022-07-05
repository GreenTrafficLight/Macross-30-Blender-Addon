from ..Utilities import *

class GMH2:
    """
    Mesh Header Informations\n
    Contains :
    - Mesh Informations
    """

    def __init__(self, br):
        
        self.size = 0
        self.gm2_list = []

        self.read(br)

    def read(self, br):
        
        header = br.bytesToString(br.readBytes(4))
        self.size = br.readUInt()
        gm2_count = br.readUInt()
        br.readUInt()

        for i in range(gm2_count):

            self.gm2_list.append(GMH2.GM2(br))

    class GM2:
        """
        Mesh Information\n
        Contains :
        - How many vertex and face buffer the mesh use
        """

        def __init__(self, br):
        
            self.size = 0
            self.name = ""

            self.gpmt_list = []

            self.read(br)

        def read(self, br):
            
            header = br.bytesToString(br.readBytes(4))
            self.size = br.readUInt()
            gpmt_count = br.readUInt()
            br.readUInt() # Unknown

            position = br.tell()

            self.name = br.bytesToString(br.readBytes(32)).replace("\0", "")

            br.readUInt() # Unknown
            br.readUInt() # Unknown
            br.readUInt() # Unknown
            br.readBytes(36) # Unknown

            for i in range(gpmt_count):
                self.gpmt_list.append(GMH2.GM2.GMPT(br))

            br.seek(position + self.size, 0)

        class GMPT:
            """
            Vertex and Face Buffer Informations\n
            Contains :
            - Vertex Buffer
            - Face Buffer
            """

            def __init__(self, br):
            
                self.size = 0

                self.face_buffer = []
                self.vertex_buffer = {
                    "Positions" : [],
                    "Normals" : [],
                    "Colors" : [],
                    "TexCoords_1" : [],
                    "TexCoords_2" : [],
                    "TexCoords_3" : [],
                    "TexCoords_4" : [],
                    "TexCoords_5" : [],
                    "TexCoords_6" : []
                    }

                self.has_texCoords = False

                self.read(br)

            def read(self, br):
                
                header = br.bytesToString(br.readBytes(4))
                self.size = br.readUInt()
                br.readUInt() # zeros
                br.readUInt() # zeros

                position = br.tell()

                br.readUShort()
                vertex_type = br.readUShort()
                br.readUShort()
                vertex_count = br.readUInt()
                face_count = br.readUShort()
                br.readUInt() # 0xFFFFFFFF ?

                br.readUShort()
                face_buffer_offset = br.readUShort()
                face_buffer_size1 = br.readUShort()
                face_buffer_size2 = br.readUShort()
                br.readUShort()
                vertex_buffer_offset = br.readUShort()
                br.readUShort()
                br.readUShort()
                vertex_buffer_size1 = br.readUShort()
                vertex_buffer_size2 = br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()
                br.readUShort()

                br.readUInt()
                br.readUInt()
                br.readUInt()

                br.seek(position + face_buffer_offset, 0)
                self.read_face_buffer(br, face_count)

                br.seek(position + vertex_buffer_offset, 0)
                self.read_vertex_buffer(br, vertex_buffer_size1, vertex_buffer_size2, vertex_type)

                br.seek(position + self.size, 0)

            def read_face_buffer(self, br, face_count):

                print("Face Buffer : " + str(br.tell()) + " Face Count : " + str(face_count))
                for i in range(face_count):
                    self.face_buffer.append(br.readUShort())

            def get_vertex_stride(self, vertex_type):

                if vertex_type == 0x303: vertex_stride = 0x18
                elif vertex_type == 0x606: vertex_stride = 0x1C
                elif vertex_type == 0x707: vertex_stride =  0x10
                elif vertex_type == 0x0C08: vertex_stride = 0x10
                elif vertex_type == 0x0D09: vertex_stride = 0x14
                elif vertex_type == 0x0F0B: vertex_stride = 0x14
                elif vertex_type == 0x100C: vertex_stride = 0x14
                elif vertex_type == 0x110D: vertex_stride = 0x18
                elif vertex_type == 0x120E: vertex_stride = 0x1C
                elif vertex_type == 0x130F: vertex_stride = 0x20
                elif vertex_type == 0x1511: vertex_stride = 0x28
                elif vertex_type == 0x1A16: vertex_stride = 0x1C
                elif vertex_type == 0x1C18: vertex_stride = 0x24
                elif vertex_type == 0x1D19: vertex_stride = 0x20
                elif vertex_type == 0x1E1A: vertex_stride = 0x2C
                elif vertex_type == 0x1F1B: vertex_stride = 0x28
                elif vertex_type == 0x201C: vertex_stride = 0x24
                elif vertex_type == 0x2521: vertex_stride = 0x1C
                elif vertex_type == 0x2D29: vertex_stride = 0x28
                elif vertex_type == 0x2F2B: vertex_stride = 0x20
                elif vertex_type == 0x3430: vertex_stride = 0x18
                elif vertex_type == 0x3C38: vertex_stride = 0x2C
                elif vertex_type == 0x403C: vertex_stride = 0x28
                elif vertex_type == 0x4440: vertex_stride = 0x38
                elif vertex_type == 0x4541: vertex_stride = 0x38 
                elif vertex_type == 0x524E: vertex_stride = 0x28

                return vertex_stride

            def read_vertex_buffer(self, br, vertex_buffer_size1, vertex_buffer_size2, vertex_type):
                
                vertex_stride = self.get_vertex_stride(vertex_type)
                vertex_count = (vertex_buffer_size1 + vertex_buffer_size2) // vertex_stride

                print("Vertex Buffer : " + str(br.tell()) + " Vertex Count : " + str(vertex_count) + " Vertex Type : " + str(vertex_type))
                for i in range(vertex_count):
                    self.vertex_buffer["Positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])

                    if vertex_type == 0x303:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readBytes(4)
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])

                        self.has_texCoords = True

                    elif vertex_type == 0x606:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readBytes(8)
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])

                        self.has_texCoords = True

                    elif vertex_type == 0x707:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readBytes(8)
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])

                        self.has_texCoords = True

                    elif vertex_type == 0x0C08:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))

                    elif vertex_type == 0x0D09:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])

                        self.has_texCoords = True

                    elif vertex_type == 0x0F0B:

                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        br.readBytes(4)

                        self.has_texCoords = True

                    elif vertex_type == 0x100C:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        self.vertex_buffer["Colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

                        self.has_texCoords = True

                    elif vertex_type == 0x110D:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        br.readBytes(4)

                        self.has_texCoords = True

                    elif vertex_type == 0x120E:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["Colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

                        self.has_texCoords = True

                    elif vertex_type == 0x130F:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["Colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

                        self.has_texCoords = True

                    elif vertex_type == 0x1511: 

                        br.readBytes(4)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        self.vertex_buffer["TexCoords_3"].append([br.readHalfFloat(), br.readHalfFloat()])

                        self.has_texCoords = True

                    elif vertex_type == 0x1A16:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 

                        self.has_texCoords = True

                    elif vertex_type == 0x1C18:

                        br.readBytes(4)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()])                        

                        self.has_texCoords = True

                    elif vertex_type == 0x1D19:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()])                         

                        self.has_texCoords = True

                    elif vertex_type == 0x1E1A:

                        br.readBytes(4)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        self.vertex_buffer["TexCoords_3"].append([br.readHalfFloat(), br.readHalfFloat()])
                        br.readBytes(4)

                        self.has_texCoords = True

                    elif vertex_type == 0x1F1B:

                        br.readBytes(4)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        br.readBytes(4)

                        self.has_texCoords = True

                    elif vertex_type == 0x201C:

                        br.readBytes(4)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 

                        self.has_texCoords = True

                    elif vertex_type == 0x2521:

                        self.vertex_buffer["Colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 

                        self.has_texCoords = True

                    elif vertex_type == 0x2D29:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        self.vertex_buffer["TexCoords_3"].append([br.readHalfFloat(), br.readHalfFloat()])
                        br.readBytes(4)

                        self.has_texCoords = True

                    elif vertex_type == 0x2F2B:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()])                       

                        self.has_texCoords = True

                    elif vertex_type == 0x3430:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()])  

                        self.has_texCoords = True

                    elif vertex_type == 0x3C38:

                        br.readBytes(4)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        self.vertex_buffer["TexCoords_3"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_4"].append([br.readHalfFloat(), br.readHalfFloat()])                                            
    
                        self.has_texCoords = True

                    elif vertex_type == 0x403C:

                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        self.vertex_buffer["TexCoords_3"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_4"].append([br.readHalfFloat(), br.readHalfFloat()])

                        self.has_texCoords = True

                    elif vertex_type == 0x4440:

                        br.readBytes(8)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        self.vertex_buffer["TexCoords_3"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_4"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_5"].append([br.readHalfFloat(), br.readHalfFloat()])
                        br.readBytes(4)  

                        self.has_texCoords = True

                    elif vertex_type == 0x4541:

                        br.readBytes(8)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        br.readFloat() # Tangent/binormal
                        br.readFloat() # Tangent/binormal
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        self.vertex_buffer["TexCoords_3"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_4"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_5"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_6"].append([br.readHalfFloat(), br.readHalfFloat()])

                        self.has_texCoords = True

                    elif vertex_type == 0x524E:

                        br.readBytes(8)
                        self.vertex_buffer["Normals"].append(ConvertNormal_S10S11S11(br.readUInt()))
                        self.vertex_buffer["TexCoords_1"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_2"].append([br.readHalfFloat(), br.readHalfFloat()]) 
                        self.vertex_buffer["TexCoords_3"].append([br.readHalfFloat(), br.readHalfFloat()])
                        self.vertex_buffer["TexCoords_4"].append([br.readHalfFloat(), br.readHalfFloat()])

                        self.has_texCoords = True

                print("End : " + str(br.tell()))