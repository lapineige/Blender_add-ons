######################################################################################################
# An operator to automatically save your file with an incremental suffix                             #
# Actualy partly uncommented - if you do not understand some parts of the code,                      #
# please see further version or contact me.                                                          #
# Author: Lapineige                                                                                  #
# License: GPL v3                                                                                    #
######################################################################################################

############# Add-on description (used by Blender)

bl_info = {
    "name": "Auto Save Incremental",
    "description": 'Automatically save your file with an incremental suffix (after a defined period of time)',
    "author": "Lapineige",
    "version": (1, 3),
    "blender": (2, 74, 0),
    "location": "Search > Auto Save Incremental",
    "warning": "Beta version - may not work correctly",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"}

##############

import bpy, os
from time import time as tm
from bpy.props import IntProperty, FloatProperty

##############

class AutoSaveIncrementalPreferencesPanel(bpy.types.AddonPreferences):
    """ """
    bl_idname = __name__

    time_btw_save = bpy.props.IntProperty(default=300) # seconds
    dir_path_user_defined = bpy.props.StringProperty(subtype='DIR_PATH', default='//Incremental Save\\', description="Output directory for the render") # user defined, wil be changed by the code    # Voir chemin os + bouton setup adapté à l'os
    dir_path = bpy.props.StringProperty(subtype='DIR_PATH', default='', description="Output directory for the render used by the Auto Save tool")
    stop = bpy.props.BoolProperty(default=False, description="Property used to stop auto save - to avoid multiple simultaneous instances")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "time_btw_save", text="Timer (seconds)")
        layout.prop(self, "dir_path_user_defined", text="Auto-Save Directory")
        layout.operator('file.auto_save_incremental')
        layout.prop(self, "stop")
        return {'FINISHED'}

class FileIncrementalSave(bpy.types.Operator):
    bl_idname = "file.save_incremental"
    bl_label = "Save Incremental"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        if bpy.data.filepath:
            dir_name = context.user_preferences.addons[__name__].preferences.dir_path
            f_path = os.path.dirname(bpy.data.filepath) + dir_name + bpy.path.basename(bpy.data.filepath)
            #bpy.ops.wm.save_mainfile(filepath=f_path)

            # detecting number
            increment_files = [file for file in os.listdir(os.path.dirname(f_path)) if os.path.basename(f_path).split('.blend')[0] in file.split('.blend')[0] and file.split('.blend')[0] !=  os.path.basename(f_path).split('.blend')[0]]
            for file in increment_files:
                if not detect_number(file):
                    increment_files.remove(file)
            numbers_index = [ ( index, detect_number(file.split('.blend')[0]) ) for index, file in enumerate(increment_files)]
            numbers = [index_nb[1] for index_nb in numbers_index] #[detect_number(file.split('.blend')[0]) for file in increment_files]
            if numbers: # prevent from error with max()
                str_nb = str( max([int(n[2]) for n in numbers])+1 ) # zfill to always have something like 001, 010, 100

            if increment_files:
                d_nb = detect_number(increment_files[-1].split('.blend')[0])
                str_nb = str_nb.zfill(len(d_nb[2]))
                #print(d_nb, len(d_nb[2]))
            else:
                d_nb = False
                d_nb_filepath = detect_number(os.path.basename(f_path).split('.blend')[0])
                #if numbers: ## USELESS ??
                #    str_nb.zfill(3)
                if d_nb_filepath:
                    str_nb = str(int(d_nb_filepath[2]) + 1).zfill(len(d_nb_filepath[2]))

            # generating output file name
            if d_nb:
                if len(increment_files[-1].split('.blend')[0]) < d_nb[1]: # in case last_nb_index is just after filename's max index
                    output = bpy.path.abspath('//') + dir_name + increment_files[-1].split('.blend')[0][:d_nb[0]] + str_nb + '.blend'
                else:
                    output = bpy.path.abspath('//') + dir_name + increment_files[-1].split('.blend')[0][:d_nb[0]] + str_nb + increment_files[-1].split('.blend')[0][d_nb[1]:] + '.blend'
            else:
                if d_nb_filepath:
                    if len(os.path.basename(f_path).split('.blend')[0]) < d_nb_filepath[1]: # in case last_nb_index is just after filename's max index
                        output = bpy.path.abspath('//') + dir_name + os.path.basename(f_path).split('.blend')[0][:d_nb_filepath[0]] + str_nb + '.blend'
                    else:
                        output = bpy.path.abspath('//') + dir_name + os.path.basename(f_path).split('.blend')[0][:d_nb_filepath[0]] + str_nb + os.path.basename(f_path).split('.blend')[0][d_nb_filepath[1]:] + '.blend'
                else:
                    output = f_path.split(".blend")[0] + '_' + '001' + '.blend'

            if os.path.isfile(output):
                self.report({'WARNING'}, "Internal Error: trying to save over an existing file. Cancelled")
                print('Tested Output: ', output)
                return {'CANCELLED'}
            bpy.ops.wm.save_mainfile()
            bpy.ops.wm.save_as_mainfile(filepath=output, copy=True)
            
            self.report({'INFO'}, "File: {0} - Created at: {1}".format(output[len(bpy.path.abspath("//")):], output[:len(bpy.path.abspath("//"))]))
        else:
            self.report({'WARNING'}, "Please save a main file")
        return {'FINISHED'}
        ###### PENSER A TESTER AUTRES FICHIERS DU DOSSIER, VOIR SI TROU DANS NUMEROTATION==> WARNING

class AutoIncrementalSave(bpy.types.Operator):
    """  """
    bl_idname = "file.auto_save_incremental"
    bl_label = "Auto Save Incremental"
    
    def modal(self, context, event):
        #print(tm()-self.time)

        if context.user_preferences.addons[__name__].preferences.stop == True or event.type == 'ESC':
            print('STOP')
            return {'FINISHED'}

        if tm()-self.time >= context.user_preferences.addons[__name__].preferences.time_btw_save:
            print('Auto Saving...')
            bpy.ops.file.save_incremental()
            self.time = tm()

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        #context.user_preferences.addons[__name__].preferences.stop = True # kill any running instance

        context.user_preferences.addons[__name__].preferences.dir_path = context.user_preferences.addons[__name__].preferences.dir_path_user_defined + os.path.basename(bpy.data.filepath.split('.blend')[0]) + '/'   # to create a directory with base file name # change to prefs => access from all the code
        dir_path = os.path.dirname(bpy.data.filepath) + context.user_preferences.addons[__name__].preferences.dir_path # récupérer path de base + path du nouveau répertoire

        print()
        print('Creating directory and base file (copy of current file)...')

        print('Trying to create directory: ', dir_path)
        os.makedirs(dir_path, exist_ok=True)
        print('Directory created')

        bpy.ops.wm.save_as_mainfile(filepath= dir_path + bpy.path.basename(bpy.data.filepath).split('.blend')[0] + '_000' +  '.blend', copy= True)
        print('Base file created')

        context.user_preferences.addons[__name__].preferences.stop = False
        self.time = tm() 
        context.window_manager.modal_handler_add(self)
        print('Auto Incremental Saving started')
        print()
        return {'RUNNING_MODAL'}
        #self.report({'WARNING'}, "No active object, could not finish")
        #return {'CANCELLED'}

##############

def detect_number(name):
    last_nb_index = -1

    for i in range(1,len(name)):
        if name[-i].isnumeric():
            if last_nb_index == -1:
                last_nb_index = len(name)-i+1 # +1 because last index in [:] need to be 1 more
        elif last_nb_index != -1:
            first_nb_index = len(name)-i+1 #+1 to restore previous index
            return (first_nb_index,last_nb_index,name[first_nb_index:last_nb_index]) # first: index of the number / last: last number index +1
    return False

def draw_into_file_menu(self,context):
    self.layout.operator('file.auto_save_incremental', icon='SAVE_COPY')


def register():
    bpy.utils.register_class(FileIncrementalSave)
    bpy.types.INFO_MT_file.prepend(draw_into_file_menu)
    bpy.utils.register_class(AutoIncrementalSave)
    bpy.utils.register_class(AutoSaveIncrementalPreferencesPanel)


def unregister():
    bpy.utils.unregister_class(FileIncrementalSave)
    bpy.types.INFO_MT_file.remove(draw_into_file_menu)
    bpy.utils.unregister_class(AutoIncrementalSave)
    bpy.utils.unregister_class(AutoSaveIncrementalPreferencesPanel)


if __name__ == "__main__":
    register()
