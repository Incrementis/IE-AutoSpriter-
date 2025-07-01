# Never Forget: Comments can "lie", but code not so much ;P
# Used source: 
# https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#your-first-add-onimport bpy
# https://docs.blender.org/api/current/bpy.types.Operator.html
# https://developer.blender.org/docs/release_notes/2.80/python_api/addons/#Naming
# https://docs.blender.org/api/current/bpy.props.html#bpy.props.PointerProperty
# https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.select_all
# https://docs.blender.org/api/current/bpy.ops.render.html#bpy.ops.render.render
# (PT   = Panel Type)
# (OT   = Operator Type)
# (PGT  = Property Group Type)
from bpy.types import Panel
from bpy.types import PropertyGroup
from bpy.types import Operator
import bpy
import os
import math


# --------
# Purpose:
# --------
# Contains Add-on information
# ---------------------------
bl_info = {
    "name": "IE AutoSpriter",
    "author": "Incrementis",
    "version": (0, 7, 0),
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
    Object_List:    bpy.props.PointerProperty(
                                                type=bpy.types.Object,
                                                name="Object List", # Label for the UI element
                                                description="Select the armature to be used to apply rendering." # Tooltip
                                                )
    Resolution_X:   bpy.props.IntProperty(name="Resolution X",default=256, min=1)
    Resolution_Y:   bpy.props.IntProperty(name="Resolution Y",default=256, min=1)
    Every_X_Frame:  bpy.props.IntProperty(name="Every X Frame", default=1, min=1)
    # --- Step 2: Shading Nodes
    Principled_BSDF:    bpy.props.StringProperty(name="Principle BSDF", default="Principled BSDF")
    Material_Output:    bpy.props.StringProperty(name="Material Output", default="Material Output")
    Material_List:      bpy.props.PointerProperty(
                                                    type=bpy.types.Material,# Crucially, specify the type of data block it points to
                                                    name="Material List", # Label for the UI element
                                                    description="Select the material to be used to apply shading nodes." # Tooltip
                                                    )
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
    Use_S:     bpy.props.BoolProperty(name="Use S", default=True)
    Use_SW:    bpy.props.BoolProperty(name="Use SW", default=True)
    Use_W:     bpy.props.BoolProperty(name="Use W", default=True)
    Use_NW:    bpy.props.BoolProperty(name="Use NW", default=True)
    Use_N:     bpy.props.BoolProperty(name="Use N", default=True)
    Use_NE:    bpy.props.BoolProperty(name="Use NE", default=True)
    Use_E:     bpy.props.BoolProperty(name="Use E", default=True)
    Use_SE:    bpy.props.BoolProperty(name="Use SE", default=True)
    # --- Step 4: Animation
    # Strings
    Attack1:    bpy.props.StringProperty(name="A1", default="slash")
    Attack2:    bpy.props.StringProperty(name="A2", default="stab")
    Attack3:    bpy.props.StringProperty(name="A3", default="strike")
    Attack4:    bpy.props.StringProperty(name="A4", default="throw")
    Cast:       bpy.props.StringProperty(name="CA", default="cast")
    Death:      bpy.props.StringProperty(name="DE", default="death")
    Get_Hit:    bpy.props.StringProperty(name="GH", default="get hit")
    Get_Up:     bpy.props.StringProperty(name="GU", default="get up")
    Ready:      bpy.props.StringProperty(name="SC", default="ready")
    Idle:       bpy.props.StringProperty(name="SD", default="idle")
    Sleep:      bpy.props.StringProperty(name="SL", default="sleep")
    Conjure:    bpy.props.StringProperty(name="SP", default="conjure")
    Dead:       bpy.props.StringProperty(name="TW", default="dead")
    Walk:       bpy.props.StringProperty(name="WK", default="walk")
    # Bools
    Use_A1: bpy.props.BoolProperty(name="Use A1", default=True)
    Use_A2: bpy.props.BoolProperty(name="Use A2", default=True)
    Use_A3: bpy.props.BoolProperty(name="Use A3", default=True)
    Use_A4: bpy.props.BoolProperty(name="Use A4", default=True)
    Use_CA: bpy.props.BoolProperty(name="Use CA", default=True)
    Use_DE: bpy.props.BoolProperty(name="Use DE", default=True)
    Use_GH: bpy.props.BoolProperty(name="Use GH", default=True)
    Use_GU: bpy.props.BoolProperty(name="Use GU", default=True)
    Use_SC: bpy.props.BoolProperty(name="Use SC", default=True)
    Use_SD: bpy.props.BoolProperty(name="Use SD", default=True)
    Use_SL: bpy.props.BoolProperty(name="Use SL", default=True)
    Use_SP: bpy.props.BoolProperty(name="Use SP", default=True)
    Use_TW: bpy.props.BoolProperty(name="Use TW", default=True)
    Use_WK: bpy.props.BoolProperty(name="Use WK", default=True)
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
    
    # Blender specific function which is executed in this case when ADD button is pressed
    def execute(self, context):
        
        materialName    = context.scene.IEAS_properties.Material_List.name
        activeMaterial  = bpy.data.materials[materialName]
        # Activates nodes for specific mesh material(See toggle button "Use Nodes" in "Shading" screen)
        use_nodes = bpy.data.materials[materialName].use_nodes
        
        # The materials "use nodes" will set to true, so adding new nodes is possible. 
        if(use_nodes==False):
            use_nodes = True
        
        # Gets the user given string inputs(see Step 2) and stores them into variables.
        Principled_BSDF_name = context.scene.IEAS_properties.Principled_BSDF
        Material_Output_name = context.scene.IEAS_properties.Material_Output
        
        # Gets the node types "ShaderNodeBsdfPrincipled" and "ShaderNodeOutputMaterial" depending on their name 
        Principled_BSDF = activeMaterial.node_tree.nodes.get(Principled_BSDF_name)
        Material_Output = activeMaterial.node_tree.nodes.get(Material_Output_name)
        
        # Creates the new nodes and positions them  near "Principled BSDF" node.
        MixShader_node = activeMaterial.node_tree.nodes.new('ShaderNodeMixShader')
        MixShader_node.location = (Principled_BSDF.location[0]+250,-100)
        BrightContrast_node = activeMaterial.node_tree.nodes.new('ShaderNodeBrightContrast')
        BrightContrast_node.location = (Principled_BSDF.location[0],-100)
        
        # Connects nodes
        activeMaterial.node_tree.links.new(Principled_BSDF.outputs[0],MixShader_node.inputs[1])
        activeMaterial.node_tree.links.new(MixShader_node.outputs[0],Material_Output.inputs[0])
        activeMaterial.node_tree.links.new(BrightContrast_node.outputs[0],MixShader_node.inputs[2])
        
        # Legit Default values of the nodes is needed(Check TheArtisan's manual)
        MixShader_node.inputs[0].default_value       = 0.010
        BrightContrast_node.inputs[1].default_value  = 1.000
        
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
    
    # Blender specific function which is executed in this case when RENDER button is pressed
    # TODO: Cleanup/refactor function
    def execute(self, context):
        # Put your render property code here
        print("--------IEAS_OT_Final----------")
        
        pathSaveAt = context.scene.IEAS_properties.Save_at
        # TODO: Delte print
        print("pathSaveAt:",pathSaveAt)
        
        # Just to make sure that the path is formated es expected
        # (maybe this is not needed,but the "icon viewer" prints a different output than the "Toggle System Console")
        # Also preventing relative path (user given)
        pathSaveAt = os.path.abspath(pathSaveAt)
        # TODO: Delte print
        print("pathSaveAt:",pathSaveAt)
        
        prefixResref = context.scene.IEAS_properties.Prefix + context.scene.IEAS_properties.Resref
        # TODO: Delte print
        print("prefixResref:",prefixResref)
        
        #selected_objects = bpy.context.selected_objects
        # TODO: Delte print
        #print("selected_objects",selected_objects)
        
        # deselect all in scene(preventing a second unintended rendering by the user)
        bpy.ops.object.select_all(action='DESELECT') 
        
        #TODO: Loop through all the stored objects
        # TODO: Delte print
        print("Object List:",context.scene.IEAS_properties.Object_List.name)
        objectName = context.scene.IEAS_properties.Object_List.name
        # Selects the specific object.
        bpy.context.scene.objects[objectName].select_set(True)
        
        # ---- Camera
        cameraPosFolderNames = {
            'south': context.scene.IEAS_properties.South,  'south_west': context.scene.IEAS_properties.South_West,
            'west': context.scene.IEAS_properties.West,    'north_west': context.scene.IEAS_properties.North_West,
            'north': context.scene.IEAS_properties.North,  'north_east': context.scene.IEAS_properties.North_East,
            'east': context.scene.IEAS_properties.East,    'south_east': context.scene.IEAS_properties.South_East
        }
        cameraPosToggles = {
            'south': context.scene.IEAS_properties.Use_S,  'south_west': context.scene.IEAS_properties.Use_SW,
            'west': context.scene.IEAS_properties.Use_W,   'north_west': context.scene.IEAS_properties.Use_NW,
            'north': context.scene.IEAS_properties.Use_N,  'north_east': context.scene.IEAS_properties.Use_NE,
            'east': context.scene.IEAS_properties.Use_E,   'south_east': context.scene.IEAS_properties.Use_SE
        }
        cameraAngles = {
            'south': 0,  'south_west': 315,
            'west': 270,   'north_west': 225,
            'north': 180,  'north_east': 135,
            'east': 90,   'south_east': 45
        }
        # ----- Animation
        animationFolderNames = {
            'A1': context.scene.IEAS_properties.Attack1,    'A2': context.scene.IEAS_properties.Attack2,
            'A3': context.scene.IEAS_properties.Attack3,    'A4': context.scene.IEAS_properties.Attack4,
            'CA': context.scene.IEAS_properties.Cast,       'DE': context.scene.IEAS_properties.Death,
            'GH': context.scene.IEAS_properties.Get_Hit,    'GU': context.scene.IEAS_properties.Get_Up,
            'SC': context.scene.IEAS_properties.Ready,      'SD': context.scene.IEAS_properties.Idle,
            'SL': context.scene.IEAS_properties.Sleep,      'SP': context.scene.IEAS_properties.Conjure,
            'TW': context.scene.IEAS_properties.Dead,       'WK': context.scene.IEAS_properties.Walk,            
        }
        animationToggle = {
            'A1': context.scene.IEAS_properties.Use_A1,     'A2': context.scene.IEAS_properties.Use_A2,
            'A3': context.scene.IEAS_properties.Use_A3,     'A4': context.scene.IEAS_properties.Use_A4,
            'CA': context.scene.IEAS_properties.Use_CA,     'DE': context.scene.IEAS_properties.Use_DE,
            'GH': context.scene.IEAS_properties.Use_GH,     'GU': context.scene.IEAS_properties.Use_GU,
            'SC': context.scene.IEAS_properties.Use_SC,     'SD': context.scene.IEAS_properties.Use_SD,
            'SL': context.scene.IEAS_properties.Use_SL,     'SP': context.scene.IEAS_properties.Use_SP,
            'TW': context.scene.IEAS_properties.Use_TW,     'WK': context.scene.IEAS_properties.Use_WK,            
        }
        
        
#        # TODO: Delte print
#        for key, value in animationToggle.items():
#            print(f"{key}:{value}")
#        
#        # loop through the actions
#        for a in bpy.data.actions:
#            # TODO: Delte print
#            print("\na:",a.name)
            
        for animationKey, animation in animationFolderNames.items():
            # Gets the action and sets it as current action
            bpy.context.active_object.animation_data.action = bpy.data.actions.get(animation)
            currentAction = bpy.context.active_object.animation_data.action
            
            if(animationToggle[animationKey] == True and currentAction != None):
                # TODO: Delte print
                print("\nanimation:",animation)
                #assign the action
                bpy.context.active_object.animation_data.action = bpy.data.actions.get(animation)
                # TODO: Delte print
                print("action:",bpy.context.active_object.animation_data.action)
                # In this case there are no subframe(?!) animations, thus converted into integer.
                # Furtehrmore this prevents rendering empty frames.
                bpy.context.scene.frame_end = int(bpy.context.active_object.animation_data.action.frame_range[1])
                # TODO: Delte print
                print("\nFrame End:",bpy.context.scene.frame_end)
                # Sets path of the sprites and subfolders
                animation_folder = os.path.join(pathSaveAt, animation)
                if not os.path.exists(animation_folder):
                    os.makedirs(animation_folder)
                # Uses only the camerapostions which are selected.    
                for positionKey, position in cameraPosFolderNames.items():
                    if(cameraPosToggles[positionKey] == True):
                        # Create folder for specific angles
                        position_folder = os.path.join(animation_folder, positionKey)                  
                        if not os.path.exists(position_folder):
                            os.makedirs(position_folder)
                            
                    # The script is not explicitly rotating the camera for each of the 8 directions. 
                    # It's rotating the subject (the character/model) and relying on a static camera to capture it.
                    bpy.context.active_object.rotation_euler[2] = math.radians(cameraAngles[positionKey])
                    # TODO: Delte print
                    print("\nbpy.context.active_object.rotation_euler:",bpy.context.active_object.rotation_euler)
                    print("\nbpy.context.active_object.rotation_euler[2]:",bpy.context.active_object.rotation_euler[2])
            
            
                    frameStart      = bpy.context.scene.frame_start
                    frameEnd        = bpy.context.scene.frame_end
                    frameCurrent    = bpy.context.scene.frame_current
                    renderFrame     = bpy.ops.render.render
                    Every_X_Frame   = context.scene.IEAS_properties.Every_X_Frame
                    
                    #loop through and render frames.  Can set how "often" it renders.
                    for frame in range(frameStart,frameEnd,Every_X_Frame):
                        frameCurrent = frame
                        
                        # TODO: Delte print
                        print("position_folder:",position_folder)
                        
                        fileName = f"{prefixResref}{animationKey}_{positionKey}_{str(frameCurrent).zfill(5)}.png"
                         # TODO: Delte print
                        print("fileName:",fileName)
                        
                        bpy.context.scene.render.filepath = os.path.join(position_folder, fileName)
                         # TODO: Delte print
                        print("filepath:",bpy.context.scene.render.filepath)
                        
                        # TODO: Delte print
                        print("action:",bpy.context.active_object.animation_data.action)
                        
                        renderFrame(  False, # This is the 'undo' parameter     
                                      animation     =False, 
                                      write_still   =True) 
        
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
        self.layout.prop(context.scene.IEAS_properties, "Object_List")
        self.layout.prop(context.scene.IEAS_properties, "Resolution_X")
        self.layout.prop(context.scene.IEAS_properties, "Resolution_Y")
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
        layout.prop(context.scene.IEAS_properties, "Principled_BSDF")
        layout.prop(context.scene.IEAS_properties, "Material_Output")
        layout.prop(context.scene.IEAS_properties, "Material_List")
        col = layout.column()
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
        row.prop(context.scene.IEAS_properties, "Use_S")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "South_West")
        row.prop(context.scene.IEAS_properties, "Use_SW")
               
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "West")
        row.prop(context.scene.IEAS_properties, "Use_W")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "North_West")
        row.prop(context.scene.IEAS_properties, "Use_NW")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "North")
        row.prop(context.scene.IEAS_properties, "Use_N")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "North_East")
        row.prop(context.scene.IEAS_properties, "Use_NE")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "East")
        row.prop(context.scene.IEAS_properties, "Use_E")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "South_East")
        row.prop(context.scene.IEAS_properties, "Use_SE")      


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
        row.prop(context.scene.IEAS_properties, "Use_A1")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Attack2")
        row.prop(context.scene.IEAS_properties, "Use_A2") 
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Attack3")
        row.prop(context.scene.IEAS_properties, "Use_A3")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Attack4")
        row.prop(context.scene.IEAS_properties, "Use_A4")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Cast")
        row.prop(context.scene.IEAS_properties, "Use_CA")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Death")
        row.prop(context.scene.IEAS_properties, "Use_DE")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Get_Hit")
        row.prop(context.scene.IEAS_properties, "Use_GH")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Get_Up")
        row.prop(context.scene.IEAS_properties, "Use_GU")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Ready")
        row.prop(context.scene.IEAS_properties, "Use_SC")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Idle")
        row.prop(context.scene.IEAS_properties, "Use_SD")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Sleep")
        row.prop(context.scene.IEAS_properties, "Use_SL")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Conjure")
        row.prop(context.scene.IEAS_properties, "Use_SP")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Dead")
        row.prop(context.scene.IEAS_properties, "Use_TW")
        
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Walk")
        row.prop(context.scene.IEAS_properties, "Use_WK")


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
# This makes it possible to Use the classes for the concrete usage in blender's environment.
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