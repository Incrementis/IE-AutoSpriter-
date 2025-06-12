# Never Forget: Comments can "lie", but code not so much ;P
# Used source: 
# https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#your-first-add-onimport bpy
# https://docs.blender.org/api/current/bpy.types.Operator.html
# https://developer.blender.org/docs/release_notes/2.80/python_api/addons/#Naming
# (PT = Panel Type)
# (OT = Operator Type)
# (PGT = Property Group Type)
from bpy.types import Panel
from bpy.types import PropertyGroup
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
import bpy

# --------
# Purpose:
# --------
# Contains Add-on information
# ---------------------------
bl_info = {
    "name": "IE AutoSpriter",
    "author": "Incrementis",
    "version": (0, 1, 2),
    "blender": (4, 0, 0),
    "location": "View3d > Tool",
    "support": "https://github.com/Incrementis/IE-AutoSpriter-",
    "category": "Object",
    "description": "Infinity Engine AutoSpriter is a Blender add-on that automates sprite creation from creature animations for IE games.",
    "warning": "",
    "wiki_url": "https://github.com/Incrementis/IE-AutoSpriter-",
    "tracker_url": "",
    "category": "Render Animation"
}


# --------
# Purpose:
# --------
# Group of input types which will be added into the other panels
# --------------------------------------------------------------
class IEAS_PGT_Inputs(PropertyGroup):
    """Group of input types which will be added into the other panels"""
    
    # --- Step 1: Global Parameters
    Save_at: bpy.props.StringProperty(name="Save at",subtype='FILE_PATH') # File-opener
    Prefix: bpy.props.StringProperty(name="Prefix")
    Resref: bpy.props.StringProperty(name="Resref")
    Every_X_Frame: bpy.props.IntProperty(name="Every X Frame", default=1, min=1)
    # --- Step 2: Shading Nodes
    Principle_BSDF: bpy.props.StringProperty(name="Principle BSDF", default="Principled BSDF")
    Material_Output: bpy.props.StringProperty(name="Material Output", default="Material Output")


# --------
# Purpose:
# --------
# Adds shading nodes which is used in "IEAS_PT_ShadingNodes" class
# ----------------------------------------------------------------
class IEAS_OT_ShadingNodes(Operator):
    """This class offers a function which adds shading nodes which then is used in "IEAS_PT_ShadingNodes" class."""
    bl_idname = "ieas.shading_nodes" # To be on the safe side, the follwoing naming "convention" is used <lower case>.<lower case>[_<lower case>]
    bl_label = "ADD"
    
    def execute(self, context):
        # Put your render property code here
        print("Hello World")
        return {'FINISHED'}


# --------
# Purpose:
# --------
# Manages and serves as main container for the other classes.
# -----------------------------------------------------------
class IEAS_PT_Core(Panel):
    # Use this as a tooltip for menu items and buttons. 
    """Infinity Engine AutoSpriter is a Blender add-on that automates sprite creation from creature animations."""
    
     # --- Blender specific class variables
    bl_label        = "IE AutoSpriter"   # Visible name when category is opened(title)
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
        # Instances by pointers
        self.layout.prop(context.scene.IEAS_properties, "Save_at")
        self.layout.prop(context.scene.IEAS_properties, "Prefix")
        self.layout.prop(context.scene.IEAS_properties, "Resref")
        self.layout.prop(context.scene.IEAS_properties, "Every_X_Frame")
        
 
# --------
# Purpose:
# --------
# This step allows for the addition of specific shaders to the material shading setup. 
# This is crucial for Infinity Engine sprites, which require indexed color palettes.
# ------------------------------------------------------------------------------------
class IEAS_PT_ShadingNodes(Panel):
    """This step defines general settings that apply across the entire sprite rendering process."""
    
    # --- Blender specific class variables
    bl_label        = "Step 2: Shading Nodes" 
    bl_idname       = 'IEAS_PT_ShadingNodes'
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "IE AutoSpriter"
    bl_parent_id    = 'IEAS_PT_Core'
    bl_options      = {'DEFAULT_CLOSED'}
    
    # --- Blender specific function which places elements into GUI
    def draw(self, context):
        # Instances by pointers
        self.layout.prop(context.scene.IEAS_properties, "Principle_BSDF")
        self.layout.prop(context.scene.IEAS_properties, "Material_Output")
        #TODO create button and execute buttons business logic.
        #self.layout.operator("mesh.primitive_cone_add",text="Add")
        col = self.layout.column(align=True)
        col.operator("ieas.shading_nodes")
        
 
 
        
      
def register():
    bpy.utils.register_class(IEAS_OT_ShadingNodes)
    bpy.utils.register_class(IEAS_PGT_Inputs)
    bpy.utils.register_class(IEAS_PT_Core)
    bpy.utils.register_class(IEAS_PT_GlobalParameters)
    bpy.utils.register_class(IEAS_PT_ShadingNodes)
    
    # Pointers
    bpy.types.Scene.IEAS_properties = bpy.props.PointerProperty(type=IEAS_PGT_Inputs)
    


def unregister():
    bpy.utils.unregister_class(IEAS_OT_ShadingNodes)
    bpy.utils.unregister_class(IEAS_PGT_Inputs)
    bpy.utils.unregister_class(IEAS_PT_Core)
    bpy.utils.unregister_class(IEAS_PT_GlobalParameters)
    bpy.utils.unregister_class(IEAS_PT_ShadingNodes)
    del bpy.types.Scene.IEAS_properties
    
    
if __name__ == "__main__":
    register()