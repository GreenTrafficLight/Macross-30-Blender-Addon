bl_info = {
	"name": "Macross 30 Models format",
	"description": "Import Macross 30 Model",
	"author": "GreenTrafficLight",
	"version": (1, 0),
	"blender": (2, 92, 0),
	"location": "File > Import > Macross 30 Importer",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

import bpy
import struct

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportRidgeRacer(Operator, ImportHelper):
    """Load a Macross 30 model file"""
    bl_idname = "import_macross30.data"
    bl_label = "Import Macross 30 model"

    filename_ext = ".mdl"
    filter_glob: StringProperty(default="*.mdl", options={'HIDDEN'}, maxlen=255,)

    clear_scene: BoolProperty(
        name="Clear scene",
        description="Example Tooltip",
        default=True,
    )

    def execute(self, context):
        from . import  import_macross
        return import_macross.main(self.filepath, self.clear_scene)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportRidgeRacer.bl_idname, text="Macross 30")


def register():
    bpy.utils.register_class(ImportRidgeRacer)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportRidgeRacer)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
