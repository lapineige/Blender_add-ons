######################################################################################################
# An operator to save your file with an incremental suffix                                          #
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
    "version": (1, 2),
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
        if bpy.data.filepath:
            f_path = bpy.data.filepath
            bpy.ops.wm.save_mainfile(filepath=f_path)
            str_nb = "001"
            int_nb = 1
            new_nb = str_nb.replace(str(int_nb),str(int_nb+1))   
            output = f_path.replace(str_nb,new_nb)

            i = 1
            while os.path.isfile(output):
                i += 1
                new_nb = str_nb.replace(str(int_nb),str(int_nb+i))
                output = f_path.rpartition("_")[-1].rpartition(".blend")[0] + '_' + new_nb + '.blend'
            
            bpy.ops.wm.save_as_mainfile(filepath=output, copy=True)
            self.report({'INFO'}, "File: {0} - Created at: {1}".format(output[len(bpy.path.abspath("//")):], output[:len(bpy.path.abspath("//"))]))
        else:
            self.report({'WARNING'}, "Please save your main file")
        return {'FINISHED'}
        ###### PENSER A TESTER AUTRES FICHIERS DU DOSSIER, VOIR SI NUMERO SUPERIEUR ==> WARNING

def register():
    bpy.utils.register_class(FileIncrementalSave)


def unregister():
    bpy.utils.unregister_class(FileIncrementalSave)


if __name__ == "__main__":
    register()
