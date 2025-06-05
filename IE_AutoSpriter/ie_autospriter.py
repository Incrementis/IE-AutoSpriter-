# Never Forget: Comments can "lie", but code not so much ;P
# Used source: https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#your-first-add-onimport bpy
from bpy.types import Panel
from bpy.types import PropertyGroup
import bpy

# --------
# Purpose:
# --------
# Contains Add-on information
# ---------------------------
bl_info = {
    "name": "IE AutoSpriter",
    "author": "Incrementis",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3d > Tool",
    "category": "Object",
    "warning": "",
    "wiki_url": "https://github.com/Incrementis/IE-AutoSpriter-",
    "category": "Render Animation"
}


# --------
# Purpose:
# --------
# Group of input types which will be added into the other panels
# --------------------------------------------------------------
class IEAS_Inputs(PropertyGroup):
    """Group of input types which will be added into the other panels"""
    
    # --- Step 1: Global Parameters
    Save_at: bpy.props.StringProperty(name="Save at")
    Prefix: bpy.props.StringProperty(name="Prefix")
    Resref: bpy.props.StringProperty(name="Resref")
    Every_X_frame: bpy.props.IntProperty(name="Every X Frame", default=1)


# --------
# Purpose:
# --------
# Manages and serves as main container for the other classes.
# -----------------------------------------------------------
class IEAS_PT_Core(Panel):
    # Use this as a tooltip for menu items and buttons.
    """Infinity Engine AutoSpriter is a Blender add-on that automates sprite creation from creature animations."""
    
     # --- Blender specific class variables
    bl_label        = "IE AutoSpriter"   # Visible name when category is opened
    bl_idname       = 'IEAS_PT_Core'     # Notice the ‘CATEGORY_PT_name’ Panel.bl_idname, this is a naming convention for panels.
    bl_space_type   = 'VIEW_3D'          # In which editor type Add-on should be appended to
    bl_region_type  = 'UI'               # The region where the panel is going to be used in
    bl_category     = bl_label           # Visible category tab name
    
    # --- Blender specific function which places elements into GUI
    def draw(self, context):
        pass


# --------
# Purpose:
# --------
# This step defines general settings that apply across the entire sprite rendering process.
# -----------------------------------------------------------------------------------------
class IEAS_PT_GlobalParameters(Panel):
    """This step defines general settings that apply across the entire sprite rendering process."""
    
    # --- Blender specific class variables
    bl_label        = "Step 1: Global Parameters" 
    bl_idname       = 'IEAS_PT_GlobalParameters'
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "IE AutoSpriter"
    bl_parent_id    = 'IEAS_PT_Core'
    bl_options      = {'DEFAULT_CLOSED'}
    
    # --- Blender specific function which places elements into GUI
    def draw(self, context):
        self.layout.prop(context.scene.IEAS_properties, "Save_at")
        self.layout.prop(context.scene.IEAS_properties, "Prefix")
        self.layout.prop(context.scene.IEAS_properties, "Resref")
        self.layout.prop(context.scene.IEAS_properties, "Every_X_frame")
        
        
      
def register():
    bpy.utils.register_class(IEAS_PT_Core)
    bpy.utils.register_class(IEAS_PT_GlobalParameters)
    bpy.utils.register_class(IEAS_Inputs)
    bpy.types.Scene.IEAS_properties = bpy.props.PointerProperty(type=IEAS_Inputs)
    


def unregister():
    bpy.utils.unregister_class(IEAS_PT_Core)
    bpy.utils.unregister_class(IEAS_PT_GlobalParameters)
    
    
if __name__ == "__main__":
    register()