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
import requests
import json

#breakpoint = bpy.types.bp.bp
__package__ = "blender_poly"

def enum_previews_from_model_previews_all(self, context):

    if context is None:
        return []

    wm = context.window_manager
    preferences = context.user_preferences.addons[__package__].preferences
    
    return []
    
def change_image_model_all(self,context):
    pass
    
class BlenderPolyPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    polyApiKey = bpy.props.StringProperty (
        name = "API Key",
        default = "",
        description = "Input the Poly's API Key",
        subtype = 'BYTE_STRING'
        )
           
    def draw(self, context):
        props = context.window_manager.poly
        layout = self.layout
        preferences = context.user_preferences.addons[__package__].preferences
        
        row = layout.row()
        row.prop(preferences, 'polyApiKey')
        
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
        items = [
#            ('featured', 'Featured', 'featured'),
#            ('uploads', 'Your Uploads', 'uploads'),
#            ('likes', 'Your Likes', 'likes'),
            ('animal', 'Animals and Creatures', 'animal'),
            ('architecture', 'Architecture', 'architecture'),
            ('art', 'Art', 'art'),
            ('food', 'Food and Drink', 'food'),
            ('nature', 'Nature', 'nature'),
            ('objects', 'Objects', 'objects'),
            ('people', 'People and Characters', 'people'),
            ('scenes', 'Places and Scenes', 'scenes'),
            ('technology', 'Technology', 'technology'),
            ('transport', 'Transport', 'transport')
        ],
        name = "Category Type",
        default = "animal")
    maxComplexity = bpy.props.EnumProperty(
        items = [
            ('COMPLEX', 'COMPLEX', 'COMPLEX'),
            ('MEDIUM', 'MEDIUM', 'MEDIUM'),
            ('SIMPLE', 'SIMPLE', 'SIMPLE')
        ],
        name = "Max Complexity",
        default = "COMPLEX")
    keywords = bpy.props.StringProperty(name = 'Keywords', description = 'Keywords')
    curated = bpy.props.BoolProperty(name = 'Curated', description = 'Curated')
    pageSize = bpy.props.IntProperty(name = 'Page size', description = 'Page size', default = 20, min = 1, max = 100)
    orderBy = bpy.props.EnumProperty(
        items = [('BEST', 'BEST', 'BEST'), ('NEWEST', 'NEWEST', 'NEWEST'), ('OLDEST', 'OLDEST', 'OLDEST')],
        name = 'Order by',
        default = 'BEST')
    pageToken = ''
        
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
        
        row = layout.row(align=True)
        row.prop(props, "category_type")
        
        row = layout.row(align=True)
        row.prop(props, "maxComplexity")

        row = layout.row(align=True)
        row.prop(props, "orderBy")

        row = layout.row(align=True)
        row.prop(props, "pageSize")
        
        row = layout.row(align=True)
        row.prop(props, "curated")
        
        row = layout.row(align=True)
        row.prop(props, "keywords")
        
        row = layout.row(align = True)
        row.scale_y = 2.0
        row.operator("render.render", text = "Load")

        row = layout.row(align=True)
        col = row.column()
        col.scale_y = 7
        col.operator("scene.previous_mat_item", icon = "TRIA_LEFT", text = "")

        col = row.column()
        col.scale_y = 1
        col.template_icon_view(wm, "poly_model_previews_all", show_labels = True)
#        col.label(matNameNew.title().replace("_", " "))
        
        col = row.column()
        col.scale_y = 7
        col.operator("scene.next_mat_item", icon = "TRIA_RIGHT", text = "")
        
        row = layout.row(align = True)
        row.scale_y = 2.0
        row.operator("blender_poly.test", text = "Test")

class BlenderPolyAssets(bpy.types.Operator):
    bl_idname = "blender_poly.test"
    bl_label = "Test Operator"
    
    def execute(self, context):
        url = "https://poly.googleapis.com/v1/assets"
        props = context.window_manager.poly
        preferences = context.user_preferences.addons[__package__].preferences
        payload = {'key': preferences.polyApiKey, 'format': 'OBJ',
            'category': props.category_type,
            'maxComplexity': props.maxComplexity,
            'curated': props.curated,
            'keywords': props.keywords,
            'pageSize': props.pageSize,
            'orderBy': props.orderBy,
#            'pageToken': props.pageToken
        }
        
        r = requests.get(url, params=payload)
        
        print (r.json())
        print (r.url)
            
        return {'FINISHED'}
        
def register():
    bpy.utils.register_class(BlenderPolyProps)
    bpy.utils.register_class(LayoutPolyPanel)
    bpy.utils.register_class(BlenderPolyAssets)
    bpy.utils.register_class(BlenderPolyPreferences)
    bpy.utils.register_class(BlenderPolyInstallAssets)
    
    bpy.types.WindowManager.poly = bpy.props.PointerProperty(type=BlenderPolyProps)
    bpy.types.WindowManager.poly_model_previews_all = bpy.props.EnumProperty(items=enum_previews_from_model_previews_all, update=change_image_model_all)

def unregister():
    bpy.utils.unregister_class(BlenderPolyInstallAssets)
    bpy.utils.unregister_class(BlenderPolyPreferences)
    bpy.utils.unregister_class(BlenderPolyAssets)
    bpy.utils.unregister_class(LayoutPolyPanel)
    bpy.utils.unregister_class(BlenderPolyProps)

    try:
        del bpy.types.WindowManager.poly_model_previews_all
        del bpy.types.WindowManager.poly
    except:
        pass
    
if __name__ == "__main__":
    register()
