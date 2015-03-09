######################################################################################################
# A tool that makes opening/closing window faster and easier                                         #
# Actualy partly uncommented - if you do not understand some parts of the code,                      #
# please see further version or contact me                                                           #
# Author: Lapineige                                                                                  #
# License: GPL v3                                                                                    #
######################################################################################################


############# Add-on description (used by Blender)

bl_info = {
    "name": "Tweak Area",
    "description": 'A tool that makes opening/closing window faster and easier  ',
    "author": "Lapineige",
    "version": (1, 0),
    "blender": (2, 71, 0),
    "location": "Shortcut (default Mouse Button 5)",
    "warning": "",
    "wiki_url": "https://www.youtube.com/watch?v=CTPsqHxmrgM&list=UUNhIgErK9OY3XzhEoRS_j7Q",
    "tracker_url": "http://le-terrier-de-lapineige.over-blog.com/contact",
    "category": "Scene"}

##############

import bpy
        
########################
###### Preferences Panel
class TweakAreaPreferencePanel(bpy.types.AddonPreferences):
    """ Create a configuration panel in the preferences """
    bl_idname = __name__
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        wm = bpy.context.window_manager
        row.prop(wm.keyconfigs.addon.keymaps['Window'].keymap_items[TweakArea.bl_idname], "map_type")
        row.prop(wm.keyconfigs.addon.keymaps['Window'].keymap_items[TweakArea.bl_idname], "type", full_event=True)
        return {'FINISHED'}
    
########################
###### Tweak Area

class TweakArea(bpy.types.Operator):
    """ Join the current area with the selected (by clicking) """
    bl_idname = "wm.tweak_area"
    bl_label = "Tweak Area"

    @classmethod
    def poll(cls, context):
        return True

    min_x = bpy.props.IntProperty()
    min_y = bpy.props.IntProperty()

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            self.max_x = event.mouse_x
            self.max_y = event.mouse_y
            if bpy.ops.screen.area_join(min_x=self.min_x, min_y=self.min_y, max_x=self.max_x, max_y=self.max_y) == {'CANCELLED'}:
                if (min(self.min_x,self.max_x) >= context.area.x) and (min(self.min_y,self.max_y) >= context.area.y) and (max(self.min_x,self.max_x) <= (context.area.x + context.area.width)) and (max(self.min_y,self.max_y) <= (context.area.y + context.area.height)):
                    if abs(self.min_x - self.max_x) > abs(self.min_y - self.max_y):
                        bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5, mouse_x=self.min_x, mouse_y=self.min_y)
                    elif abs(self.min_x - self.max_x) < abs(self.min_y - self.max_y):
                        bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.5, mouse_x=self.min_x, mouse_y=self.min_y)
                else:
                    self.report({'INFO'}, "Areas selected can't be merged together")
            bpy.ops.screen.header_toggle_menus()
            bpy.ops.screen.header_toggle_menus()
            return {'FINISHED'}
        if event.type == 'RIGHTMOUSE' or event.type == 'ESC':
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.min_x = event.mouse_x
        self.min_y = event.mouse_y
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


###################### Registration of all Operators, Panels and Shortcuts

def register():
    bpy.utils.register_class(TweakAreaPreferencePanel)

    bpy.utils.register_class(TweakArea)
    # keymap
    wm = bpy.context.window_manager
    sc = wm.keyconfigs.addon.keymaps['Window'].keymap_items.new(TweakArea.bl_idname, 'BUTTON5MOUSE', 'PRESS')

###################### Unregistration of all Operators, Panels and Shortcuts
    
def unregister():
    bpy.utils.unregister_class(TweakAreaPreferencePanel)

    # keymap
    wm = bpy.context.window_manager
    wm.keyconfigs.addon.keymaps['Window'].keymap_items.remove(wm.keyconfigs.addon.keymaps['Window'].keymap_items[JoinArea.bl_idname])
    bpy.utils.unregister_class(TweakArea)
    
if __name__ == '__main__':
    register()
