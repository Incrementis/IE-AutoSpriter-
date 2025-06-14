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
import bpy


# --------
# Purpose:
# --------
# Contains Add-on information
# ---------------------------
bl_info = {
    "name": "IE AutoSpriter",
    "author": "Incrementis",
    "version": (0, 5, 0),
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
# Group of input types which will be added into the other sub/child panels
# ------------------------------------------------------------------------
class IEAS_PGT_Inputs(PropertyGroup):
    """Group of input types which will be added into the other panels"""
    
    # --- Step 1: Global Parameters
    Save_at:        bpy.props.StringProperty(name="Save at",subtype='FILE_PATH') # File-opener
    Prefix:         bpy.props.StringProperty(name="Prefix")
    Resref:         bpy.props.StringProperty(name="Resref")
    Every_X_Frame:  bpy.props.IntProperty(name="Every X Frame", default=1, min=1)
    # --- Step 2: Shading Nodes
    Principle_BSDF:     bpy.props.StringProperty(name="Principle BSDF", default="Principled BSDF")
    Material_Output:    bpy.props.StringProperty(name="Material Output", default="Material Output")
    # --- Step 3: Camera
    # Strings
    South:      bpy.props.StringProperty(name="Subfolder S", default="south")
    South_West: bpy.props.StringProperty(name="Subfolder SW", default="south_west")
    West:       bpy.props.StringProperty(name="Subfolder W", default="west")
    North_West: bpy.props.StringProperty(name="Subfolder NW", default="noth_west")
    North:      bpy.props.StringProperty(name="Subfolder N", default="north")
    North_East: bpy.props.StringProperty(name="Subfolder NE", default="north_east")
    East:       bpy.props.StringProperty(name="Subfolder E", default="east")
    South_East: bpy.props.StringProperty(name="Subfolder SE", default="south_east")
    # Bools
    Activate_S:     bpy.props.BoolProperty(name="Activate S", default=True)
    Activate_SW:    bpy.props.BoolProperty(name="Activate SW", default=True)
    Activate_W:     bpy.props.BoolProperty(name="Activate W", default=True)
    Activate_NW:    bpy.props.BoolProperty(name="Activate NW", default=True)
    Activate_N:     bpy.props.BoolProperty(name="Activate N", default=True)
    Activate_NE:    bpy.props.BoolProperty(name="Activate NE", default=True)
    Activate_E:     bpy.props.BoolProperty(name="Activate E", default=True)
    Activate_SE:    bpy.props.BoolProperty(name="Activate SE", default=True)
    # --- Step 4: Animation
    # Strings
    Attack1:    bpy.props.StringProperty(name="A1", default="slash")
    Attack2:    bpy.props.StringProperty(name="A2", default="stab")
    Attack3:    bpy.props.StringProperty(name="A3", default="strike")
    Attack4:    bpy.props.StringProperty(name="A4", default="throw")
    Cast:       bpy.props.StringProperty(name="CA", default="cast")
    Death:      bpy.props.StringProperty(name="DE", default="death")
    Get_Hit:    bpy.props.StringProperty(name="GH", default="get hit")
    Get_Up:     bpy.props.StringProperty(name="GU", default="Get up")
    Ready:      bpy.props.StringProperty(name="SC", default="Ready")
    Idle:       bpy.props.StringProperty(name="SD", default="idle")
    Sleep:      bpy.props.StringProperty(name="SL", default="sleep")
    Conjure:    bpy.props.StringProperty(name="SP", default="conjure")
    Dead:       bpy.props.StringProperty(name="TW", default="dead")
    Walk:       bpy.props.StringProperty(name="WK", default="walk")
    # Bools
    Activate_A1: bpy.props.BoolProperty(name="Activate A1", default=True)
    Activate_A2: bpy.props.BoolProperty(name="Activate A2", default=True)
    Activate_A3: bpy.props.BoolProperty(name="Activate A3", default=True)
    Activate_A4: bpy.props.BoolProperty(name="Activate A4", default=True)
    Activate_CA: bpy.props.BoolProperty(name="Activate CA", default=True)
    Activate_DE: bpy.props.BoolProperty(name="Activate DE", default=True)
    Activate_GH: bpy.props.BoolProperty(name="Activate GH", default=True)
    Activate_GU: bpy.props.BoolProperty(name="Activate GU", default=True)
    Activate_SC: bpy.props.BoolProperty(name="Activate SC", default=True)
    Activate_SD: bpy.props.BoolProperty(name="Activate SD", default=True)
    Activate_SL: bpy.props.BoolProperty(name="Activate SL", default=True)
    Activate_SP: bpy.props.BoolProperty(name="Activate SP", default=True)
    Activate_TW: bpy.props.BoolProperty(name="Activate TW", default=True)
    Activate_WK: bpy.props.BoolProperty(name="Activate WK", default=True)
    # --- Step 5: Render
    # Reserved/None


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
        print("Hello IEAS_OT_ShadingNodes")
        return {'FINISHED'}


# --------
# Purpose:
# --------
# Starts the rendering which is used in "IEAS_PT_Final" class
# -----------------------------------------------------------
class IEAS_OT_Final(Operator):
    """This class offers a function which starts the rendering which is used in "IEAS_PT_Final" class."""
    bl_idname = "ieas.final" # To be on the safe side, the follwoing naming "convention" is used <lower case>.<lower case>[_<lower case>]
    bl_label = "RENDER"
    
    def execute(self, context):
        # Put your render property code here
        print("Hello IEAS_OT_Final")
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
        layout = self.layout
        # Instances by pointers
        layout.prop(context.scene.IEAS_properties, "Principle_BSDF")
        layout.prop(context.scene.IEAS_properties, "Material_Output")
        col = layout.column(align=True)
        col.operator("ieas.shading_nodes") # selfdefined button functionality
        
 
# --------
# Purpose:
# --------
# This step manages the output folders and defines which camera orientations will be rendered.
# --------------------------------------------------------------------------------------------
class IEAS_PT_Camera(Panel):
    """This step manages the output folders and defines which camera orientations will be rendered."""
    
    # --- Blender specific class variables
    bl_label        = "Step 3: Camera" 
    bl_idname       = 'IEAS_PT_Camera'
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "IE AutoSpriter"
    bl_parent_id    = 'IEAS_PT_Core'
    bl_options      = {'DEFAULT_CLOSED'}
    # --- Blender specific function which places elements into GUI
    def draw(self, context):        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "South")
        row.prop(context.scene.IEAS_properties, "Activate_S")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "South_West")
        row.prop(context.scene.IEAS_properties, "Activate_SW")
               
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "West")
        row.prop(context.scene.IEAS_properties, "Activate_W")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "North_West")
        row.prop(context.scene.IEAS_properties, "Activate_NW")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "North")
        row.prop(context.scene.IEAS_properties, "Activate_N")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "North_East")
        row.prop(context.scene.IEAS_properties, "Activate_NE")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "East")
        row.prop(context.scene.IEAS_properties, "Activate_E")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "South_East")
        row.prop(context.scene.IEAS_properties, "Activate_SE")      


# --------
# Purpose:
# --------
# This step defines which animations (Blender Actions) should be rendered and how they are named in the output.
# -------------------------------------------------------------------------------------------------------------
class IEAS_PT_Animation(Panel):
    """This step defines which animations (Blender Actions) should be rendered and how they are named in the output."""
    
    # --- Blender specific class variables
    bl_label        = "Step 4: Animation" 
    bl_idname       = 'IEAS_PT_Animation'
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "IE AutoSpriter"
    bl_parent_id    = 'IEAS_PT_Core'
    bl_options      = {'DEFAULT_CLOSED'}
    # --- Blender specific function which places elements into GUI
    def draw(self, context):      
        pass
          
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Attack1")
        row.prop(context.scene.IEAS_properties, "Activate_A1")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Attack2")
        row.prop(context.scene.IEAS_properties, "Activate_A2") 
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Attack3")
        row.prop(context.scene.IEAS_properties, "Activate_A3")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Attack1")
        row.prop(context.scene.IEAS_properties, "Activate_A4")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Cast")
        row.prop(context.scene.IEAS_properties, "Activate_CA")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Death")
        row.prop(context.scene.IEAS_properties, "Activate_DE")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Get_Hit")
        row.prop(context.scene.IEAS_properties, "Activate_GH")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Get_Up")
        row.prop(context.scene.IEAS_properties, "Activate_GU")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Ready")
        row.prop(context.scene.IEAS_properties, "Activate_SC")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Idle")
        row.prop(context.scene.IEAS_properties, "Activate_SD")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Sleep")
        row.prop(context.scene.IEAS_properties, "Activate_SL")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Conjure")
        row.prop(context.scene.IEAS_properties, "Activate_SP")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Dead")
        row.prop(context.scene.IEAS_properties, "Activate_TW")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Walk")
        row.prop(context.scene.IEAS_properties, "Activate_WK")


# --------
# Purpose:
# --------
# Starts the rendering which is used in "IEAS_PT_Final" class
# -----------------------------------------------------------
class IEAS_PT_Final(Panel):
    """This step defines general settings that apply across the entire sprite rendering process."""
    
    # --- Blender specific class variables
    bl_label        = "Step 5: Final" 
    bl_idname       = 'IEAS_PT_Final'
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "IE AutoSpriter"
    bl_parent_id    = 'IEAS_PT_Core'
    bl_options      = {'DEFAULT_CLOSED'}
    
    # --- Blender specific function which places elements into GUI
    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("ieas.final") # selfdefined button functionality
 
               
# --------
# Purpose:
# --------      
# This makes it possible to activate the classes for the concrete usage in blender's environment.
# This is also needed for regitering the code as add-on.
def register():
    bpy.utils.register_class(IEAS_OT_ShadingNodes)
    bpy.utils.register_class(IEAS_OT_Final)
    bpy.utils.register_class(IEAS_PGT_Inputs)
    bpy.utils.register_class(IEAS_PT_Core)
    bpy.utils.register_class(IEAS_PT_GlobalParameters)
    bpy.utils.register_class(IEAS_PT_ShadingNodes)
    bpy.utils.register_class(IEAS_PT_Camera)
    bpy.utils.register_class(IEAS_PT_Animation)
    bpy.utils.register_class(IEAS_PT_Final)
    
    # Pointers
    bpy.types.Scene.IEAS_properties = bpy.props.PointerProperty(type=IEAS_PGT_Inputs)
    

# --------
# Purpose:
# --------
# Cleanup(When Addo-on is disabled)!
def unregister():
    bpy.utils.unregister_class(IEAS_OT_ShadingNodes)
    bpy.utils.register_class(IEAS_OT_Final)
    bpy.utils.unregister_class(IEAS_PGT_Inputs)
    bpy.utils.unregister_class(IEAS_PT_Core)
    bpy.utils.unregister_class(IEAS_PT_GlobalParameters)
    bpy.utils.unregister_class(IEAS_PT_ShadingNodes)
    bpy.utils.unregister_class(IEAS_PT_Camera)
    bpy.utils.unregister_class(IEAS_PT_Animation)
    bpy.utils.unregister_class(IEAS_PT_Final)
    del bpy.types.Scene.IEAS_properties
    

# --------
# Purpose:
# --------   
# Code execution control!  
if __name__ == "__main__":
    register()