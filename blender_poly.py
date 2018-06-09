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
from pathlib import Path

#breakpoint = bpy.types.bp.bp
__package__ = "blender_poly"
BLENDER_POLY_PATH = 'BlenderPoly'

preview_collections = {}
blender_poly_category_items = [
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
]

def enum_previews_from_model_previews_all(self, context):
    """EnumProperty callback"""
    if context is None:
        return []

    wm = context.window_manager
    preferences = context.user_preferences.addons[__package__].preferences
    props = context.window_manager.poly
    
    enum_items_all = []
    directory = Path(context.user_preferences.filepaths.temporary_directory).joinpath (BLENDER_POLY_PATH, props.category_type)

    filepath_list = list(Path(directory).glob('**/*'))
    
#    print(filepath_list)
    
    for filepath in filepath_list:
        comp_path = str(filepath.resolve())
        print (comp_path)
        pcoll = preview_collections[props.category_type]
        thumb = pcoll.load (comp_path, comp_path, 'IMAGE')
        enum_items_all.append((comp_path, props.category_type, comp_path, thumb.icon_id))
        
    return enum_items_all
    
def change_image_model_all(self,context):
    pass

class BlenderPolyUIPanel(bpy.types.Panel):
    """Creates a Panel in the material tab"""
    bl_label = "Blender Poly"
    bl_idname = "OBJECT_PT_blender_poly_previews"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        preferences = context.user_preferences.addons[__package__].preferences
        props = context.window_manager.poly
        
        row = layout.row()
        col = row.column()
        
        col.template_icon_view(props, "preview_icons", show_labels=False)
    
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
        items = blender_poly_category_items,
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
    preview_icons = bpy.props.EnumProperty(items = enum_previews_from_model_previews_all, update = change_image_model_all)
        
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

        tmp_path = Path (context.user_preferences.filepaths.temporary_directory).joinpath (BLENDER_POLY_PATH, props.category_type)

        print(tmp_path)
        
        if not tmp_path.exists ():
            tmp_path.mkdir (parents=True)
        
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
        
        json = r.json()

        if not 'assets' in json.keys ():
            return {'INTERFACE'}

        for asset in json['assets']:
            thumbnail_url = asset['thumbnail']['url']
            
            if not tmp_path.joinpath (asset['thumbnail']['relativePath']).exists ():
                thumbnail = requests.get(thumbnail_url)
            
                with tmp_path.joinpath (asset['thumbnail']['relativePath']).open (mode='wb') as f:
                    f.write (thumbnail.content)
        
#        print (r.text)
#        print (r.url)

        return {'FINISHED'}
        
def register():
    bpy.utils.register_class(BlenderPolyProps)
    bpy.utils.register_class(LayoutPolyPanel)
    bpy.utils.register_class(BlenderPolyAssets)
    bpy.utils.register_class(BlenderPolyPreferences)
    bpy.utils.register_class(BlenderPolyInstallAssets)
    bpy.utils.register_class(BlenderPolyUIPanel)
    
    bpy.types.WindowManager.poly = bpy.props.PointerProperty(type=BlenderPolyProps)
    bpy.types.WindowManager.poly_model_previews_all = bpy.props.EnumProperty(items=enum_previews_from_model_previews_all, update=change_image_model_all)

    for category in blender_poly_category_items:
        pcoll = bpy.utils.previews.new ()
        preview_collections [category[0]] = pcoll

def unregister():
    bpy.utils.unregister_class(BlenderPolyUIPanel)
    bpy.utils.unregister_class(BlenderPolyInstallAssets)
    bpy.utils.unregister_class(BlenderPolyPreferences)
    bpy.utils.unregister_class(BlenderPolyAssets)
    bpy.utils.unregister_class(LayoutPolyPanel)
    bpy.utils.unregister_class(BlenderPolyProps)

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    
    try:
        del bpy.types.WindowManager.poly_model_previews_all
        del bpy.types.WindowManager.poly
    except:
        pass
    
if __name__ == "__main__":
    register()
