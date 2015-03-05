######################################################################################################
# Add some options in 3D View > Properties > Shading to display wire for all objects                 #
# Actualy partly uncommented - if you do not understand some parts of the code,                      #
# please see further version or contact me.                                                          #
# Author: Lapineige                                                                                  #
# License: GPL v3                                                                                    #
######################################################################################################

import bpy

bpy.types.Scene.WT_only_selection = bpy.props.BoolProperty(name="Only Selection")
bpy.types.Scene.WT_invert = bpy.props.BoolProperty(name="Invert")
   
class HideAllWire(bpy.types.Operator):
    """ Hide object's wire and edges"""
    bl_idname = "object.hide_all_wire"
    bl_label = "Hide Wire And Edges"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for obj in bpy.data.objects:
            if (not context.scene.WT_only_selection)  or  (obj.select and context.scene.WT_only_selection and not context.scene.WT_invert)  or  ((context.scene.WT_invert and context.scene.WT_only_selection) and not obj.select):
                if hasattr(obj,"show_wire"):
                    obj.show_wire,obj.show_all_edges = False,False
                    
        return {'FINISHED'}

class DrawWireEdges(bpy.types.Operator):
    """Display the object's wire (all edges)"""
    bl_idname = "object.draw_wire_and_edges"
    bl_label = "Draw Wires and Edges"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for obj in bpy.data.objects:
            if (not context.scene.WT_only_selection)  or  (obj.select and context.scene.WT_only_selection and not context.scene.WT_invert)  or  ((context.scene.WT_invert and context.scene.WT_only_selection) and not obj.select):
                if hasattr(obj,"show_wire"):
                    obj.show_wire,obj.show_all_edges = True,True
        return {'FINISHED'}
    
class DrawOnlyWire(bpy.types.Operator):
    """Display the object's wire"""
    bl_idname = "object.draw_only_wire"
    bl_label = "Draw Only Wire"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for obj in bpy.data.objects:
            if (not context.scene.WT_only_selection)  or  (obj.select and context.scene.WT_only_selection and not context.scene.WT_invert)  or  ((context.scene.WT_invert and context.scene.WT_only_selection) and not obj.select):
                if hasattr(obj,"show_wire"):
                    obj.show_wire,obj.show_all_edges = True,False
        return {'FINISHED'}

def shading_wire_tools_layout(self,context):
    layout = self.layout
    
    split = layout.split(percentage=.75, align=True)
    split.prop(context.scene,"WT_only_selection", toggle=True, icon="BORDER_RECT")
    split.prop(context.scene,"WT_invert",toggle=True)
    
    col = layout.column(align=True)
    col.operator("object.draw_wire_and_edges", icon="WIRE", text="Wire + Edges")
    col.operator("object.draw_only_wire", icon="SOLID", text="Wire")
    col.operator("object.hide_all_wire", icon="RESTRICT_VIEW_ON", text="Hide All")

def register():
    bpy.utils.register_class(DrawWireEdges)
    bpy.utils.register_class(DrawOnlyWire)
    bpy.utils.register_class(HideAllWire)
    bpy.types.VIEW3D_PT_view3d_shading.append(shading_wire_tools_layout)


def unregister():
    bpy.types.VIEW3D_PT_view3d_shading.remove(shading_wire_tools_layout)
    bpy.utils.unregister_class(DrawWireEdges)
    bpy.utils.unregister_class(DrawOnlyWire)
    bpy.utils.unregister_class(HideAllWire)

if __name__ == "__main__":
    register()
