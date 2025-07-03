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
import time


# --------
# Purpose:
# --------
# Contains Add-on metadata and registration information for Blender.
# ------------------------------------------------------------------
bl_info = {
    "name": "IE AutoSpriter",
    "author": "Incrementis",
    "version": (0, 7, 7),
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
# Defines a PropertyGroup to hold all custom properties (settings and inputs) for the add-on's UI.
# These properties are accessible via `context.scene.IEAS_properties`.
# ------------------------------------------------------------------------------------------------
class IEAS_PGT_Inputs(PropertyGroup):
    """Group of input types which will be added into the other panels"""
    
    # --- Step 1: Global Parameters
    # File path property for saving rendered sprites.
    Save_at:        bpy.props.StringProperty(name="Save at",subtype='FILE_PATH') # File-opener
    # String property for the file prefix.
    Prefix:         bpy.props.StringProperty(name="Prefix")
    # String property for the resource reference (resref).
    Resref:         bpy.props.StringProperty(name="Resref")
    # Pointer to a Blender object, typically the armature for animation.
    Object_List:    bpy.props.PointerProperty(
                                                type=bpy.types.Object,
                                                name="Object List", # Label for the UI element
                                                description="Select the armature to be used to apply rendering." # Tooltip
                                                )
    # Integer property for the render resolution in X-dimension.
    Resolution_X:   bpy.props.IntProperty(name="Resolution X",default=256, min=1)
    # Integer property for the render resolution in Y-dimension.
    Resolution_Y:   bpy.props.IntProperty(name="Resolution Y",default=256, min=1)
    # Integer property to control rendering frequency (e.g., render every X frames).
    Every_X_Frame:  bpy.props.IntProperty(name="Every X Frame", default=1, min=1)
    # --- Step 2: Shading Nodes
    # String property for the name of the Principled BSDF node.
    Principled_BSDF:    bpy.props.StringProperty(name="Principle BSDF", default="Principled BSDF")
    # String property for the name of the Material Output node.
    Material_Output:    bpy.props.StringProperty(name="Material Output", default="Material Output")
    # Pointer to a Blender Material, used for applying shading nodes.
    Material_List:      bpy.props.PointerProperty(
                                                    type=bpy.types.Material,# Crucially, specify the type of data block it points to
                                                    name="Material List", # Label for the UI element
                                                    description="Select the material to be used to apply shading nodes." # Tooltip
                                                    )
                                                    
    # --- Step 3: Camera (Subfolder Names and Toggles for each direction)
    South:      bpy.props.StringProperty(name="Subfolder S", default="south")
    South_West: bpy.props.StringProperty(name="Subfolder SW", default="south_west")
    West:       bpy.props.StringProperty(name="Subfolder W", default="west")
    North_West: bpy.props.StringProperty(name="Subfolder NW", default="noth_west")
    North:      bpy.props.StringProperty(name="Subfolder N", default="north")
    North_East: bpy.props.StringProperty(name="Subfolder NE", default="north_east")
    East:       bpy.props.StringProperty(name="Subfolder E", default="east")
    South_East: bpy.props.StringProperty(name="Subfolder SE", default="south_east")
    # Boolean toggles for rendering each camera direction.
    Use_S:     bpy.props.BoolProperty(name="Use S", default=True)
    Use_SW:    bpy.props.BoolProperty(name="Use SW", default=True)
    Use_W:     bpy.props.BoolProperty(name="Use W", default=True)
    Use_NW:    bpy.props.BoolProperty(name="Use NW", default=True)
    Use_N:     bpy.props.BoolProperty(name="Use N", default=True)
    Use_NE:    bpy.props.BoolProperty(name="Use NE", default=True)
    Use_E:     bpy.props.BoolProperty(name="Use E", default=True)
    Use_SE:    bpy.props.BoolProperty(name="Use SE", default=True)
    
    # --- Step 4: Animation (Animation Names and Toggles)
    # String properties for names of various animation actions.
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
    # Boolean toggles for rendering each animation.
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
# Operator to add necessary shading nodes to the selected material for sprite rendering.
# This prepares the material for indexed color palettes required by Infinity Engine games.
# ----------------------------------------------------------------------------------------
class IEAS_OT_ShadingNodes(Operator):
    """This class offers a function which adds shading nodes which then is used in "IEAS_PT_ShadingNodes" class."""
    bl_idname = "ieas.shading_nodes" # Unique identifier for the operator. Naming convention(??): <lower_case>.<lower_case>[_<lower_case>]
    bl_label = "ADD" # Text displayed on the button in the UI.
    
    # Blender specific function which is executed in this case when ADD button is pressed
    def execute(self, context):
        
        materialName    = context.scene.IEAS_properties.Material_List.name
        activeMaterial  = bpy.data.materials[materialName]
        # Activates nodes for specific mesh material(See toggle button "Use Nodes" in "Shading" screen)
        use_nodes = bpy.data.materials[materialName].use_nodes
        
        # Enable material nodes if they are not already active.
        if(use_nodes==False):
            use_nodes = True
        
        # Gets the user given string inputs (node names) and stores them into variables.
        Principled_BSDF_name = context.scene.IEAS_properties.Principled_BSDF
        Material_Output_name = context.scene.IEAS_properties.Material_Output
        
        # Retrieves existing nodes by their names from the active material's node tree.
        Principled_BSDF = activeMaterial.node_tree.nodes.get(Principled_BSDF_name)
        Material_Output = activeMaterial.node_tree.nodes.get(Material_Output_name)
        
        # Creates the new nodes (Mix Shader and Bright/Contrast) and positions them near the Principled BSDF node.
        MixShader_node = activeMaterial.node_tree.nodes.new('ShaderNodeMixShader')
        MixShader_node.location = (Principled_BSDF.location[0]+250,-100)
        BrightContrast_node = activeMaterial.node_tree.nodes.new('ShaderNodeBrightContrast')
        BrightContrast_node.location = (Principled_BSDF.location[0],-100)
        
        # Connects the newly created nodes and existing nodes to form the desired shader graph.
        activeMaterial.node_tree.links.new(Principled_BSDF.outputs[0],MixShader_node.inputs[1])
        activeMaterial.node_tree.links.new(MixShader_node.outputs[0],Material_Output.inputs[0])
        activeMaterial.node_tree.links.new(BrightContrast_node.outputs[0],MixShader_node.inputs[2])
        
        # Sets default values for the new nodes' inputs, based on typical(??) IE sprite requirements.
        MixShader_node.inputs[0].default_value       = 0.010
        BrightContrast_node.inputs[1].default_value  = 1.000
        
        return {'FINISHED'}


# --------
# Purpose:
# --------
# Operator to initiate the full sprite rendering process for selected objects, animations, and directions.
# --------------------------------------------------------------------------------------------------------
class IEAS_OT_Final(Operator):
    """This class offers a function which starts the rendering which is used in "IEAS_PT_Final" class."""
    bl_idname = "ieas.final" # T# Unique identifier for the operator. Naming convention(??): <lower_case>.<lower_case>[_<lower_case>]
    bl_label = "RENDER" # Text displayed on the button in the UI.
    
    # Blender specific function which is executed in this case when RENDER button is pressed
    def execute(self, context):
        # ---- Start timer
        startTimer = time.time()    
        # ---- Camera
        # Dictionaries mapping internal keys to user-defined subfolder names and toggle states for camera angles.
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
        # Dictionary mapping internal keys to rotation angles in degrees.
        cameraAngles = {
            'south':0,      'south_west': 315,
            'west': 270,    'north_west': 225,
            'north':180,    'north_east': 135,
            'east': 90,     'south_east': 45
        }
        # ----- Animation
        # Dictionaries mapping internal keys to user-defined animation names and toggle states.
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
        
        # ----- Filename and path
        # Retrieves the base save path from user input.            
        pathSaveAt = context.scene.IEAS_properties.Save_at
        # Converts the path to an absolute path for consistency, preventing relative path issues.
        pathSaveAt = os.path.abspath(pathSaveAt)
        # Combines prefix and resref for use in filename construction.      
        prefixResref = context.scene.IEAS_properties.Prefix + context.scene.IEAS_properties.Resref
                
        # ----- Deselecting and selecting
        # Deselects all objects in the scene to ensure only the target object is affected.
        bpy.ops.object.select_all(action='DESELECT')
        # Retrieves the name of the object selected in the UI.        
        objectName = context.scene.IEAS_properties.Object_List.name
        # Selects the specific object by setting its selection state to True.
        bpy.context.scene.objects[objectName].select_set(True)
        # Sets the selected object as the active object, crucial for operations relying on `bpy.context.active_object`.
        bpy.context.view_layer.objects.active = bpy.data.objects[objectName]
        
        # ----- Debugging 
        # TODO: Delete print
        print("--------IEAS_OT_Final----------")
        # TODO: Delete print
        print("pathSaveAt:",pathSaveAt)
        # TODO: Delete print
        print("prefixResref:",prefixResref)
        # TODO: Delete print
        print("Object List:",context.scene.IEAS_properties.Object_List.name)
        
        # ----- Main/Outer loop 
        # Iterates through each defined animation.  
        for animationKey, animation in animationFolderNames.items():
            # Attempts to get the animation action data block.
            bpy.context.active_object.animation_data.action = bpy.data.actions.get(animation)
            currentAction = bpy.context.active_object.animation_data.action
            
            # Proceeds only if the animation is enabled by the user and the action exists in Blender. 
            if(animationToggle[animationKey] == True and currentAction != None):
               
                # Assigns the current animation action to the active object's animation data.
                bpy.context.active_object.animation_data.action = bpy.data.actions.get(animation)               
                # Sets the scene's end frame to match the animation's end frame, converted to an integer
                # to prevent rendering empty frames beyond the action's actual length.
                bpy.context.scene.frame_end = int(bpy.context.active_object.animation_data.action.frame_range[1])     
                # Constructs the base folder path for the current animation.
                animation_folder = os.path.join(pathSaveAt, animation)
                
                # ----- Debugging
                # TODO: Delete print
                print("animation:",animation)
                # TODO: Delete print
                print("action:",bpy.context.active_object.animation_data.action)
                # TODO: Delte print
                print("Frame End:",bpy.context.scene.frame_end)
                
                # Creates the animation-specific subfolder if it doesn't already exist.
                if not os.path.exists(animation_folder):
                    os.makedirs(animation_folder)
                    
                #  ----- Nested/Middle loop
                # Iterates through each defined camera position/direction.
                for positionKey, position in cameraPosFolderNames.items():
                    # Uses only the camera positions that are selected by the user.
                    if(cameraPosToggles[positionKey] == True):
                        # Creates a subfolder for the specific angle/direction.
                        position_folder = os.path.join(animation_folder, positionKey)                  
                        if not os.path.exists(position_folder):
                            os.makedirs(position_folder)
                            
                        # Rotates the active object (the character/model) around its Z-axis to face the current direction.
                        # The script rotates the subject, relying on a static camera to capture it, rather than rotating the camera itself.
                        bpy.context.active_object.rotation_euler[2] = math.radians(cameraAngles[positionKey])
                        
                        # ----- Debugging
                        # TODO: Delete print
                        #print("\nbpy.context.active_object.rotation_euler:",bpy.context.active_object.rotation_euler)
                        # TODO: Delete print
                        #print("\nbpy.context.active_object.rotation_euler[2]:",bpy.context.active_object.rotation_euler[2])
                
                        # ----- Variables used in nested inner loop
                        frameStart      = bpy.context.scene.frame_start
                        frameEnd        = bpy.context.scene.frame_end
                        renderFrame     = bpy.ops.render.render
                        Every_X_Frame   = context.scene.IEAS_properties.Every_X_Frame
                        
                        #  ----- Nested/Inner loop 
                        # Loops through frames within the animation's range, stepping by 'Every_X_Frame'.
                        for frame in range(frameStart,frameEnd,Every_X_Frame):
                            # Sets the current frame of the scene, updating the object's animation pose.
                            bpy.context.scene.frame_current = frame
                            
                            # Constructs the filename for the current sprite, including prefix, animation, position, and padded frame number.
                            if(positionKey == 'east' or positionKey == 'south_east' or positionKey == 'north_east'):                     
                                fileName = f"{prefixResref}{animationKey}E_{positionKey}_{str(frame).zfill(5)}.png"
                            else:
                                fileName = f"{prefixResref}{animationKey}_{positionKey}_{str(frame).zfill(5)}.png"
                                
                            
                            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
                            bpy.context.scene.render.filepath = os.path.join(position_folder, fileName)
                            
                            # This is the actual rendering process.
                            # `animation=False` renders a single still image.
                            # `write_still=True` saves the rendered image to the specified `filepath`.
                            # The first `False` argument disables undo support for the operation.
                            renderFrame(  False,
                                          animation     =False,
                                          write_still   =True)
                            
                            # ----- Debugging
                            # TODO: Delete print
                            #print("position_folder:",position_folder)
                            # TODO: Delete print
                            print("fileName:",fileName)
                            # TODO: Delete print
                            print("filepath:",bpy.context.scene.render.filepath)
                            # TODO: Delete print
                            print("action:",bpy.context.active_object.animation_data.action)
        
        # ----- Debugging
        # TODO: Delete print
        # Calculates and prints the total time taken for the rendering process.
        print("Elapsed:",time.time() - startTimer)
        
        return {'FINISHED'}


# --------
# Purpose:
# --------
# Defines the main panel for the add-on in the Blender UI.
# It serves as a container for other sub-panels.
# -----------------------------------------------------------
class IEAS_PT_Core(Panel):
    # Use this as a tooltip for menu items and buttons. 
    """Infinity Engine AutoSpriter is a Blender add-on that automates sprite creation from creature animations."""
    
     # --- Blender specific class variables
    bl_label        = "IE AutoSpriter"    # Visible name when category is opened (title of the panel).
    bl_idname       = 'IEAS_PT_Core'      # Unique identifier for the panel. Naming convention: 'CATEGORY_PT_name'.
    bl_space_type   = 'VIEW_3D'           # Specifies the editor type where the panel will appear (3D Viewport).
    bl_region_type  = 'UI'                # Specifies the region within the editor where the panel will be placed.
    bl_category     = bl_label            # Name of the tab under which the panel will be found.
    
    # --- Blender specific function which places elements into GUI
    # This method is called by Blender to draw the UI elements within the panel.
    def draw(self, context):
        pass


# --------
# Purpose:
# --------
# This panel defines general settings that apply across the entire sprite rendering process.
# ------------------------------------------------------------------------------------------
class IEAS_PT_GlobalParameters(Panel):
    """This step defines general settings that apply across the entire sprite rendering process."""
    
    # --- Blender specific class variables
    bl_label        = "Step 1: Global Parameters" 
    bl_idname       = 'IEAS_PT_GlobalParameters'
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "IE AutoSpriter"
    bl_parent_id    = 'IEAS_PT_Core' # Specifies the parent panel, making it a sub-panel of IEAS_PT_Core.
    bl_options      = {'DEFAULT_CLOSED'} # Panel starts collapsed by default.
    
    # --- Blender specific function which places elements into GUI
    # This method draws the UI elements for global rendering parameters.
    def draw(self, context):
        # Instances by pointers: Draws UI elements linked to the properties defined in IEAS_PGT_Inputs.
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
# This panel allows for the addition of specific shading nodes to the material setup.
# This is crucial for Infinity Engine sprites, which often require indexed color palettes
# and specific material properties.
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
    # This method draws the UI elements for shading node settings.
    def draw(self, context):
        layout = self.layout
        # Draws UI elements linked to material-related properties.
        layout.prop(context.scene.IEAS_properties, "Principled_BSDF")
        layout.prop(context.scene.IEAS_properties, "Material_Output")
        layout.prop(context.scene.IEAS_properties, "Material_List")
        col = layout.column()
        # Creates a button that executes the IEAS_OT_ShadingNodes operator.
        col.operator("ieas.shading_nodes")
        
        
 
# --------
# Purpose:
# --------
# This panel manages the output folders and defines which camera orientations (directions)
# will be rendered for the sprites.
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
    # This method draws the UI elements for camera direction settings.
    def draw(self, context):
        # Creates rows for each direction, displaying the subfolder name input and a toggle.       
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
# This panel defines which animations (Blender Actions) should be rendered
# and how their corresponding output folders/filenames will be named.
# -------------------------------------------------------------------------
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
    # This method draws the UI elements for animation selection and naming.
    def draw(self, context):
            
        # Creates rows for each animation, displaying the name input and a toggle.  
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
# This final panel contains the button to start the sprite rendering process.
# ---------------------------------------------------------------------------
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
    # This method draws the UI elements for the final step, including the render button.
    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("ieas.final") # selfdefined button functionality
 
               
# --------
# Purpose:
# --------      
# Registers all classes (Operators, PropertyGroups, Panels) with Blender.
# This makes them available for use in the Blender environment and within the add-on.
# -----------------------------------------------------------------------------------
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
    
    # Pointers: Registers the PropertyGroup to the scene, making its properties accessible via `bpy.context.scene.IEAS_properties`.
    bpy.types.Scene.IEAS_properties = bpy.props.PointerProperty(type=IEAS_PGT_Inputs)
    

# --------
# Purpose:
# --------
# Unregisters all classes and cleans up custom properties when the add-on is disabled.
# This prevents data remnants and potential conflicts if the add-on is re-enabled or other add-ons are used(??).
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
# Controls script execution: if the script is run directly in Blender's text editor (as main),
# it will call the register function. This is standard practice for Blender add-ons. 
if __name__ == "__main__":
    register()