bl_info = {
    "name": "Blender Poly",
    "category": "Object",
    "author": "Yuichi Sato",
    "version": (0, 1),
    "blender": (2, 79, 0),
    "location": "Object Panel > Poly",
    "wiki_url": "https://github.com/satoyuichi/BlenderPoly",
}

import bpy

#breakpoint = bpy.types.bp.bp
__package__ = "blender_poly"

class BlenderPolyPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    def draw(self, context):
        props = context.window_manager.poly
        layout = self.layout
        preferences = context.user_preferences.addons[__package__].preferences
        
#        row = layout.row()
#        row.prop(preferences, 'installFolder')
        
        row = layout.row()
        row.prop(props, "api_key")
        
        row = layout.row()
        row.scale_y = 1.25
        row.operator("scene.poly_install_assets", icon='SAVE_PREFS')

class BlenderPolyInstallAssets(bpy.types.Operator):
    """Save the Blender Poly assets filepath"""
    bl_idname = "scene.poly_install_assets"
    bl_label = "Save Settings"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.save_userpref()

        return {'FINISHED'}
    
class BlenderPolyProps(bpy.types.PropertyGroup):
    category_type = bpy.props.EnumProperty(
        items = [('featured', 'Featured', 'featured'),
            ('uploads', 'Your Uploads', 'uploads'),
            ('likes', 'Your Likes', 'likes'),
            ('animal', 'Animals and Creatures', 'animal'),
            ('architecture', 'Architecture', 'architecture'),
            ('art', 'Art', 'art'),
            ('food', 'Food and Drink', 'food'),
            ('nature', 'Nature', 'nature'),
            ('objects', 'Objects', 'objects'),
            ('people', 'People and Characters', 'people'),
            ('place', 'Places and Scenes', 'place'),
            ('technology', 'Technology', 'technology'),
            ('transport', 'Transport', 'transport')
        ],
        name = "Category Type",
        default = "featured")
    api_key = bpy.props.StringProperty(
        name = "API Key")
        
class LayoutPolyPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Poly"
    bl_idname = "OBJECT_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        props = context.window_manager.poly
        
        layout = self.layout
        wm = context.window_manager

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Aligned Row:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")

        # Different sizes in a row
        layout.label(text="Different button sizes:")
        row = layout.row(align=True)
        row.operator("render.render")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")

        row.operator("render.render")
        
        row = layout.row(align=True)
        row.prop(props, "category_type")
        
        row = layout.row(align=True)
        col = row.column()
        col.scale_y = 7
        
        col.operator("scene.previous_mat_item", icon = "TRIA_LEFT", text = "")
        col = row.column()
        col.scale_y = 1
        col.template_icon_view(wm, "my_mat_previews_all", show_labels = True)
#        col.label(matNameNew.title().replace("_", " "))
        
        col = row.column()
        col.scale_y = 7
        col.operator("scene.next_mat_item", icon = "TRIA_RIGHT", text = "")
        
        row = layout.row(align = True)
        row.scale_y = 2.0
        row.operator("render.render", text = "Load")

#class BlenderPolyAssets(bpy.types.Operator):
#    pass
        
def register():
    bpy.utils.register_class(BlenderPolyProps)
    bpy.utils.register_class(LayoutPolyPanel)
#    bpy.utils.register_class(BlenderPolyAssets)
    bpy.utils.register_class(BlenderPolyPreferences)
    bpy.utils.register_class(BlenderPolyInstallAssets)
    
    bpy.types.WindowManager.poly = bpy.props.PointerProperty(type=BlenderPolyProps)

def unregister():
    bpy.utils.unregister_class(BlenderPolyInstallAssets)
    bpy.utils.unregister_class(BlenderPolyPreferences)
#    bpy.utils.unregister_class(BlenderPolyAssets)
    bpy.utils.unregister_class(LayoutPolyPanel)
    bpy.utils.unregister_class(BlenderPolyProps)

    try:
        del bpy.types.WindowManager.poly
    except:
        pass
    
if __name__ == "__main__":
    register()
