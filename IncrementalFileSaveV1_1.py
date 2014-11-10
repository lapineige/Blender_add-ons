######################################################################################################
# An operator to save your file with an incremental suffix.                                          #
# Actualy partly uncommented - if you do not understand some parts of the code,                      #
# please see further version or contact me.                                                          #
# Author: Lapineige                                                                                  #
# License: GPL v3                                                                                    #
######################################################################################################

############# Add-on description (used by Blender)

bl_info = {
    "name": "Incremental Saving",
    "description": 'Save your file with an incremental suffix',
    "author": "Lapineige",
    "version": (1, 1),
    "blender": (2, 72, 0),
    "location": "Search > Save Incremental",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "http://blenderlounge.fr/forum/viewtopic.php?f=18&t=736",
    "category": "System"}

##############
import bpy, os

class FileIncrementalSave(bpy.types.Operator):
    bl_idname = "file.save_incremental"
    bl_label = "Save Incremental"
    bl_options = {"REGISTER"}
   
    def execute(self, context):
        f_path = bpy.data.filepath
        bpy.ops.wm.save_mainfile(filepath=f_path)
        if f_path.find("_") != -1:
            str_nb = f_path.rpartition("_")[-1].rpartition(".blend")[0]
            int_nb = int(str_nb)
            new_nb = str_nb.replace(str(int_nb),str(int_nb+1))   
            output = f_path.replace(str_nb,new_nb)
            
            i = 1
            while os.path.isfile(output):
                str_nb = f_path.rpartition("_")[-1].rpartition(".blend")[0]
                i += 1
                new_nb = str_nb.replace(str(int_nb),str(int_nb+i))
                output = f_path.replace(str_nb,new_nb)
        else:
            output = f_path.rpartition(".blend")[0]+"_001"+".blend"
            
        bpy.ops.wm.save_as_mainfile(filepath=output)
        self.report({'INFO'}, "File: {0} - Created at: {1}".format(output[len(bpy.path.abspath("//")):], output[:len(bpy.path.abspath("//"))]))
        bpy.ops.wm.open_mainfile(filepath=f_path)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(FileIncrementalSave)


def unregister():
    bpy.utils.unregister_class(FileIncrementalSave)


if __name__ == "__main__":
    register()
