import bmesh
import os

from math import *
from bpy_extras import image_utils

from .mdl import *

from .Blender import *
from .Utilities import *
from .Resource import *


def build_mdl_armature(mdl, file_name):

    
    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.name = mdl.frah.fram_list[0].name

    amt = ob.data
    amt.name = mdl.frah.fram_list[0].name

    """
    for fram in mdl.frah.fram_list:

        if fram.name != "":

            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            bone = amt.edit_bones.new(fram.name)

            bone.tail = (0.01 , 0.01, 0.01)

            matrix = Matrix.Identity(4)

            matrix = Matrix.Translation(fram.translation)

            matrix @= fram.quaternion.to_matrix().to_4x4()

            bone.matrix = matrix

    bones = amt.edit_bones
    for fram in mdl.frah.fram_list:

        if fram.name != "":

            bone = bones[fram.name]

            if bone.parent != -1 and fram.parent_index != 0:

                bone.parent = amt.edit_bones[mdl.frah.fram_list[fram.parent_index].name]
                bone.matrix = amt.edit_bones[mdl.frah.fram_list[fram.parent_index].name].matrix @ bone.matrix 

    for fram in mdl.frah.fram_list:

        if fram.name != "":

            bone = bones[fram.name]

            if bone.parent != -1 and fram.parent_index != 0:

                bone.tail = bones[mdl.frah.fram_list[fram.parent_index].name].head 
    """

    bpy.ops.object.mode_set(mode='OBJECT')
    

    for fram in mdl.frah.fram_list:

        if fram.name != "":

            empty = add_empty(fram.name, empty_location = fram.translation, empty_rotation = fram.quaternion.to_euler(), empty_scale = fram.scale)
            empty.pass_index = fram.index

            if fram.parent_index == 0:
                empty.rotation_euler = ( radians(90), 0, 0 )

            if fram.parent_index != -1 and fram.parent_index != 0:
                empty.parent = bpy.context.scene.objects[fram.parent_index]

def build_mdl(mdl, filepath):

    for atmc in mdl.atmh.atmc_list:

        fram = mdl.frah.fram_list[atmc.fram_index]
        gm2 = mdl.gmh2.gm2_list[atmc.gm2_index]
        mtrl = mdl.mtrh.mtrl_list[atmc.mtrl_index]

        mesh = bpy.data.meshes.new(gm2.name)
        obj = bpy.data.objects.new(gm2.name, mesh)

        parent = bpy.context.scene.objects[fram.name]

        if bpy.app.version >= (2, 80, 0):
            parent.users_collection[0].objects.link(obj)
        else:
            parent.users_collection[0].objects.link(obj)

        obj.parent = parent

        vertexList = {}
        facesList = []
        normals = []

        last_vertex_count = 0

        for gmpt in gm2.gpmt_list:

            bm = bmesh.new()
            bm.from_mesh(mesh)

            # Set vertices
            for j in range(len(gmpt.vertex_buffer["Positions"])):
                vertex = bm.verts.new(gmpt.vertex_buffer["Positions"][j])

                if "Normals" in gmpt.vertex_buffer:
                    vertex.normal = gmpt.vertex_buffer["Normals"][j]
                    normals.append(gmpt.vertex_buffer["Normals"][j])
                            
                vertex.index = last_vertex_count + j

                vertexList[last_vertex_count + j] = vertex

            faces = ToTriangle(gmpt.face_buffer)

            # Set faces
            for j in range(0, len(faces)):
                try:
                    face = bm.faces.new([vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2] + last_vertex_count]])
                    face.smooth = True
                    facesList.append([face, [vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2]] + last_vertex_count]])
                except:
                    pass
            
            # Set uv
            if gmpt.has_texCoords == True:

                if gmpt.vertex_buffer["TexCoords_1"] != []:
                    uv_layer1 = bm.loops.layers.uv.verify()
                if gmpt.vertex_buffer["TexCoords_2"] != []:
                    uv_layer2 = bm.loops.layers.uv.verify()                
                if gmpt.vertex_buffer["TexCoords_3"] != []:
                    uv_layer3 = bm.loops.layers.uv.verify()
                if gmpt.vertex_buffer["TexCoords_4"] != []:
                    uv_layer4 = bm.loops.layers.uv.verify()
                if gmpt.vertex_buffer["TexCoords_5"] != []:
                    uv_layer5 = bm.loops.layers.uv.verify()
                if gmpt.vertex_buffer["TexCoords_6"] != []:
                    uv_layer6 = bm.loops.layers.uv.verify()

                for f in bm.faces:
                    
                    if gmpt.vertex_buffer["TexCoords_1"] != []:
                        for l in f.loops:
                            if l.vert.index >= last_vertex_count:
                                l[uv_layer1].uv = [gmpt.vertex_buffer["TexCoords_1"][l.vert.index - last_vertex_count][0], 1 - gmpt.vertex_buffer["TexCoords_1"][l.vert.index - last_vertex_count][1]]
                   
                    if gmpt.vertex_buffer["TexCoords_2"] != []:
                        for l in f.loops:
                            if l.vert.index >= last_vertex_count:
                                l[uv_layer2].uv = [gmpt.vertex_buffer["TexCoords_2"][l.vert.index - last_vertex_count][0], 1 - gmpt.vertex_buffer["TexCoords_2"][l.vert.index - last_vertex_count][1]]

                    if gmpt.vertex_buffer["TexCoords_3"] != []:
                        for l in f.loops:
                            if l.vert.index >= last_vertex_count:
                                l[uv_layer3].uv = [gmpt.vertex_buffer["TexCoords_3"][l.vert.index - last_vertex_count][0], 1 - gmpt.vertex_buffer["TexCoords_3"][l.vert.index - last_vertex_count][1]]

                    if gmpt.vertex_buffer["TexCoords_4"] != []:
                        for l in f.loops:
                            if l.vert.index >= last_vertex_count:
                                l[uv_layer4].uv = [gmpt.vertex_buffer["TexCoords_4"][l.vert.index - last_vertex_count][0], 1 - gmpt.vertex_buffer["TexCoords_4"][l.vert.index - last_vertex_count][1]]

                    if gmpt.vertex_buffer["TexCoords_5"] != []:
                        for l in f.loops:
                            if l.vert.index >= last_vertex_count:
                                l[uv_layer5].uv = [gmpt.vertex_buffer["TexCoords_5"][l.vert.index - last_vertex_count][0], 1 - gmpt.vertex_buffer["TexCoords_5"][l.vert.index - last_vertex_count][1]]

                    if gmpt.vertex_buffer["TexCoords_6"] != []:
                        for l in f.loops:
                            if l.vert.index >= last_vertex_count:
                                l[uv_layer6].uv = [gmpt.vertex_buffer["TexCoords_6"][l.vert.index - last_vertex_count][0], 1 - gmpt.vertex_buffer["TexCoords_6"][l.vert.index - last_vertex_count][1]]

            bm.to_mesh(mesh)
            bm.free()            


            # Set normals
            #mesh.use_auto_smooth = True

            #if normals != []:
                #mesh.normals_split_custom_set_from_vertices(normals)

            # Set material
            material = bpy.data.materials.get(mtrl.name)
            if not material:
                material = bpy.data.materials.new(mtrl.name)

                material.use_nodes = True
                
                nodes = material.node_tree.nodes
                links = material.node_tree.links

                bsdf =  material.node_tree.nodes["Principled BSDF"]
                output = material.node_tree.nodes["Material Output"]

                if mtrl.tex_index != None:
                
                    texture_filepath = f"{os.path.split(filepath)[0]}" + "\\" + mdl.tex.tex_list[mtrl.tex_index]
                    
                    if os.path.isfile(texture_filepath):
                        
                        texture_file = image_utils.load_image(texture_filepath, check_existing=True)       

                        diffuseTextureImage_node = nodes.new(type='ShaderNodeTexImage')
                        diffuseTextureImage_node.image = texture_file
                        diffuseTextureImage_node.extension = 'CLIP'

                        links.new(bsdf.inputs['Base Color'], diffuseTextureImage_node.outputs['Color'])
                        links.new(bsdf.inputs['Alpha'], diffuseTextureImage_node.outputs['Alpha'])

                if "cxexxxx" in mtrl.shader_name:
                    material.blend_method = 'BLEND'
                else:
                    material.blend_method = 'OPAQUE'
                

            last_vertex_count += len(gmpt.vertex_buffer["Positions"])

        mesh.materials.append(material)

# Main

def main(filepath, clear_scene):
    if clear_scene:
        clearScene()

    file = open(filepath, 'rb')
    file_name =  filepath.split("\\")[-1]
    br = BinaryReader(file, ">")

    mdl = MDL(br)
    build_mdl_armature(mdl, os.path.splitext(file_name)[0])
    build_mdl(mdl, filepath)

    return {'FINISHED'}

if __name__ == '__main__':
    main()
