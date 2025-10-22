# Never Forget: Comments can "lie", but code not so much ;P

# Used source:
# ------------
# https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#your-first-add-onimport bpy
# https://docs.blender.org/api/current/bpy.types.Operator.html
# https://developer.blender.org/docs/release_notes/2.80/python_api/addons/#Naming
# https://docs.blender.org/api/current/bpy.props.html#bpy.props.PointerProperty
# https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.select_all
# https://docs.blender.org/api/current/bpy.ops.render.html#bpy.ops.render.render
# https://docs.blender.org/api/current/info_best_practice.html#user-interface-layout
# https://docs.blender.org/api/current/bpy.props.html#bpy.props.EnumProperty
# ----------------------------------------------------------------------------------
# (PT   = Panel Type)
# (OT   = Operator Type)
# (PGT  = Property Group Type)

from bpy.types import Panel
from bpy.types import PropertyGroup
from bpy.types import Operator
from dataclasses import dataclass, replace
import bpy
import os
import shutil
import math
import time
import numpy as np


# --------
# Purpose:
# --------
# Contains Add-on metadata and registration information for Blender.
# ------------------------------------------------------------------
bl_info = {
    "name": "IE AutoSpriter",
    "author": "Incrementis",
    "version": (0, 29, 0),
    "blender": (4, 0, 0),
    "location": "Render > IE AutoSpriter",
    "category": "Render",
    "description": "Infinity Engine AutoSpriter is a Blender add-on that automates sprite creation from creature animations for IE games. GitHub:https://github.com/Incrementis/IE-AutoSpriter- ",
}


# --------
# Purpose:
# --------
# Contains parameters for the class IEAS_AnimationTypes 
# -----------------------------------------------------
@dataclass
class IEAS_AnimationTypesParameters:
    """Contains parameters for the class IEAS_AnimationTypes"""
    exclude:                    bool    # Deactivates every collection and activates only creature collection.
    CreatureCollectionName:     str     # The name of the main creature's collection.
    CreatureCollectionNameLP:   str     # The name of the creature's lower part collection.
    animationWeaponFolderNames: dict    # Maps weapon keys to collection names.
    animationWeaponToggles:     dict    # Toggles rendering for specific weapons.
    pathSaveAt:                 str     # The output file path for rendered sprites.
    animation:                  str     # The current animation name (e.g., "dead").
    positionKey:                str     # The camera angle/direction key (e.g., "south").
    animationKey:               str     # A short key for the animation (e.g., "TW").
    frame:                      int     # The current frame number.
    prefixResref:               str     # The combined filename prefix and resref.
    position_folder:            str     # The full path to the subfolder for the current camera position.


# --------
# Purpose:
# --------
# Collection of methods for preparing animation types for rendering.
# ------------------------------------------------------------------
class IEAS_AnimationTypes():
    """Contains methods for handling different animation types before rendering"""
    
    # --- TODO: Methods
    def type0000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling 0000 type logic."""       
        if (typeParameters.exclude == False):
            # Constructs the filename for the current sprite, including prefix,resref and padded frame number.
            fileName = f"{typeParameters.prefixResref}_{str(typeParameters.frame).zfill(5)}.png"                    
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)         
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                          
    def type1000_monster_quadrant(self, typeParameters:IEAS_AnimationTypesParameters):
        """Handles the logic for rendering and processing monster quadrants of type 1000."""
        if (typeParameters.exclude == False):
            # Used to identify which sprite file is defined for which sequence.
            sequences = {
                'WK':'G1', 
                'SD':'G2', 'SC':'G2', 'GH':'G2', 'DE':'G2', 'TW':'G2',
                'A1':'G3', 'A2':'G3', 'A3':'G3',
            }
            animationKey    = sequences[typeParameters.animationKey]    # Gets e.g. G1.
            # TODO: Don't forget to apply resolution in step 1 to blender renderer(Those lines are key lines).
            width           = bpy.context.scene.render.resolution_x
            height          = bpy.context.scene.render.resolution_y
            fileName        = "temp.png"
            # Used to identify which quadrant has which coordinates for slicing.
            # Since the image is divided into four parts, a divisor of 2 is required.
            quadrants = {
                'Q1': (slice(height//2, height), slice(0, width//2)),   'Q2': (slice(height//2, height), slice(width//2, width)),
                'Q3': (slice(0, height//2), slice(0, width//2)),        'Q4': (slice(0, height//2), slice(width//2, width)),
            }
            quadrantsNumbers = {
                'Q1': "1", 'Q2': "2",
                'Q3': "3", 'Q4': "4"
            }                                        
            # This tells Blender where to save the next (temporary) rendered image.
            temp_folder = os.path.join(typeParameters.position_folder, "temp")
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            # This tells Blender where to save the next (temporary) rendered image.                    
            bpy.context.scene.render.filepath = os.path.join(temp_folder, fileName)                 
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
            # Loads the rendered image from disk and retrieves its pixel data.      
            renderedImage       = bpy.data.images.load(bpy.context.scene.render.filepath)                       
            pixels              = renderedImage.pixels
            arrPixels           = np.array(pixels)# (flat array)  
            channels            = 4
            # Reshapes the 1D pixel array into a 3D array (height, width, channels).
            arrPixelsReshaped   = np.reshape(arrPixels, (height, width, channels))
            arrPixelsFlipped    = arrPixelsReshaped
                        
            # Processes the pixels for each quadrant and writes them as an image to a specific location.
            for quadrant, coordinate in quadrants.items():                                                          
                # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
                if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                    fileNameQuadrant = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}{quadrantsNumbers[quadrant]}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                else:
                    fileNameQuadrant = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}{quadrantsNumbers[quadrant]}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                
                # Zeroes out the pixels of all quadrants except the current one.
                # This clever approach avoids the need for if-statements to handle each quadrant's logic separately.
                quadrant_path = os.path.join(typeParameters.position_folder, f"{quadrant}")
                if not os.path.exists(quadrant_path):
                    os.makedirs(quadrant_path)
                    
                quadrantFile_path       = os.path.join(quadrant_path, fileNameQuadrant)
                # Prevents referencing the original values of the variables
                tempQuadrants           = quadrants.copy()
                tempArrPixelsReshaped   = arrPixelsReshaped.copy()
                # Deletes the current quadrant coordinate, so the remaining quadrants values can be set(Benefit: No if statements needed).
                del tempQuadrants[quadrant]
                for remainingCoordinate in tempQuadrants.values():
                    tempArrPixelsReshaped[remainingCoordinate] = 0 # Transparent
                    
                # Flattens the array so it can be stored into a blender image data block.
                arrPixelsFlatten = np.reshape(tempArrPixelsReshaped,arrPixels.shape)               
                # Creates a new Blender image data block.
                quadrantImage = bpy.data.images.new(
                    name="QuadrantType1000MQ",
                    width=width,
                    height=height,
                    alpha=True,
                )               
                # Assign the manipulated NumPy array's pixel data to the new Blender image.
                quadrantImage.pixels = arrPixelsFlatten             
                # Set the new image's file path and format.
                quadrantImage.filepath_raw = quadrantFile_path
                quadrantImage.file_format = 'PNG'
                # Save the new image data block to a file.
                quadrantImage.save()
                
            # Deletes the temporary folder.
            shutil.rmtree(temp_folder)
            
    def type1000_monster_multi_sp0(self, typeParameters:IEAS_AnimationTypesParameters):
        """Handles the logic for rendering and processing monster multi of type 1000(split_bams = 0)."""
        if (typeParameters.exclude == False):
            # Used to identify which sprite file is defined for which sequence.
            sequences = {
                'WK':'G1',
                'SD':'G2', 'SC':'G2', 'SP':'G2',
                'A1':'G3', 'A2':'G3', 'A3':'G3',
                'GH':'G4', 'DE':'G4', 'SL':'G4', 'GU':'G4', 'DE':'G4', 'TW':'G4',
                'SP':'G5', 'CA':'G5',
            }
            animationKey    = sequences[typeParameters.animationKey]    # Gets e.g. G1.
            width           = bpy.context.scene.render.resolution_x
            height          = bpy.context.scene.render.resolution_y
            fileName        = "temp.png"
            # Used to identify which quadrant has which coordinates for slicing.
            # Since the image is divided into four parts, a divisor of 2 is required.
            quadrants = {
                'Q1': (slice(height//2, height), slice(0, width//2)),   'Q2': (slice(height//2, height), slice(width//2, width)),
                'Q3': (slice(0, height//2), slice(0, width//2)),        'Q4': (slice(0, height//2), slice(width//2, width)),
            }
            quadrantsNumbers = {
                'Q1': "1", 'Q2': "2",
                'Q3': "3", 'Q4': "4"
            }
            # This tells Blender where to save the next (temporary) rendered image.
            temp_folder = os.path.join(typeParameters.position_folder, "temp")
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            # This tells Blender where to save the next (temporary) rendered image.                    
            bpy.context.scene.render.filepath = os.path.join(temp_folder, fileName)                 
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
            # Loads the rendered image from disk and retrieves its pixel data.      
            renderedImage       = bpy.data.images.load(bpy.context.scene.render.filepath)                       
            pixels              = renderedImage.pixels
            arrPixels           = np.array(pixels)# (flat array)  
            channels            = 4
            # Reshapes the 1D pixel array into a 3D array (height, width, channels).
            arrPixelsReshaped   = np.reshape(arrPixels, (height, width, channels))
            arrPixelsFlipped    = arrPixelsReshaped
                        
            # Processes the pixels for each quadrant and writes them as an image to a specific location.
            for quadrant, coordinate in quadrants.items():                                                          
                # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
                fileNameQuadrant = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}{quadrantsNumbers[quadrant]}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                
                # Zeroes out the pixels of all quadrants except the current one.
                # This clever approach avoids the need for if-statements to handle each quadrant's logic separately.
                quadrant_path = os.path.join(typeParameters.position_folder, f"{quadrant}")
                if not os.path.exists(quadrant_path):
                    os.makedirs(quadrant_path)
                    
                quadrantFile_path       = os.path.join(quadrant_path, fileNameQuadrant)
                # Prevents referencing the original values of the variables
                tempQuadrants           = quadrants.copy()
                tempArrPixelsReshaped   = arrPixelsReshaped.copy()
                # Deletes the current quadrant coordinate, so the remaining quadrants values can be set(Benefit: No if statements needed).
                del tempQuadrants[quadrant]
                for remainingCoordinate in tempQuadrants.values():
                    tempArrPixelsReshaped[remainingCoordinate] = 0 # Transparent
                    
                # Flattens the array so it can be stored into a blender image data block.
                arrPixelsFlatten = np.reshape(tempArrPixelsReshaped,arrPixels.shape)               
                # Creates a new Blender image data block.
                quadrantImage = bpy.data.images.new(
                    name="QuadrantType1000MMsp0",
                    width=width,
                    height=height,
                    alpha=True,
                )               
                # Assign the manipulated NumPy array's pixel data to the new Blender image.
                quadrantImage.pixels = arrPixelsFlatten
                # Set the new image's file path and format.
                quadrantImage.filepath_raw = quadrantFile_path
                quadrantImage.file_format = 'PNG'
                # Save the new image data block to a file.
                quadrantImage.save()
                
            # Deletes the temporary folder.
            shutil.rmtree(temp_folder)
    
    def type1000_monster_multi_sp1(self, typeParameters:IEAS_AnimationTypesParameters):
        """Handles the logic for rendering and processing monster multi of type 1000(split_bams = 1)."""
        if (typeParameters.exclude == False):
            # Used to identify which sprite file is defined for which sequence.
            sequences = {
                'WK':'G1',
                'SD':'G2', 'SC':'G2', 'SP':'G2',
                'A1':'G3', 'A2':'G3', 'A3':'G3',
                'GH':'G4', 'DE':'G4', 'SL':'G4', 'GU':'G4', 'DE':'G4', 'TW':'G4',
                'SP':'G5', 'CA':'G5',
            }
            animationKey    = sequences[typeParameters.animationKey]    # Gets e.g. G1.
            width           = bpy.context.scene.render.resolution_x
            height          = bpy.context.scene.render.resolution_y
            fileName        = "temp.png"
            # Used to identify which quadrant has which coordinates for slicing.
            # Since the image is divided into nine parts, a divisor of 3 is required.
            rowsA       = slice((2*height)//3, height)
            rowsC       = slice(0, height//3)
            rowsB       = slice(height//3, (2*height)//3)
            columnsA    = slice(0, width//3)
            columnsB    = slice(width//3, (2*width)//3)
            columnsC    = slice((2*width)//3, width)
            quadrants = {
                'Q1': (rowsA, columnsA), 'Q2': (rowsA, columnsB), 'Q3': (rowsA, columnsC),
                'Q4': (rowsB, columnsA), 'Q5': (rowsB, columnsB), 'Q6': (rowsB, columnsC),
                'Q7': (rowsC, columnsA), 'Q8': (rowsC, columnsB), 'Q9': (rowsC, columnsC),
            }
            quadrantsNumbers = {
                'Q1': "1", 'Q2': "2",'Q3': "3",
                'Q4': "4", 'Q5': "5",'Q6': "6",
                'Q7': "7", 'Q8': "8",'Q9': "9",
            }
            directions = {
            'south':        "00", 'south_south_west': "01",
            'south_west':   "02", 'west_south_west':  "03",
            'west':         "04", 'west_north_west':  "05",
            'north_west':   "06", 'north_north_west': "07",
            'north':        "08",
            }
            
            # --- Debugging: TODO - Delete all following prints
#            print(f"rowsA: {rowsA.start} to {rowsA.stop}")
#            print(f"rowsB: {rowsB.start} to {rowsB.stop}")
#            print(f"rowsC: {rowsC.start} to {rowsC.stop}")
#            print(f"columnsA: {columnsA.start} to {columnsA.stop}")
#            print(f"columnsB: {columnsB.start} to {columnsB.stop}")
#            print(f"columnsC: {columnsC.start} to {columnsC.stop}")
            
            # This tells Blender where to save the next (temporary) rendered image.
            temp_folder = os.path.join(typeParameters.position_folder, "temp")
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            # This tells Blender where to save the next (temporary) rendered image.                    
            bpy.context.scene.render.filepath = os.path.join(temp_folder, fileName)                 
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
            # Loads the rendered image from disk and retrieves its pixel data.      
            renderedImage       = bpy.data.images.load(bpy.context.scene.render.filepath)                       
            pixels              = renderedImage.pixels
            arrPixels           = np.array(pixels)# (flat array)  
            channels            = 4
            # Reshapes the 1D pixel array into a 3D array (height, width, channels).
            arrPixelsReshaped   = np.reshape(arrPixels, (height, width, channels))
            arrPixelsFlipped    = arrPixelsReshaped          
            # Creates a path for a transparent pixel that serves as a placeholder for the unused cycles in the BAM file.
            placeholder_path    = os.path.join(typeParameters.position_folder, "placeholder.png")              
            # Creates a new Blender image data block.        
            placeholderImage = bpy.data.images.new(
                    name    = "QuadrantType1000MMsp1Placeholder",
                    width   = 1,
                    height  = 1,
                    alpha   = True,
            )
            placeholderImage.pixels = [0,0,0,0]  # One transparent pixel (RGBA)             
            # Set the new image's file path and format.
            placeholderImage.filepath_raw   = placeholder_path
            placeholderImage.file_format    = 'PNG'
            # Save the new image data block to a file.
            placeholderImage.save()
                    
            # Processes the pixels for each quadrant and writes them as an image to a specific location.
            for quadrant, coordinate in quadrants.items():                                                          
                # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
                fileNameQuadrant = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}{quadrantsNumbers[quadrant]}{directions[typeParameters.positionKey]}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                
                # Zeroes out the pixels of all quadrants except the current one.
                # This clever approach avoids the need for if-statements to handle each quadrant's logic separately.
                quadrant_path = os.path.join(typeParameters.position_folder, f"{quadrant}")
                if not os.path.exists(quadrant_path):
                    os.makedirs(quadrant_path)
                    
                quadrantFile_path       = os.path.join(quadrant_path, fileNameQuadrant)
                # Prevents referencing the original values of the variables
                tempQuadrants           = quadrants.copy()
                tempArrPixelsReshaped   = arrPixelsReshaped.copy()
                # Deletes the current quadrant coordinate, so the remaining quadrants values can be set(Benefit: No if statements needed).
                del tempQuadrants[quadrant]
                for remainingCoordinate in tempQuadrants.values():
                    tempArrPixelsReshaped[remainingCoordinate] = 0 # Transparent
                    
                # Flattens the array so it can be stored into a blender image data block.
                arrPixelsFlatten = np.reshape(tempArrPixelsReshaped,arrPixels.shape)               
                # Creates a new Blender image data block.
                quadrantImage = bpy.data.images.new(
                    name    = "QuadrantType1000MMsp1",
                    width   = width,
                    height  = height,
                    alpha   = True,
                )               
                # Assign the manipulated NumPy array's pixel data to the new Blender image.
                quadrantImage.pixels = arrPixelsFlatten
                # Set the new image's file path and format.
                quadrantImage.filepath_raw  = quadrantFile_path
                quadrantImage.file_format   = 'PNG'
                # Save the new image data block to a file.
                quadrantImage.save()
                
            # Deletes the temporary folder.
            shutil.rmtree(temp_folder)
            
    def type1000_multi_new_sp0(self, typeParameters:IEAS_AnimationTypesParameters):
        """Handles the logic for rendering and processing multi new of type 1000(split_bams = 0)."""
        if (typeParameters.exclude == False):
            # Used to identify which sprite file is defined for which sequence.
            sequences = {
                'WK':'G1', 'SC':'G1', 'SD':'G1', 'GH':'G1', 'DE':'G1', 'TW':'G1',
                'A1':'G2', 'A2':'G2', 'A3':'G2', 'A4':'G2', 'A5':'G2', 'SP':'G2', 'CA':'G2',
            }
            animationKey    = sequences[typeParameters.animationKey]    # Gets e.g. G1.
            width           = bpy.context.scene.render.resolution_x
            height          = bpy.context.scene.render.resolution_y
            fileName        = "temp.png"
            # Used to identify which quadrant has which coordinates for slicing.
            # Since the image is divided into four parts, a divisor of 2 is required.
            quadrants = {
                'Q1': (slice(height//2, height), slice(0, width//2)),   'Q2': (slice(height//2, height), slice(width//2, width)),
                'Q3': (slice(0, height//2), slice(0, width//2)),        'Q4': (slice(0, height//2), slice(width//2, width)),
            }
            quadrantsNumbers = {
                'Q1': "1", 'Q2': "2",
                'Q3': "3", 'Q4': "4"
            }
            # This tells Blender where to save the next (temporary) rendered image.
            temp_folder = os.path.join(typeParameters.position_folder, "temp")
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            # This tells Blender where to save the next (temporary) rendered image.                    
            bpy.context.scene.render.filepath = os.path.join(temp_folder, fileName)                 
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     = False,
                          write_still   = True)
            # Loads the rendered image from disk and retrieves its pixel data.      
            renderedImage       = bpy.data.images.load(bpy.context.scene.render.filepath)                       
            pixels              = renderedImage.pixels
            arrPixels           = np.array(pixels)# (flat array)  
            channels            = 4
            # Reshapes the 1D pixel array into a 3D array (height, width, channels).
            arrPixelsReshaped   = np.reshape(arrPixels, (height, width, channels))
            arrPixelsFlipped    = arrPixelsReshaped
            
            # Processes the pixels for each quadrant and writes them as an image to a specific location.
            for quadrant, coordinate in quadrants.items():                                                          
                # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
                fileNameQuadrant = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}{quadrantsNumbers[quadrant]}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                
                # Zeroes out the pixels of all quadrants except the current one.
                # This clever approach avoids the need for if-statements to handle each quadrant's logic separately.
                quadrant_path = os.path.join(typeParameters.position_folder, f"{quadrant}")
                if not os.path.exists(quadrant_path):
                    os.makedirs(quadrant_path)
                    
                quadrantFile_path       = os.path.join(quadrant_path, fileNameQuadrant)
                # Prevents referencing the original values of the variables
                tempQuadrants           = quadrants.copy()
                tempArrPixelsReshaped   = arrPixelsReshaped.copy()
                # Deletes the current quadrant coordinate, so the remaining quadrants values can be set(Benefit: No if statements needed).
                del tempQuadrants[quadrant]
                for remainingCoordinate in tempQuadrants.values():
                    tempArrPixelsReshaped[remainingCoordinate] = 0 # Transparent
                    
                # Flattens the array so it can be stored into a blender image data block.
                arrPixelsFlatten = np.reshape(tempArrPixelsReshaped,arrPixels.shape)               
                # Creates a new Blender image data block.
                quadrantImage = bpy.data.images.new(
                    name    = "QuadrantType1000MNsp0",
                    width   = width,
                    height  = height,
                    alpha   = True,
                )               
                # Assign the manipulated NumPy array's pixel data to the new Blender image.
                quadrantImage.pixels        = arrPixelsFlatten
                # Set the new image's file path and format.
                quadrantImage.filepath_raw  = quadrantFile_path
                quadrantImage.file_format   = 'PNG'
                # Save the new image data block to a file.
                quadrantImage.save()
                
            # Deletes the temporary folder.
            shutil.rmtree(temp_folder)
         
    def type1000_multi_new_sp1(self, typeParameters:IEAS_AnimationTypesParameters):
        """Handles the logic for rendering and processing multi new of type 1000(split_bams = 1)."""
        if (typeParameters.exclude == False):
            # Used to identify which sprite file is defined for which sequence.
            sequences = {
                'WK':'G1', 'SC':'G1', 'SD':'G1', 'GH':'G1', 'DE':'G1', 'TW':'G1',
                'A1':'G2', 'A2':'G2', 'A3':'G2', 'A4':'G2', 'A5':'G2', 'SP':'G2', 'CA':'G2',
            }
            animationKey    = sequences[typeParameters.animationKey]    # Gets e.g. G1.
            width           = bpy.context.scene.render.resolution_x
            height          = bpy.context.scene.render.resolution_y
            fileName        = "temp.png"
            # Used to identify which quadrant has which coordinates for slicing.
            # Since the image is divided into four parts, a divisor of 2 is required.
            quadrants = {
                'Q1': (slice(height//2, height), slice(0, width//2)),   'Q2': (slice(height//2, height), slice(width//2, width)),
                'Q3': (slice(0, height//2), slice(0, width//2)),        'Q4': (slice(0, height//2), slice(width//2, width)),
            }
            quadrantsNumbers = {
                'Q1': "1", 'Q2': "2",
                'Q3': "3", 'Q4': "4"
            }
            # This tells Blender where to save the next (temporary) rendered image.
            temp_folder = os.path.join(typeParameters.position_folder, "temp")
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            # This tells Blender where to save the next (temporary) rendered image.                    
            bpy.context.scene.render.filepath = os.path.join(temp_folder, fileName)                 
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     = False,
                          write_still   = True)
            # Loads the rendered image from disk and retrieves its pixel data.      
            renderedImage       = bpy.data.images.load(bpy.context.scene.render.filepath)                       
            pixels              = renderedImage.pixels
            arrPixels           = np.array(pixels)# (flat array)  
            channels            = 4
            # Reshapes the 1D pixel array into a 3D array (height, width, channels).
            arrPixelsReshaped   = np.reshape(arrPixels, (height, width, channels))
            arrPixelsFlipped    = arrPixelsReshaped
            
            # Processes the pixels for each quadrant and writes them as an image to a specific location.
            for quadrant, coordinate in quadrants.items():                                                          
                # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
                fileNameQuadrant = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}{quadrantsNumbers[quadrant]}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                
                # Zeroes out the pixels of all quadrants except the current one.
                # This clever approach avoids the need for if-statements to handle each quadrant's logic separately.
                quadrant_path = os.path.join(typeParameters.position_folder, f"{quadrant}")
                if not os.path.exists(quadrant_path):
                    os.makedirs(quadrant_path)
                    
                quadrantFile_path       = os.path.join(quadrant_path, fileNameQuadrant)
                # Prevents referencing the original values of the variables
                tempQuadrants           = quadrants.copy()
                tempArrPixelsReshaped   = arrPixelsReshaped.copy()
                # Deletes the current quadrant coordinate, so the remaining quadrants values can be set(Benefit: No if statements needed).
                del tempQuadrants[quadrant]
                for remainingCoordinate in tempQuadrants.values():
                    tempArrPixelsReshaped[remainingCoordinate] = 0 # Transparent
                    
                # Flattens the array so it can be stored into a blender image data block.
                arrPixelsFlatten = np.reshape(tempArrPixelsReshaped,arrPixels.shape)               
                # Creates a new Blender image data block.
                quadrantImage = bpy.data.images.new(
                    name    = "QuadrantType1000MNsp1",
                    width   = width,
                    height  = height,
                    alpha   = True,
                )               
                # Assign the manipulated NumPy array's pixel data to the new Blender image.
                quadrantImage.pixels        = arrPixelsFlatten
                # Set the new image's file path and format.
                quadrantImage.filepath_raw  = quadrantFile_path
                quadrantImage.file_format   = 'PNG'
                # Save the new image data block to a file.
                quadrantImage.save()
                
            # Deletes the temporary folder.
            shutil.rmtree(temp_folder)
            
    def type2000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling 2000 type logic."""    
        # ----- Deactivates/Activates collections      
        if (typeParameters.exclude == True):
            # Deactivates every collection found.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collection.exclude = True            
            # Activates only creature collection.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].exclude = False
            # TODO:Delete!
            print("type2000: Executing 'exclude' logic for 2000 type.")
        else:
            # Used to identify which sprite file is defined for which sequence.
            sequences = {
                'WK':'G1', 'SC':'G1', 'SD':'G1', 'GH':'G1', 'DE':'G1', 'TW':'G1',
                'A1':'G2', 'A2':'G2', 'A3':'G2', 'SP':'G2', 'CA':'G2',
            }
            animationKey    = sequences[typeParameters.animationKey]    # Gets e.g. G1.
            
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                          
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)            
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                       
            # TODO:Delete!
            print("type2000: Executing complex logic for 2000 type.")
            # Stores the initial 'holdout' state of the creature collection before modification.
            # 'holdout' makes objects within the collection invisible during rendering without excluding them from the view layer. 
            holdout = bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout
            
            # ----- Debugging
            # TODO: Delete print
            print("holdout:",holdout)
                                            
            # Activates 'holdout' (invisibility for rendering) specifically for the creature collection.
            # This ensures only weapon sprites are rendered when collections are toggled.
            if (holdout == False):
                # WARNING: This change to 'holdout' status will not be visibly reflected in the Blender GUI's Outliner.
                bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout = True
            
            # Iterates through all top-level collections in the current view layer to manage their visibility.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collectionName  = collection.name
                # Finds the corresponding weapon key for the collection name.
                # "next" is used for a single, fast lookup with built-in error handling.
                # This key is also used as the <wovl> (weapon overlay) identifier in the filename.
                wovl = next((key for key,value in typeParameters.animationWeaponFolderNames.items() if value == collectionName), None)
                
                # Checks if the collection corresponds to a recognized weapon animation and if that weapon is enabled for rendering.
                if ( (wovl != None) and (typeParameters.animationWeaponToggles[wovl] == True) ):
                    # Deactivates exclusion for the current weapon collection, making it visible for rendering.
                    # All other weapon collections remain excluded (invisible) by default.
                    collection.exclude=False
                    
                    # Constructs the base output folder path for the current weapon.
                    weapon_folder = os.path.join(typeParameters.pathSaveAt, collectionName)
                    weapon_animation_folder = os.path.join(weapon_folder, typeParameters.animation)
                    
                    # Creates a subfolder for the specific weapon and camera angle.
                    weapon_position_folder = os.path.join(weapon_animation_folder, typeParameters.positionKey)                  
                    if not os.path.exists(weapon_position_folder):
                        os.makedirs(weapon_position_folder)
                    
                    # Constructs the full filename for the current sprite, incorporating prefix, weapon identifier (wovl),
                    # animation key, camera position, and zero-padded frame number. East-facing sprites get an 'E' suffix.
                    if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                        fileName = f"{typeParameters.prefixResref}{wovl}{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                    else:
                        fileName = f"{typeParameters.prefixResref}{wovl}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                        
                    # Sets Blender's render output filepath for the current image. This is where the next rendered image will be saved.
                    bpy.context.scene.render.filepath = os.path.join(weapon_position_folder, fileName)                
                    # This is the actual rendering process.
                    # `animation=False` renders a single still image.
                    # `write_still=True` saves the rendered image to the specified `filepath`.
                    # The first `False` argument disables undo support for the operation.
                    renderFrame = bpy.ops.render.render
                    renderFrame(  False,
                                  animation     =False,
                                  write_still   =True)

                    # ----- Debugging
                    # TODO: Delete print
                    #print("position_folder:",position_folder)
                    # TODO: Delete print
                    print("fileName:",fileName)
                    # TODO: Delete print
                    print("weapon_folder:",weapon_folder)
                    # TODO: Delete print
                    print("weapon_position_folder:",weapon_position_folder)
                       
                    # After rendering the current weapon's sprite for this frame/angle, its collection is excluded again.
                    # This ensures only one weapon collection is active at any given time for subsequent renders.
                    collection.exclude = True
 
                # ----- Debugging
                # TODO: Delete print
                print("collectionName:",collectionName)
                # TODO: Delete print
                print("wovl:",wovl)
            
            # Resets the 'holdout' state of the creature collection to its original value.
            # This ensures the creature is visible again after weapon rendering is complete, if it was originally visible.
            if (holdout == False):
                # WARNING: This change to 'holdout' status will not be visibly reflected in the Blender GUI's Outliner.
                bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout = False
    
    def type3000_mirror0(self, typeParameters:IEAS_AnimationTypesParameters):
        """Handles the logic for rendering and processing type 3000(mirror = 0)."""
         # ----- Controls the 'exclude' and 'hide_render' visibility of collections -----
        if (typeParameters.exclude == True):
            # Deactivates every collection found.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collection.exclude = True            
            # Activates only creature collection.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].exclude = False
            # TODO:Delete!
            print("type3000M0: Executing 'exclude' logic for 3000M0 type.")
            print("typeParameters.CreatureCollectionName:",typeParameters.CreatureCollectionName)
        else:
            # TODO:Delete!
            print("type3000M0: Executing complex logic for 3000M0 type.") 
             # Used to identify which sprite file is defined for which sequence.
            sequences = {
                'DE':'G1', 'TW':'G1',       'SD':'G1',
                'SC':'G2', 'EMERGE':'G2',   'HIDE':'G2',
                'A1':'G3', 'CA':'G3',
            }
            animationKey = sequences[typeParameters.animationKey] # Gets e.g. G1.
            
            # Makes the main/upper creature collection visible for rendering.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].collection.hide_render  = False
            # Ensures the Lower Part collection remains excluded (invisible) on the View Layer.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionNameLP].exclude = True
            
            # Constructs the full filename for the current sprite, incorporating prefix, weapon identifier (wovl),
            # animation key, camera position, and zero-padded frame number. East-facing sprites get an 'E' suffix.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                          
            # ----- Setup for SECOND RENDER PASS: Lower Creature Part -----                                                 
            # Constructs the output folder path for the creature's lower part.
            lowerpart_folder            = os.path.join(typeParameters.pathSaveAt, typeParameters.CreatureCollectionNameLP)
            lowerpart_animation_folder  = os.path.join(lowerpart_folder, typeParameters.animation)
             # Creates a subfolder for the specific animation and position angle.
            lowerpart_position_folder   = os.path.join(lowerpart_animation_folder, typeParameters.positionKey)
            if not os.path.exists(lowerpart_position_folder):
                os.makedirs(lowerpart_position_folder)
                
            # Hides the main/upper creature collection (makes it invisible for the next render).
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].collection.hide_render = True             
            # Un-excludes the Lower Part collection, making its LayerCollection enabled
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionNameLP].exclude = False
            
            # Constructs the full filename for the current sprite (for the lower part), using the 'D' prefix.
            # East-facing sprites get an 'E' suffix.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}D{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}D{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                
             # Sets Blender's render output filepath for the current lower-part image.
            bpy.context.scene.render.filepath = os.path.join(lowerpart_position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                          
            # Restores the render visibility of the main/upper creature collection (visible for subsequent calls).
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].collection.hide_render  = False
                
    def type3000_mirror1(self, typeParameters:IEAS_AnimationTypesParameters):
        """Handles the logic for rendering and processing type 3000(mirror = 1)."""    
        # ----- Controls the 'exclude' and 'hide_render' visibility of collections -----
        if (typeParameters.exclude == True):
            # Deactivates every collection found.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collection.exclude = True            
            # Activates only creature collection.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].exclude = False
            # TODO:Delete!
            print("type3000M1: Executing 'exclude' logic for 3000M1 type.")
            print("typeParameters.CreatureCollectionName:",typeParameters.CreatureCollectionName)
        else:
            # TODO:Delete!
            print("type3000M1: Executing complex logic for 3000M1 type.")
            
            # Used to identify which sprite file is defined for which sequence.
            sequences = {
                'DE':'G1', 'TW':'G1',       'SD':'G1',
                'SC':'G2', 'EMERGE':'G2',   'HIDE':'G2',
                'A1':'G3', 'CA':'G3',
            }
            animationKey = sequences[typeParameters.animationKey] # Gets e.g. G1.
            
            # Makes the main/upper creature collection visible for rendering.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].collection.hide_render  = False
            # Ensures the Lower Part collection remains excluded (invisible) on the View Layer.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionNameLP].exclude = True
            
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                          
            # ----- Setup for SECOND RENDER PASS: Lower Creature Part -----                                                 
            # Constructs the output folder path for the creature's lower part.
            lowerpart_folder            = os.path.join(typeParameters.pathSaveAt, typeParameters.CreatureCollectionNameLP)
            lowerpart_animation_folder  = os.path.join(lowerpart_folder, typeParameters.animation)
             # Creates a subfolder for the specific animation and position angle.
            lowerpart_position_folder   = os.path.join(lowerpart_animation_folder, typeParameters.positionKey)
            if not os.path.exists(lowerpart_position_folder):
                os.makedirs(lowerpart_position_folder)
                
            # Hides the main/upper creature collection (makes it invisible for the next render).
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].collection.hide_render = True             
            # Un-excludes the Lower Part collection, making its LayerCollection enabled
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionNameLP].exclude = False
            
            # Constructs the full filename for the current sprite (for the lower part), using the 'D' prefix.
            fileName = f"{typeParameters.prefixResref}D{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            
            # Sets Blender's render output filepath for the current lower-part image.
            bpy.context.scene.render.filepath = os.path.join(lowerpart_position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                          
            # Restores the render visibility of the main/upper creature collection (visible for subsequent calls).
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].collection.hide_render  = False
    
    def type4000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling 4000 type logic."""
        if (typeParameters.exclude == False):
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.                  
            fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"              
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)        
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                
    def type7000_monster_sp0(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling 7000 monster split bams 0 type logic."""
         # ----- Deactivates/Activates collections      
        if (typeParameters.exclude == True):
            # Deactivates every collection found.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collection.exclude = True            
            # Activates only creature collection.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].exclude = False
            # TODO:Delete!
            print("type7000: Executing 'exclude' logic for type7000 monster sp0 type.")
        else:
            # Used to identify which sprite file is defined for which sequence
            sequences = {
                'SD':'G1', 'SC':'G1', 'WK':'G1', 'GH':'G1', 'GU':'G1', 'DE':'G1', 'TW':'G1', 
                'A1':'G2', 'A2':'G2', 'A3':'G2', 'A4':'G2', 'A5':'G2', 'SP':'G2', 'CA':'G2',
            }
            animationKey = sequences[typeParameters.animationKey] # Gets e.g. G1.
            
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)            
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                       
            # TODO:Delete!
            print("type7000: Executing 'exclude' logic for type7000 monster sp0 type.")
            # Stores the initial 'holdout' state of the creature collection before modification.
            # 'holdout' makes objects within the collection invisible during rendering without excluding them from the view layer. 
            holdout = bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout
            
            # ----- Debugging
            # TODO: Delete print
            print("holdout:",holdout)
                                            
            # Activates 'holdout' (invisibility for rendering) specifically for the creature collection.
            # This ensures only weapon sprites are rendered when collections are toggled.
            if (holdout == False):
                # WARNING: This change to 'holdout' status will not be visibly reflected in the Blender GUI's Outliner.
                bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout = True
            
            # Iterates through all top-level collections in the current view layer to manage their visibility.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collectionName  = collection.name
                # Finds the corresponding weapon key (e.g., 'A', 'B', 'C') for the collection name.
                # This key is also used as the <wovl> (weapon overlay) identifier in the filename.
                wovl = next((key for key,value in typeParameters.animationWeaponFolderNames.items() if value == collectionName), None)
                
                # Checks if the collection corresponds to a recognized weapon animation and if that weapon is enabled for rendering.
                if ( (wovl != None) and (typeParameters.animationWeaponToggles[wovl] == True) ):
                    # Deactivates exclusion for the current weapon collection, making it visible for rendering.
                    # All other weapon collections remain excluded (invisible) by default.
                    collection.exclude=False
                    
                    # Constructs the base output folder path for the current weapon.
                    weapon_folder = os.path.join(typeParameters.pathSaveAt, collectionName)
                    weapon_animation_folder = os.path.join(weapon_folder, typeParameters.animation)
                    
                    # Creates a subfolder for the specific weapon and camera angle.
                    weapon_position_folder = os.path.join(weapon_animation_folder, typeParameters.positionKey)                  
                    if not os.path.exists(weapon_position_folder):
                        os.makedirs(weapon_position_folder)
                    
                    # Constructs the full filename for the current sprite, incorporating prefix, weapon identifier (wovl),
                    # animation key, camera position, and zero-padded frame number. East-facing sprites get an 'E' suffix.
                    fileName = f"{typeParameters.prefixResref}{animationKey}{wovl}{typeParameters.animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                        
                    # Sets Blender's render output filepath for the current image. This is where the next rendered image will be saved.
                    bpy.context.scene.render.filepath = os.path.join(weapon_position_folder, fileName)                
                    # This is the actual rendering process.
                    # `animation=False` renders a single still image.
                    # `write_still=True` saves the rendered image to the specified `filepath`.
                    # The first `False` argument disables undo support for the operation.
                    renderFrame = bpy.ops.render.render
                    renderFrame(  False,
                                  animation     =False,
                                  write_still   =True)

                    # ----- Debugging
                    # TODO: Delete print
                    #print("position_folder:",position_folder)
                    # TODO: Delete print
                    print("fileName:",fileName)
                    # TODO: Delete print
                    print("weapon_folder:",weapon_folder)
                    # TODO: Delete print
                    print("weapon_position_folder:",weapon_position_folder)
                       
                    # After rendering the current weapon's sprite for this frame/angle, its collection is excluded again.
                    # This ensures only one weapon collection is active at any given time for subsequent renders.
                    collection.exclude = True
 
                # ----- Debugging
                # TODO: Delete print
                print("collectionName:",collectionName)
                # TODO: Delete print
                print("wovl:",wovl)
            
            # Resets the 'holdout' state of the creature collection to its original value.
            # This ensures the creature is visible again after weapon rendering is complete, if it was originally visible.
            if (holdout == False):
                # WARNING: This change to 'holdout' status will not be visibly reflected in the Blender GUI's Outliner.
                bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout = False
                
    def type7000_monster_sp1(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling 7000 monster split bams 1 type logic."""
         # ----- Deactivates/Activates collections      
        if (typeParameters.exclude == True):
            # Deactivates every collection found.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collection.exclude = True            
            # Activates only creature collection.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].exclude = False
            # TODO:Delete!
            print("type7000: Executing 'exclude' logic for type7000 monster sp1 type.")
        else:
            # Used to identify which sprite file is defined for which sequence
            sequences = {
                'SC':'G1', 'WK':'G11','SD':'G12', 'GH':'G13and14', 'DE':'G14', 'TW':'G14and15',
                'A1':'G2', 'A2':'G21', 'A3':'G22', 'A4':'G23', 'A5':'G24', 'SP':'G25', 'CA':'G26',
            }
            animationKey = sequences[typeParameters.animationKey] # Gets e.g. G1.
            
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            fileName = f"{typeParameters.prefixResref}{animationKey}{typeParameters.animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)            
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                       
            # TODO:Delete!
            print("type7000: Executing 'exclude' logic for type7000 monster sp1 type.")
            # Stores the initial 'holdout' state of the creature collection before modification.
            # 'holdout' makes objects within the collection invisible during rendering without excluding them from the view layer. 
            holdout = bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout
            
            # ----- Debugging
            # TODO: Delete print
            print("holdout:",holdout)
                                            
            # Activates 'holdout' (invisibility for rendering) specifically for the creature collection.
            # This ensures only weapon sprites are rendered when collections are toggled.
            if (holdout == False):
                # WARNING: This change to 'holdout' status will not be visibly reflected in the Blender GUI's Outliner.
                bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout = True
            
            # Iterates through all top-level collections in the current view layer to manage their visibility.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collectionName  = collection.name
                # Finds the corresponding weapon key (e.g., 'A', 'B', 'C') for the collection name.
                # This key is also used as the <wovl> (weapon overlay) identifier in the filename.
                wovl = next((key for key,value in typeParameters.animationWeaponFolderNames.items() if value == collectionName), None)
                
                # Checks if the collection corresponds to a recognized weapon animation and if that weapon is enabled for rendering.
                if ( (wovl != None) and (typeParameters.animationWeaponToggles[wovl] == True) ):
                    # Deactivates exclusion for the current weapon collection, making it visible for rendering.
                    # All other weapon collections remain excluded (invisible) by default.
                    collection.exclude=False
                    
                    # Constructs the base output folder path for the current weapon.
                    weapon_folder = os.path.join(typeParameters.pathSaveAt, collectionName)
                    weapon_animation_folder = os.path.join(weapon_folder, typeParameters.animation)
                    
                    # Creates a subfolder for the specific weapon and camera angle.
                    weapon_position_folder = os.path.join(weapon_animation_folder, typeParameters.positionKey)                  
                    if not os.path.exists(weapon_position_folder):
                        os.makedirs(weapon_position_folder)
                    
                    # Constructs the full filename for the current sprite, incorporating prefix, weapon identifier (wovl),
                    # animation key, camera position, and zero-padded frame number. East-facing sprites get an 'E' suffix.
                    fileName = f"{typeParameters.prefixResref}{animationKey}{wovl}{typeParameters.animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                        
                    # Sets Blender's render output filepath for the current image. This is where the next rendered image will be saved.
                    bpy.context.scene.render.filepath = os.path.join(weapon_position_folder, fileName)                
                    # This is the actual rendering process.
                    # `animation=False` renders a single still image.
                    # `write_still=True` saves the rendered image to the specified `filepath`.
                    # The first `False` argument disables undo support for the operation.
                    renderFrame = bpy.ops.render.render
                    renderFrame(  False,
                                  animation     =False,
                                  write_still   =True)

                    # ----- Debugging
                    # TODO: Delete print
                    #print("position_folder:",position_folder)
                    # TODO: Delete print
                    print("fileName:",fileName)
                    # TODO: Delete print
                    print("weapon_folder:",weapon_folder)
                    # TODO: Delete print
                    print("weapon_position_folder:",weapon_position_folder)
                       
                    # After rendering the current weapon's sprite for this frame/angle, its collection is excluded again.
                    # This ensures only one weapon collection is active at any given time for subsequent renders.
                    collection.exclude = True
 
                # ----- Debugging
                # TODO: Delete print
                print("collectionName:",collectionName)
                # TODO: Delete print
                print("wovl:",wovl)
            
            # Resets the 'holdout' state of the creature collection to its original value.
            # This ensures the creature is visible again after weapon rendering is complete, if it was originally visible.
            if (holdout == False):
                # WARNING: This change to 'holdout' status will not be visibly reflected in the Blender GUI's Outliner.
                bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout = False
                
    def type7000_monster_old(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling 7000 monster_old type logic."""
        if (typeParameters.exclude == False):
             # Used to identify which sprite file is defined for which sequence
            sequences = {
                'WK':'G1', 'SC':'G1', 'SD':'G1', 'GH':'G1','DE':'G1', 'TW':'G1',
                'A1':'G2', 'CA':'G2', 'A3':'G3'
            }
            animationKey = sequences[typeParameters.animationKey] # Gets e.g. G1.
            
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                       
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
    
    def type9000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling 9000 type logic."""
        if (typeParameters.exclude == False):
            # Used to identify which sprite file is defined for which sequence
            sequences = {
                'SD':'G1', 'SC':'G1', 'WK':'G1',
                'A1':'G2', 'A2':'G2',
                'A3':'G3', 'GH':'G3', 'DE':'G3', 'TW':'G3'
            }
            animationKey = sequences[typeParameters.animationKey] # Gets e.g. G1.
            
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                       
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
        
    def typeA000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling A000 type logic."""
        if (typeParameters.exclude == False):
             # Used to identify which sprite file is defined for which sequence
            sequences = {
                'WK':'G1',
                'SD':'G2', 'SC':'G2', 'GH':'G3', 'DE':'G3', 'TW':'G3',
                'A1':'G2', 'A2':'G2', 'A3':'G3', 
            }
            animationKey = sequences[typeParameters.animationKey] # Gets e.g. G1.
            
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                       
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                          
    def typeB000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling B000 type logic."""
        if (typeParameters.exclude == False):
            # Used to identify which sprite file is defined for which sequence
            sequences = {
                'SC':'G1', 'SD':'G1', 'GH':'G1', 'DE':'G1', 'TW':'G1',
                'A1':'G2', 'CA':'G2', 'A3':'G2',
            }
            animationKey = sequences[typeParameters.animationKey]
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                       
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
        
    def typeC000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling C000 type logic."""
        if (typeParameters.exclude == False):
            # Used to identify which sprite file is defined for which sequence
            sequences = {
                'WK':'G1', 'SC':'G1', 'SD':'G1', 'GH':'G1', 'DE':'G1', 'TW':'G1',
                'A1':'G2', 'CA':'G2', 'A3':'G2',
            }
            animationKey = sequences[typeParameters.animationKey]
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}{animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                       
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
        
    def typeD000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling D000 type logic."""
        if (typeParameters.exclude == False):
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.                  
            fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"              
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)        
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
        
    def typeE000(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling E000 type logic."""     
        # ----- Deactivates/Activates collections      
        if (typeParameters.exclude == True):
            # Deactivates every collection found.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collection.exclude = True            
            # Activates only creature collection.
            bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].exclude = False
            # TODO:Delete!
            print("typeE000: Executing 'exclude' logic for E000 type.")
        else:
            # Constructs the filename for the current sprite, including prefix, resref, animation, position, and padded frame number.
            if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
            else:
                fileName = f"{typeParameters.prefixResref}{typeParameters.animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                          
            # Sets the scene's render output file path. This tells Blender where to save the next rendered image.                       
            bpy.context.scene.render.filepath = os.path.join(typeParameters.position_folder, fileName)            
            # This is the actual rendering process.
            # `animation=False` renders a single still image.
            # `write_still=True` saves the rendered image to the specified `filepath`.
            # The first `False` argument disables undo support for the operation.
            renderFrame = bpy.ops.render.render
            renderFrame(  False,
                          animation     =False,
                          write_still   =True)
                       
            # TODO:Delete!
            print("typeE000: Executing complex logic for E000 type.")
            # Stores the initial 'holdout' state of the creature collection before modification.
            # 'holdout' makes objects within the collection invisible during rendering without excluding them from the view layer. 
            holdout = bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout
            
            # ----- Debugging
            # TODO: Delete print
            print("holdout:",holdout)
                                            
            # Activates 'holdout' (invisibility for rendering) specifically for the creature collection.
            # This ensures only weapon sprites are rendered when collections are toggled.
            if (holdout == False):
                # WARNING: This change to 'holdout' status will not be visibly reflected in the Blender GUI's Outliner.
                bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout = True
            
            # Iterates through all top-level collections in the current view layer to manage their visibility.                   
            for collection in bpy.context.view_layer.layer_collection.children:
                collectionName  = collection.name
                # Finds the corresponding weapon key (e.g., 'A', 'B', 'C') for the collection name.
                # This key is also used as the <wovl> (weapon overlay) identifier in the filename.
                wovl = next((key for key,value in typeParameters.animationWeaponFolderNames.items() if value == collectionName), None)
                
                # Checks if the collection corresponds to a recognized weapon animation and if that weapon is enabled for rendering.
                if ( (wovl != None) and (typeParameters.animationWeaponToggles[wovl] == True) ):
                    # Deactivates exclusion for the current weapon collection, making it visible for rendering.
                    # All other weapon collections remain excluded (invisible) by default.
                    collection.exclude=False
                    
                    # Constructs the base output folder path for the current weapon.
                    weapon_folder = os.path.join(typeParameters.pathSaveAt, collectionName)
                    weapon_animation_folder = os.path.join(weapon_folder, typeParameters.animation)
                    
                    # Creates a subfolder for the specific weapon and camera angle.
                    weapon_position_folder = os.path.join(weapon_animation_folder, typeParameters.positionKey)                  
                    if not os.path.exists(weapon_position_folder):
                        os.makedirs(weapon_position_folder)
                    
                    # Constructs the full filename for the current sprite, incorporating prefix, weapon identifier (wovl),
                    # animation key, camera position, and zero-padded frame number. East-facing sprites get an 'E' suffix.
                    if(typeParameters.positionKey == 'east' or typeParameters.positionKey == 'south_east' or typeParameters.positionKey == 'north_east'):                     
                        fileName = f"{typeParameters.prefixResref}{wovl}{typeParameters.animationKey}E_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                    else:
                        fileName = f"{typeParameters.prefixResref}{wovl}{typeParameters.animationKey}_{typeParameters.positionKey}_{str(typeParameters.frame).zfill(5)}.png"
                        
                    # Sets Blender's render output filepath for the current image. This is where the next rendered image will be saved.
                    bpy.context.scene.render.filepath = os.path.join(weapon_position_folder, fileName)                
                    # This is the actual rendering process.
                    # `animation=False` renders a single still image.
                    # `write_still=True` saves the rendered image to the specified `filepath`.
                    # The first `False` argument disables undo support for the operation.
                    renderFrame = bpy.ops.render.render
                    renderFrame(  False,
                                  animation     =False,
                                  write_still   =True)

                    # ----- Debugging
                    # TODO: Delete print
                    #print("position_folder:",position_folder)
                    # TODO: Delete print
                    print("fileName:",fileName)
                    # TODO: Delete print
                    print("weapon_folder:",weapon_folder)
                    # TODO: Delete print
                    print("weapon_position_folder:",weapon_position_folder)
                       
                    # After rendering the current weapon's sprite for this frame/angle, its collection is excluded again.
                    # This ensures only one weapon collection is active at any given time for subsequent renders.
                    collection.exclude = True
 
                # ----- Debugging
                # TODO: Delete print
                print("collectionName:",collectionName)
                # TODO: Delete print
                print("wovl:",wovl)
            
            # Resets the 'holdout' state of the creature collection to its original value.
            # This ensures the creature is visible again after weapon rendering is complete, if it was originally visible.
            if (holdout == False):
                # WARNING: This change to 'holdout' status will not be visibly reflected in the Blender GUI's Outliner.
                bpy.context.view_layer.layer_collection.children[typeParameters.CreatureCollectionName].holdout = False                  
        
    def typeNone(self, typeParameters:IEAS_AnimationTypesParameters):
        """Method for handling no type logic."""
        print("No animation type found. This shouldn't happen!")


# --------
# Purpose:
# --------
# Defines a PropertyGroup to hold all custom properties (settings and inputs) for the add-on's UI.
# These properties are accessible via `context.scene.IEAS_properties`.
# ------------------------------------------------------------------------------------------------
class IEAS_PGT_Inputs(PropertyGroup):
    """Group of input types which will be added into the other panels"""
    
    # --- Resets all camera and animation toggles to false.
    def resetToggles(self, context):
        # Lists with property names.
        cameraToggles = [
            'Use_SO', 'Use_SSW', 'Use_SW', 'Use_WSW', 'Use_WE', 'Use_WNW',
            'Use_NW', 'Use_NNW', 'Use_NO', 'Use_NNE', 'Use_NE', 'Use_ENE',
            'Use_ES', 'Use_ESE', 'Use_SE', 'Use_SSE'
        ]
        animationToggles = [
            'Use_A1', 'Use_A2', 'Use_A3', 'Use_A4', 'Use_A5', 'Use_CA', 'Use_DE',
            'Use_GH', 'Use_GU', 'Use_SC', 'Use_SD', 'Use_SL', 'Use_SP',
            'Use_TW', 'Use_WK', 'Use_Effect', 'Use_Emerge', 'Use_Hide',
        ]
        weaponToggles = [
            'Use_A', 'Use_B', 'Use_C', 'Use_D', 'Use_F', 'Use_H',
            'Use_M', 'Use_S', 'Use_W', 'Use_Q'
        ]
        
        # Resets all properties to false to prevent unwanted background sprite rendering.  
        for propertyName in cameraToggles:
            setattr(context.scene.IEAS_properties, propertyName, False)

        for propertyName in animationToggles:
            setattr(context.scene.IEAS_properties, propertyName, False)

        for propertyName in weaponToggles:
            setattr(context.scene.IEAS_properties, propertyName, False)

    # --- Updates the user-specified resolution X input from IE Autospriter to Output Properties and vice versa
    def updateResolutionX(self, context):
        bpy.context.scene.render.resolution_x = context.scene.IEAS_properties.Resolution_X
        #TODO: delete prints
        print("bpy resX:",bpy.context.scene.render.resolution_x)
        print("resX:",context.scene.IEAS_properties.Resolution_X)
    
    # --- Updates the user-specified resolution Y input from IE Autospriter to Output Properties and vice versa
    def updateResolutionY(self, context):
        bpy.context.scene.render.resolution_y = context.scene.IEAS_properties.Resolution_Y
                    
    # --- Step 1: Global Parameters    
    # File path property for saving rendered sprites.
    Save_at:        bpy.props.StringProperty(name="Save at",subtype='DIR_PATH') # File-opener
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
    # (unique identifier, property name, property description, icon identifier, number)
    Type:   bpy.props.EnumProperty(
                                    items=[
                                        ('0000','0000','','',0),
                                        ('1000 monster quadrant','1000 monster quadrant','','',1),
                                        ('1000 monster multi split bams 0','1000 monster multi split bams 0','','',2),
                                        ('1000 monster multi split bams 1','1000 monster multi split bams 1','','',3),
                                        ('1000 multi new split bams 0','1000 multi new split bams 0','','',4),
                                        ('1000 multi new split bams 1','1000 multi new split bams 1','','',5),
                                        ('2000','2000','','',6),
                                        ('3000 mirror 0','3000 mirror 0','','',7),
                                        ('3000 mirror 1','3000 mirror 1','','',8),
                                        ('7000 monster split bams 0','7000 monster split bams 0','','',9),
                                        ('7000 monster split bams 1','7000 monster split bams 1','','',10),
                                        ('7000 monster old','7000 monster old','','',11),
                                        ('4000','4000','','',12),
                                        ('9000','9000','','',13),
                                        ('A000','A000','','',14),
                                        ('B000','B000','','',15),
                                        ('C000','C000','','',16),
                                        ('D000','D000','','',17),
                                        ('E000','E000','','',18),
                                        # TODO: Delete unique identifier
                                        ('unique identifier', 'property name', 'property description', 'icon identifier', 19),
                                    ],
                                    name            = "Animationtype",
                                    description     = "TODO: Enum Name Description",
                                    default         = 'E000',
                                    update          = resetToggles
                                    )
    # Integer property for the render resolution in X-dimension.
    Resolution_X:   bpy.props.IntProperty(  name    = "Resolution X",
                                            default = 256,
                                            min     = 1,
                                            update  = updateResolutionX)
    # Integer property for the render resolution in Y-dimension.
    Resolution_Y:   bpy.props.IntProperty(  name    = "Resolution Y",
                                            default = 256,
                                            min     = 1,
                                            update  = updateResolutionY)
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
    South:              bpy.props.StringProperty(name="Subfolder S", default="south")
    South_South_West:   bpy.props.StringProperty(name="Subfolder SSW", default="south_south_west")
    South_West:         bpy.props.StringProperty(name="Subfolder SW", default="south_west")
    West_South_West:    bpy.props.StringProperty(name="Subfolder WSW", default="west_south_west")
    West:               bpy.props.StringProperty(name="Subfolder W", default="west")
    West_North_West:    bpy.props.StringProperty(name="Subfolder WNW", default="west_north_west")
    North_West:         bpy.props.StringProperty(name="Subfolder NW", default="noth_west")
    North_North_West:   bpy.props.StringProperty(name="Subfolder NNW", default="north_noth_west")
    North:              bpy.props.StringProperty(name="Subfolder N", default="north")
    North_North_East:   bpy.props.StringProperty(name="Subfolder NNE", default="north_north_east")
    North_East:         bpy.props.StringProperty(name="Subfolder NE", default="north_east")
    East_North_East:    bpy.props.StringProperty(name="Subfolder ENE", default="east_north_east")
    East:               bpy.props.StringProperty(name="Subfolder E", default="east")
    East_South_East:    bpy.props.StringProperty(name="Subfolder ESE", default="east_south_east")
    South_East:         bpy.props.StringProperty(name="Subfolder SE", default="south_east")
    South_South_East:   bpy.props.StringProperty(name="Subfolder SSE", default="south_south_east")
    # Boolean toggles for rendering each camera direction.
    Use_SO:     bpy.props.BoolProperty(name="Use S",    default=True)
    Use_SSW:    bpy.props.BoolProperty(name="Use SSW",  default=False)
    Use_SW:     bpy.props.BoolProperty(name="Use SW",   default=True)
    Use_WSW:    bpy.props.BoolProperty(name="Use WSW",  default=False)
    Use_WE:     bpy.props.BoolProperty(name="Use W",    default=True)
    Use_WNW:    bpy.props.BoolProperty(name="Use WNW",  default=False)
    Use_NW:     bpy.props.BoolProperty(name="Use NW",   default=True)
    Use_NNW:    bpy.props.BoolProperty(name="Use NNW",  default=False)
    Use_NO:     bpy.props.BoolProperty(name="Use N",    default=True)
    Use_NNE:    bpy.props.BoolProperty(name="Use NNE",  default=False)
    Use_NE:     bpy.props.BoolProperty(name="Use NE",   default=True)
    Use_ENE:    bpy.props.BoolProperty(name="Use ENE",  default=False)
    Use_ES:     bpy.props.BoolProperty(name="Use E",    default=True)
    Use_ESE:    bpy.props.BoolProperty(name="Use ESE",  default=False)
    Use_SE:     bpy.props.BoolProperty(name="Use SE",   default=True)
    Use_SSE:    bpy.props.BoolProperty(name="Use SSE",  default=False)    
    # --- Step 4: Animation (Animation Names and Toggles)
    # String properties for names of various animation actions.
    Attack1:    bpy.props.StringProperty(name="A1", default="slash")
    Attack2:    bpy.props.StringProperty(name="A2", default="stab")
    Attack3:    bpy.props.StringProperty(name="A3", default="strike")
    Attack4:    bpy.props.StringProperty(name="A4", default="throw")
    Attack5:    bpy.props.StringProperty(name="A5", default="unused?")
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
    # String property for unique effect animation(e.g. Ankheg)
    Emerge:     bpy.props.StringProperty(name="EMERGE", default="emerge")
    Hide:       bpy.props.StringProperty(name="HIDE",  default="hide")    
    # String property for unique effect animation(e.g. visual effects,spell effects or body parts of exploding creatures)
    Effect:     bpy.props.StringProperty(name="Effect", default="")   
    # String properties for names of various weapon animations based on the collection names.
    Creature:           bpy.props.StringProperty(name="Creature Main", default="")
    Creature_Lower:     bpy.props.StringProperty(name="Creature Lower", default="")
    Axe:                bpy.props.StringProperty(name="A", default="axe")
    Bow:                bpy.props.StringProperty(name="B", default="bow")
    Club:               bpy.props.StringProperty(name="C", default="club")
    Dagger:             bpy.props.StringProperty(name="D", default="dagger")
    Flail:              bpy.props.StringProperty(name="F", default="flail")
    Halberd:            bpy.props.StringProperty(name="H", default="halberd")
    Mace:               bpy.props.StringProperty(name="M", default="mace")
    Sword:              bpy.props.StringProperty(name="S", default="sword")
    Warhammer:          bpy.props.StringProperty(name="W", default="warhammer")
    Quarterstaff:       bpy.props.StringProperty(name="Q", default="quarterstaff")
    # Boolean toggles for rendering each animation.
    Use_A1:     bpy.props.BoolProperty(name="Use A1",   default=True)
    Use_A2:     bpy.props.BoolProperty(name="Use A2",   default=True)
    Use_A3:     bpy.props.BoolProperty(name="Use A3",   default=True)
    Use_A4:     bpy.props.BoolProperty(name="Use A4",   default=True)
    Use_A5:     bpy.props.BoolProperty(name="Use A5",   default=True)
    Use_CA:     bpy.props.BoolProperty(name="Use CA",   default=True)
    Use_DE:     bpy.props.BoolProperty(name="Use DE",   default=True)
    Use_GH:     bpy.props.BoolProperty(name="Use GH",   default=True)
    Use_GU:     bpy.props.BoolProperty(name="Use GU",   default=True)
    Use_SC:     bpy.props.BoolProperty(name="Use SC",   default=True)
    Use_SD:     bpy.props.BoolProperty(name="Use SD",   default=True)
    Use_SL:     bpy.props.BoolProperty(name="Use SL",   default=True)
    Use_SP:     bpy.props.BoolProperty(name="Use SP",   default=True)
    Use_TW:     bpy.props.BoolProperty(name="Use TW",   default=True)
    Use_WK:     bpy.props.BoolProperty(name="Use WK",   default=True)
    # Boolean toggles for unique effect animation(e.g. Ankheg)
    Use_Emerge: bpy.props.BoolProperty(name="Use EMERGE", default=True)
    Use_Hide:   bpy.props.BoolProperty(name="Use HIDE",   default=True)
    # Boolean toggles for unique effect animation(e.g. visual effects,spell effects or body parts of exploding creatures)
    Use_Effect: bpy.props.BoolProperty(name="Use Effect", default=False)
    # Boolean toggles to render each weapon animation with the selected creature animation.
    Use_A:      bpy.props.BoolProperty(name="Use A",    default=False)
    Use_B:      bpy.props.BoolProperty(name="Use B",    default=False)
    Use_C:      bpy.props.BoolProperty(name="Use C",    default=False)
    Use_D:      bpy.props.BoolProperty(name="Use D",    default=False)
    Use_F:      bpy.props.BoolProperty(name="Use F",    default=False)
    Use_H:      bpy.props.BoolProperty(name="Use H",    default=False)
    Use_M:      bpy.props.BoolProperty(name="Use M",    default=False)
    Use_S:      bpy.props.BoolProperty(name="Use S",    default=False)
    Use_W:      bpy.props.BoolProperty(name="Use W",    default=False)
    Use_Q:      bpy.props.BoolProperty(name="Use Q",    default=False)
    
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
                
        # TODO:Sanity chekc needs Testing
#        if not Principled_BSDF or not Material_Output:
#            self.report({'ERROR'}, "Principled BSDF or Material Output node not found. Please check names in settings.")
#            return {'CANCELLED'}
        
        # Creates the new nodes (Mix Shader and Bright/Contrast) and positions them near the Principled BSDF node.
        x           = 0
        x_location  = Principled_BSDF.location[x]
        x_offset    = 250
        y_location  = -100
        MixShader_node                  = activeMaterial.node_tree.nodes.new('ShaderNodeMixShader')
        MixShader_node.location         = (x_location, y_location)
        BrightContrast_node             = activeMaterial.node_tree.nodes.new('ShaderNodeBrightContrast')
        BrightContrast_node.location    = (x_location+x_offset, y_location)
        
        # Connects the newly created nodes and existing nodes to form the desired shader graph.
        activeMaterial.node_tree.links.new(Principled_BSDF.outputs[0],MixShader_node.inputs[1])
        activeMaterial.node_tree.links.new(MixShader_node.outputs[0],Material_Output.inputs[0])
        activeMaterial.node_tree.links.new(BrightContrast_node.outputs[0],MixShader_node.inputs[2])
        
        # Sets default values for the new nodes' inputs, based on typical(??) IE sprite requirements.
        fac     = 0
        bright  = 1    
        MixShader_node.inputs[fac].default_value            = 0.010
        BrightContrast_node.inputs[bright].default_value    = 1.000
        
        return {'FINISHED'}


# --------
# Purpose:
# --------
# Operator to initiate the full sprite rendering process for selected objects, animations, and directions.
# --------------------------------------------------------------------------------------------------------
class IEAS_OT_Final(Operator):
    """This class offers a function which starts the rendering which is used in "IEAS_PT_Final" class."""
    bl_idname = "ieas.final" # Unique identifier for the operator. Naming convention(??): <lower_case>.<lower_case>[_<lower_case>]
    bl_label = "RENDER" # Text displayed on the button in the UI.
    
    # Blender specific function which is executed in this case when RENDER button is pressed
    def execute(self, context):
        # ---- Start timer
        startTimer = time.time()
        
        # ----- Global
        animationTypeHandlers = {
            '0000':                                 IEAS_AnimationTypes().type0000,
            '1000 monster quadrant':                IEAS_AnimationTypes().type1000_monster_quadrant,
            '1000 monster multi split bams 0':      IEAS_AnimationTypes().type1000_monster_multi_sp0,
            '1000 monster multi split bams 1':      IEAS_AnimationTypes().type1000_monster_multi_sp1,
            '1000 multi new split bams 0':          IEAS_AnimationTypes().type1000_multi_new_sp0,
            '1000 multi new split bams 1':          IEAS_AnimationTypes().type1000_multi_new_sp1,
            '2000':                                 IEAS_AnimationTypes().type2000,
            '3000 mirror 0':                        IEAS_AnimationTypes().type3000_mirror0,
            '3000 mirror 1':                        IEAS_AnimationTypes().type3000_mirror1,
            '4000':                                 IEAS_AnimationTypes().type4000,
            '7000 monster split bams 0':            IEAS_AnimationTypes().type7000_monster_sp0,
            '7000 monster split bams 1':            IEAS_AnimationTypes().type7000_monster_sp1,
            '7000 monster old':                     IEAS_AnimationTypes().type7000_monster_old,
            '9000':                                 IEAS_AnimationTypes().type9000,
            'A000':                                 IEAS_AnimationTypes().typeA000,
            'B000':                                 IEAS_AnimationTypes().typeB000,
            'C000':                                 IEAS_AnimationTypes().typeC000,
            'D000':                                 IEAS_AnimationTypes().typeD000,
            'E000':                                 IEAS_AnimationTypes().typeE000,
            'unique identifier':                    False, # TODO: delete 'unique identifier'
        }
                   
        # ---- Camera
        # Dictionaries mapping internal keys to user-defined subfolder names and toggle states for camera angles.
        cameraPosFolderNames = {
            'south':        context.scene.IEAS_properties.South,        'south_south_west': context.scene.IEAS_properties.South_South_West,
            'south_west':   context.scene.IEAS_properties.South_West,   'west_south_west':  context.scene.IEAS_properties.West_South_West,
            'west':         context.scene.IEAS_properties.West,         'west_north_west':  context.scene.IEAS_properties.West_North_West,
            'north_west':   context.scene.IEAS_properties.North_West,   'north_north_west': context.scene.IEAS_properties.North_North_West,
            'north':        context.scene.IEAS_properties.North,        'north_north_east': context.scene.IEAS_properties.North_North_East,
            'north_east':   context.scene.IEAS_properties.North_East,   'east_north_east':  context.scene.IEAS_properties.East_North_East,
            'east':         context.scene.IEAS_properties.East,         'east_south_east':  context.scene.IEAS_properties.East_South_East,
            'south_east':   context.scene.IEAS_properties.South_East,   'south_south_east': context.scene.IEAS_properties.South_South_East
        }
        cameraPosToggles = {
            'south':        context.scene.IEAS_properties.Use_SO, 'south_south_west':   context.scene.IEAS_properties.Use_SSW,
            'south_west':   context.scene.IEAS_properties.Use_SW, 'west_south_west':    context.scene.IEAS_properties.Use_WSW,
            'west':         context.scene.IEAS_properties.Use_WE, 'west_north_west':    context.scene.IEAS_properties.Use_WNW,
            'north_west':   context.scene.IEAS_properties.Use_NW, 'north_north_west':   context.scene.IEAS_properties.Use_NNW,
            'north':        context.scene.IEAS_properties.Use_NO, 'north_north_east':   context.scene.IEAS_properties.Use_NNE,
            'north_east':   context.scene.IEAS_properties.Use_NE, 'east_north_east':    context.scene.IEAS_properties.Use_ENE,
            'east':         context.scene.IEAS_properties.Use_ES, 'east_south_east':    context.scene.IEAS_properties.Use_ESE,
            'south_east':   context.scene.IEAS_properties.Use_SE, 'south_south_east':   context.scene.IEAS_properties.Use_SSE
        }
        # Dictionary mapping internal keys to rotation angles in degrees.
        cameraAngles = {
            'south':        0,      'south_south_west': 337.5,
            'south_west':   315,    'west_south_west':  292.5,
            'west':         270,    'west_north_west':  247.5,
            'north_west':   225,    'north_north_west': 202.5,
            'north':        180,    'north_north_east': 157.5,
            'north_east':   135,    'east_north_east':  112.5,
            'east':         90,     'east_south_east':  67.5,
            'south_east':   45,     'south_south_east': 22.5
        }
        
        # ----- Animation
        # Dictionaries mapping internal keys to user-defined animation names and toggle states.
        animationFolderNames = {
            'A1':       context.scene.IEAS_properties.Attack1,    'A2': context.scene.IEAS_properties.Attack2,
            'A3':       context.scene.IEAS_properties.Attack3,    'A4': context.scene.IEAS_properties.Attack4,
            'CA':       context.scene.IEAS_properties.Cast,       'DE': context.scene.IEAS_properties.Death,
            'GH':       context.scene.IEAS_properties.Get_Hit,    'GU': context.scene.IEAS_properties.Get_Up,
            'SC':       context.scene.IEAS_properties.Ready,      'SD': context.scene.IEAS_properties.Idle,
            'SL':       context.scene.IEAS_properties.Sleep,      'SP': context.scene.IEAS_properties.Conjure,
            'TW':       context.scene.IEAS_properties.Dead,       'WK': context.scene.IEAS_properties.Walk,
            'Effect':   context.scene.IEAS_properties.Effect,     'EMERGE': context.scene.IEAS_properties.Emerge,
            'HIDE':     context.scene.IEAS_properties.Hide  
        }
        animationToggles = {
            'A1':       context.scene.IEAS_properties.Use_A1,     'A2': context.scene.IEAS_properties.Use_A2,
            'A3':       context.scene.IEAS_properties.Use_A3,     'A4': context.scene.IEAS_properties.Use_A4,
            'CA':       context.scene.IEAS_properties.Use_CA,     'DE': context.scene.IEAS_properties.Use_DE,
            'GH':       context.scene.IEAS_properties.Use_GH,     'GU': context.scene.IEAS_properties.Use_GU,
            'SC':       context.scene.IEAS_properties.Use_SC,     'SD': context.scene.IEAS_properties.Use_SD,
            'SL':       context.scene.IEAS_properties.Use_SL,     'SP': context.scene.IEAS_properties.Use_SP,
            'TW':       context.scene.IEAS_properties.Use_TW,     'WK': context.scene.IEAS_properties.Use_WK,
            'Effect':   context.scene.IEAS_properties.Use_Effect, 'EMERGE': context.scene.IEAS_properties.Use_Emerge,
            'HIDE':     context.scene.IEAS_properties.Use_Hide             
        }
        animationWeaponFolderNames = {
            'A': context.scene.IEAS_properties.Axe,     'B': context.scene.IEAS_properties.Bow,
            'C': context.scene.IEAS_properties.Club,    'D': context.scene.IEAS_properties.Dagger,
            'F': context.scene.IEAS_properties.Flail,   'H': context.scene.IEAS_properties.Halberd,
            'M': context.scene.IEAS_properties.Mace,    'S': context.scene.IEAS_properties.Sword,
            'W': context.scene.IEAS_properties.Warhammer, 'Q': context.scene.IEAS_properties.Quarterstaff,          
        }
        animationWeaponToggles = {
            'A': context.scene.IEAS_properties.Use_A,   'B': context.scene.IEAS_properties.Use_B,
            'C': context.scene.IEAS_properties.Use_C,   'D': context.scene.IEAS_properties.Use_D,
            'F': context.scene.IEAS_properties.Use_F,   'H': context.scene.IEAS_properties.Use_H,
            'M': context.scene.IEAS_properties.Use_M,   'S': context.scene.IEAS_properties.Use_S,
            'W': context.scene.IEAS_properties.Use_W,   'Q': context.scene.IEAS_properties.Use_Q,          
        }
        
        # ----- Resolution balancing in Blender and IE AutoSpriter, with Blender taking priority here.
        if (context.scene.IEAS_properties.Resolution_X != bpy.context.scene.render.resolution_x):
            context.scene.IEAS_properties.Resolution_X = bpy.context.scene.render.resolution_x
                       
        if (context.scene.IEAS_properties.Resolution_Y != bpy.context.scene.render.resolution_y):
            context.scene.IEAS_properties.Resolution_Y = bpy.context.scene.render.resolution_y
        
        # ----- Filename and path
        # Retrieves the base save path from user input.            
        pathSaveAt      = bpy.path.abspath(context.scene.IEAS_properties.Save_at)
        # Combines prefix and resref for use in filename construction.      
        prefixResref    = context.scene.IEAS_properties.Prefix + context.scene.IEAS_properties.Resref
        
        # ----- Init varibales(order is relevant)
        # Retrieves the animation type name of the type list from the UI settings.
        selectedType    = context.window_manager.IEAS_properties.Type
        # Retrieves the name of the object selected in the UI.       
        objectName      = context.scene.IEAS_properties.Object_List.name
        # Selects the specific object by setting its selection state to True.
        bpy.context.scene.objects[objectName].select_set(True)
        # Sets the selected object as the active object, crucial for operations relying on `bpy.context.active_object`.
        bpy.context.view_layer.objects.active = bpy.data.objects[objectName]
        # The index '2' corresponds to the Z-axis in Blender's rotation_euler tuple.        
        axis_Z                  = 2
        # Stores the object's initial Z-axis rotation to be restored at the end of the method.
        originalLocation        = bpy.context.active_object.rotation_euler[axis_Z]
        # Initilaizes the all parameters.
        typeParameters          = IEAS_AnimationTypesParameters(
            exclude                     = True,
            # Retrieves the name of the creature collection from the UI settings.
            CreatureCollectionName      = context.scene.IEAS_properties.Creature,
            CreatureCollectionNameLP    = context.scene.IEAS_properties.Creature_Lower,
            animationWeaponFolderNames  = animationWeaponFolderNames,
            animationWeaponToggles      = animationWeaponToggles,
            pathSaveAt                  = pathSaveAt,
            animation                   = "",
            positionKey                 = "",
            animationKey                = "",
            frame                       = 0,
            prefixResref                = prefixResref,
            position_folder             = ""
        )
        if (selectedType == 'E000' or selectedType == '2000' or 
            selectedType == '3000 mirror 0' or selectedType == '3000 mirror 1' or
            selectedType == '7000 monster split bams 0' or selectedType == '7000 monster split bams 1'):
            # Get the method from the dictionary, defaulting to a general handler if not found
            handler_method  = animationTypeHandlers.get(selectedType, IEAS_AnimationTypes().typeNone)
            handler_method(typeParameters)
                        
        # ----- Deselecting and selecting
        # Deselects all objects in the scene to ensure only the target object is affected.
        bpy.ops.object.select_all(action='DESELECT')
        # Selects the specific object by setting its selection state to True.
        bpy.context.scene.objects[objectName].select_set(True)
        # Sets the selected object as the active object, crucial for operations relying on `bpy.context.active_object`.
        bpy.context.view_layer.objects.active = bpy.data.objects[objectName]
        
        # ----- Debugging 
        # TODO: Delete print
        print("--------IEAS_OT_Final----------")
        # TODO: Delete print
        #print("CreatureCollectionName:",CreatureCollectionName)
        # TODO: Delete print
        print("pathSaveAt:",pathSaveAt)
        # TODO: Delete print
        print("prefixResref:",prefixResref)
        # TODO: Delete print
        print("Object List:",context.scene.IEAS_properties.Object_List.name) 
        # TODO: Delete print      
        print("selectedType:",selectedType)

        # ----- Main/Outer loop 
        # Iterates through each defined animation.  
        for animationKey, animation in animationFolderNames.items():
            # Attempts to get the animation action data block.
            bpy.context.active_object.animation_data.action = bpy.data.actions.get(animation)
            currentAction = bpy.context.active_object.animation_data.action
            
            # Proceeds only if the animation is enabled by the user and the action exists in Blender. 
            if(animationToggles[animationKey] == True and currentAction != None):               
                # Assigns the current animation action to the active object's animation data.
                bpy.context.active_object.animation_data.action = bpy.data.actions.get(animation)               
                # Sets the scene's end frame to match the animation's end frame, converted to an integer
                # to prevent rendering empty frames beyond the action's actual length.
                bpy.context.scene.frame_end = int(bpy.context.active_object.animation_data.action.frame_range[1])     
                # Constructs the base folder path for the current animation.
                animation_folder = os.path.join(pathSaveAt, "00-"+animation)
                
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
                        bpy.context.active_object.rotation_euler[axis_Z] = math.radians(cameraAngles[positionKey]) 
                        
                        # ----- Debugging
                        # TODO: Delete print
                         #print("\nbpy.context.active_object.rotation_euler:",bpy.context.active_object.rotation_euler)
                        # TODO: Delete print
                        #print("\nbpy.context.active_object.rotation_euler[2]:",bpy.context.active_object.rotation_euler[2])
                
                        # ----- Variables used in nested inner loop
                        frameStart      = bpy.context.scene.frame_start
                        frameEnd        = bpy.context.scene.frame_end+1
                        Every_X_Frame   = context.scene.IEAS_properties.Every_X_Frame
                        
                        #  ----- Nested/Inner loop 
                        # Loops through frames within the animation's range, stepping by 'Every_X_Frame'.
                        for frame in range(frameStart,frameEnd,Every_X_Frame):
                            # Sets the current frame of the scene, updating the object's animation pose.
                            bpy.context.scene.frame_current = frame
                                                       
                            # ----- Debugging
                            # TODO: Delete print
                            print("position_folder:",position_folder)
                            # TODO: Delete print
                            print("action:",bpy.context.active_object.animation_data.action)

                            
                            # TODO: need comment
                            typeParametersUpdated = replace(
                                typeParameters,
                                exclude                     = False,
                                animation                   = animation,
                                positionKey                 = positionKey,
                                animationKey                = animationKey, 
                                frame                       = frame,
                                position_folder             = position_folder,
                            )
                            
                            # Get the method from the dictionary, defaulting to a general handler if not found
                            handler_method  = animationTypeHandlers.get(selectedType, IEAS_AnimationTypes().typeNone)
                            handler_method(typeParametersUpdated)                        
                
        # Restore the object's Z-axis rotation to its original state
        bpy.context.active_object.rotation_euler[axis_Z] = originalLocation 
        
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
    bl_parent_id    = 'IEAS_PT_Core'        # Specifies the parent panel, making it a sub-panel of IEAS_PT_Core.
    bl_options      = {'DEFAULT_CLOSED'}    # Panel starts collapsed by default.
    
    # --- Blender specific function which places elements into GUI
    # This method draws the UI elements for global rendering parameters.
    def draw(self, context):
        # Instances by pointers: Draws UI elements linked to the properties defined in IEAS_PGT_Inputs.
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Save_at")
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Prefix")
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Resref")
        row = self.layout.row()
        # "True" displayes as radio buttons, not as drop-down list
        row.prop(context.window_manager.IEAS_properties, 'Type', expand=False)
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Object_List")
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Resolution_X")
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Resolution_Y")
        row = self.layout.row()
        row.prop(context.scene.IEAS_properties, "Every_X_Frame")
        
        
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
# This panel manages the output folders and defines which orientations (directions)
# will be rendered for the sprites.
# ---------------------------------------------------------------------------------
class IEAS_PT_Camera(Panel):
    """This step manages the output folders and defines which object orientations shown in the camera will be rendered."""
    
    # --- Blender specific class variables
    bl_label        = "Step 3: Camera" 
    bl_idname       = 'IEAS_PT_Camera'
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "IE AutoSpriter"
    bl_parent_id    = 'IEAS_PT_Core'
    bl_options      = {'DEFAULT_CLOSED'}
    # --- Blender specific function which places elements into GUI
    # This method draws the UI elements for camera settings.
    def draw(self, context):
        # --- All GUI elments as dict
        animationTypesActive = {
            '0000':                                 False,
            '1000 monster quadrant':                False,
            '1000 monster multi split bams 0':      False,
            '1000 monster multi split bams 1':      False,
            '1000 multi new split bams 0':          False,
            '1000 multi new split bams 1':          False,
            '2000':                                 False,
            '3000 mirror 0':                        False,
            '3000 mirror 1':                        False,
            '4000':                                 False,
            '7000 monster split bams 0':            False,
            '7000 monster split bams 1':            False,
            '7000 monster old':                     False,
            '9000':                                 False,
            'A000':                                 False,
            'B000':                                 False,
            'C000':                                 False,
            'D000':                                 False,
            'E000':                                 False,
            'unique identifier':                    False,# TODO: Delete unique identifier!
        }
        Toggles1 = {'South': context.scene.IEAS_properties.Use_SO}
        Toggles8 = {
            'South':        context.scene.IEAS_properties.Use_SO, 'South_West':   context.scene.IEAS_properties.Use_SW, 
            'West':         context.scene.IEAS_properties.Use_WE, 'North_West':   context.scene.IEAS_properties.Use_NW, 
            'North':        context.scene.IEAS_properties.Use_NO, 'North_East':   context.scene.IEAS_properties.Use_NE, 
            'East':         context.scene.IEAS_properties.Use_ES, 'South_East':   context.scene.IEAS_properties.Use_SE, 
        }
        Toggles9 = {
            'South':        context.scene.IEAS_properties.Use_SO, 'South_South_West':   context.scene.IEAS_properties.Use_SSW,
            'South_West':   context.scene.IEAS_properties.Use_SW, 'West_South_West':    context.scene.IEAS_properties.Use_WSW,
            'West':         context.scene.IEAS_properties.Use_WE, 'West_North_West':    context.scene.IEAS_properties.Use_WNW,
            'North_West':   context.scene.IEAS_properties.Use_NW, 'North_North_West':   context.scene.IEAS_properties.Use_NNW,
            'North':        context.scene.IEAS_properties.Use_NO,
        }
        Toggles16 = {
            'South':        context.scene.IEAS_properties.Use_SO, 'South_South_West':   context.scene.IEAS_properties.Use_SSW,
            'South_West':   context.scene.IEAS_properties.Use_SW, 'West_South_West':    context.scene.IEAS_properties.Use_WSW,
            'West':         context.scene.IEAS_properties.Use_WE, 'West_North_West':    context.scene.IEAS_properties.Use_WNW,
            'North_West':   context.scene.IEAS_properties.Use_NW, 'North_North_West':   context.scene.IEAS_properties.Use_NNW,
            'North':        context.scene.IEAS_properties.Use_NO, 'North_North_East':   context.scene.IEAS_properties.Use_NNE,
            'North_East':   context.scene.IEAS_properties.Use_NE, 'East_North_East':    context.scene.IEAS_properties.Use_ENE,
            'East':         context.scene.IEAS_properties.Use_ES, 'East_South_East':    context.scene.IEAS_properties.Use_ESE,
            'South_East':   context.scene.IEAS_properties.Use_SE, 'South_South_East':   context.scene.IEAS_properties.Use_SSE
        }
        ToggleNames = {
            'South':        'Use_SO', 'South_South_West': 'Use_SSW',
            'South_West':   'Use_SW', 'West_South_West':  'Use_WSW',
            'West':         'Use_WE', 'West_North_West':  'Use_WNW',
            'North_West':   'Use_NW', 'North_North_West': 'Use_NNW',
            'North':        'Use_NO', 'North_North_East': 'Use_NNE',
            'North_East':   'Use_NE', 'East_North_East':  'Use_ENE',
            'East':         'Use_ES', 'East_South_East':  'Use_ESE',
            'South_East':   'Use_SE', 'South_South_East': 'Use_SSE'
        }
                
        # --- Reset and activate
        activeType = context.window_manager.IEAS_properties.Type
        # Reset active types to false
        for animationTypeKey in animationTypesActive:
            animationTypesActive[animationTypeKey] = False
        # Set active type to true
        animationTypesActive[activeType] = True
        
        # --- Creates rows for each direction, displaying the subfolder name input and a toggle.
        if (animationTypesActive['0000']):
            for orientationKey, toggle in Toggles1.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, orientationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[orientationKey])
                
        if (animationTypesActive['4000'] or animationTypesActive['A000'] or 
            animationTypesActive['1000 monster quadrant']):
            for orientationKey, toggle in Toggles16.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, orientationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[orientationKey])
                
        if (animationTypesActive['9000'] or animationTypesActive['B000'] or 
            animationTypesActive['C000'] or animationTypesActive['E000'] or
            animationTypesActive['2000'] or animationTypesActive['3000 mirror 0'] or
            animationTypesActive['7000 monster old']):
            for orientationKey, toggle in Toggles8.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, orientationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[orientationKey])
            
        if (animationTypesActive['D000'] or 
            animationTypesActive['1000 monster multi split bams 0'] or animationTypesActive['1000 monster multi split bams 1'] or 
            animationTypesActive['1000 multi new split bams 0']     or animationTypesActive['1000 multi new split bams 1'] or
            animationTypesActive['3000 mirror 1'] or animationTypesActive['7000 monster split bams 0'] or 
            animationTypesActive['7000 monster split bams 1']):
            for orientationKey, toggle in Toggles9.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, orientationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[orientationKey])


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
        # --- All GUI elments as dict
        animationTypesActive = {
            '0000':                                 False,
            '1000 monster quadrant':                False,
            '1000 monster multi split bams 0':      False,
            '1000 monster multi split bams 1':      False,
            '1000 multi new split bams 0':          False,
            '1000 multi new split bams 1':          False,
            '2000':                                 False,
            '3000 mirror 0':                        False,
            '3000 mirror 1':                        False,
            '4000':                                 False,
            '7000 monster split bams 0':            False,
            '7000 monster split bams 1':            False,
            '7000 monster old':                     False,
            '9000':                                 False,
            'A000':                                 False,
            'B000':                                 False,
            'C000':                                 False,
            'D000':                                 False,
            'E000':                                 False,
            'unique identifier':                    False,# TODO: Delete unique identifier!
        }
        Toggles0000 = {
            'Effect':   context.scene.IEAS_properties.Use_Effect           
        }
        Toggles1000_monster_quadrant = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        Toggles1000_monster_multi_sp0 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Walk':     context.scene.IEAS_properties.Use_WK, 'Conjure':  context.scene.IEAS_properties.Use_SP,
            'Get_Up':   context.scene.IEAS_properties.Use_GU, 'Sleep':    context.scene.IEAS_properties.Use_SL,
            'Cast':     context.scene.IEAS_properties.Use_CA,
        }
        Toggles1000_monster_multi_sp1 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Walk':     context.scene.IEAS_properties.Use_WK, 'Conjure':  context.scene.IEAS_properties.Use_SP,
            'Get_Up':   context.scene.IEAS_properties.Use_GU, 'Sleep':    context.scene.IEAS_properties.Use_SL,
            'Cast':     context.scene.IEAS_properties.Use_CA,
        }
        Toggles1000_multi_new_sp0 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Attack4':  context.scene.IEAS_properties.Use_A4,
            'Attack5':  context.scene.IEAS_properties.Use_A5, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Walk':     context.scene.IEAS_properties.Use_WK, 'Conjure':  context.scene.IEAS_properties.Use_SP,
            'Cast':     context.scene.IEAS_properties.Use_CA,
        }
        Toggles1000_multi_new_sp1 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Attack4':  context.scene.IEAS_properties.Use_A4,
            'Attack5':  context.scene.IEAS_properties.Use_A5, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Walk':     context.scene.IEAS_properties.Use_WK, 'Conjure':  context.scene.IEAS_properties.Use_SP,
            'Cast':     context.scene.IEAS_properties.Use_CA,
        }
        Toggles2000 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Walk':     context.scene.IEAS_properties.Use_WK, 'Conjure':  context.scene.IEAS_properties.Use_SP,
            'Cast':     context.scene.IEAS_properties.Use_CA,
        }
        Toggles3000_mirror0 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1,       'Death':    context.scene.IEAS_properties.Use_DE,
            'Ready':    context.scene.IEAS_properties.Use_SC,       'Idle':     context.scene.IEAS_properties.Use_SD, 
            'Dead':     context.scene.IEAS_properties.Use_TW,       'Cast':     context.scene.IEAS_properties.Use_CA,
            'Emerge':   context.scene.IEAS_properties.Use_Emerge,   'Hide':     context.scene.IEAS_properties.Use_Hide,
        }
        Toggles3000_mirror1 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1,       'Death':    context.scene.IEAS_properties.Use_DE,
            'Ready':    context.scene.IEAS_properties.Use_SC,       'Idle':     context.scene.IEAS_properties.Use_SD, 
            'Dead':     context.scene.IEAS_properties.Use_TW,       'Cast':     context.scene.IEAS_properties.Use_CA,
            'Emerge':   context.scene.IEAS_properties.Use_Emerge,   'Hide':     context.scene.IEAS_properties.Use_Hide,
        }
        Toggles4000 = {
            'Death':    context.scene.IEAS_properties.Use_DE, 'Get_Hit':  context.scene.IEAS_properties.Use_GH,
            'Ready':    context.scene.IEAS_properties.Use_SC, 'Idle':     context.scene.IEAS_properties.Use_SD,
            'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        Toggles7000_monster_sp0 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Attack4':  context.scene.IEAS_properties.Use_A4,
            'Attack5':  context.scene.IEAS_properties.Use_A5, 'Conjure':  context.scene.IEAS_properties.Use_SP, 
            'Cast':     context.scene.IEAS_properties.Use_CA, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Get_Up':   context.scene.IEAS_properties.Use_GU, 'Sleep':    context.scene.IEAS_properties.Use_SL,
            'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        Toggles7000_monster_sp1 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Attack4':  context.scene.IEAS_properties.Use_A4,
            'Attack5':  context.scene.IEAS_properties.Use_A5, 'Conjure':  context.scene.IEAS_properties.Use_SP, 
            'Cast':     context.scene.IEAS_properties.Use_CA, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Get_Up':   context.scene.IEAS_properties.Use_GU, 'Sleep':    context.scene.IEAS_properties.Use_SL,
            'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        Toggles7000_monster_old = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack3':  context.scene.IEAS_properties.Use_A3, 
            'Cast':     context.scene.IEAS_properties.Use_CA, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW, 
            'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        Toggles9000 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        TogglesA000 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
            'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        TogglesB000 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack3':  context.scene.IEAS_properties.Use_A3, 
            'Cast':     context.scene.IEAS_properties.Use_CA, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC, 
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW,
        }
        TogglesC000 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack3':  context.scene.IEAS_properties.Use_A3,
            'Cast':     context.scene.IEAS_properties.Use_CA, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Ready':    context.scene.IEAS_properties.Use_SC,
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Dead':     context.scene.IEAS_properties.Use_TW, 
            'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        TogglesD000 = {
            'Idle':     context.scene.IEAS_properties.Use_SD, 'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        TogglesE000 = {
            'Attack1':  context.scene.IEAS_properties.Use_A1, 'Attack2':  context.scene.IEAS_properties.Use_A2,
            'Attack3':  context.scene.IEAS_properties.Use_A3, 'Attack4':  context.scene.IEAS_properties.Use_A4,
            'Cast':     context.scene.IEAS_properties.Use_CA, 'Death':    context.scene.IEAS_properties.Use_DE,
            'Get_Hit':  context.scene.IEAS_properties.Use_GH, 'Get_Up':   context.scene.IEAS_properties.Use_GU,
            'Ready':    context.scene.IEAS_properties.Use_SC, 'Idle':     context.scene.IEAS_properties.Use_SD,
            'Sleep':    context.scene.IEAS_properties.Use_SL, 'Conjure':  context.scene.IEAS_properties.Use_SP,
            'Dead':     context.scene.IEAS_properties.Use_TW, 'Walk':     context.scene.IEAS_properties.Use_WK,
        }
        ToggleNames = {
            'Attack1':  'Use_A1',       'Attack2':  'Use_A2',
            'Attack3':  'Use_A3',       'Attack4':  'Use_A4',
            'Attack5':  'Use_A5',       'Cast':     'Use_CA', 
            'Death':    'Use_DE',       'Get_Hit':  'Use_GH', 
            'Get_Up':   'Use_GU',       'Ready':    'Use_SC', 
            'Idle':     'Use_SD',       'Sleep':    'Use_SL',
            'Conjure':  'Use_SP',       'Dead':     'Use_TW', 
            'Walk':     'Use_WK',       'Effect':   'Use_Effect',
            'Emerge':   'Use_Emerge',   'Hide':     'Use_Hide',
        }
        
        # --- Reset and activate
        activeType = context.window_manager.IEAS_properties.Type
        # Reset active types to false
        for animationTypeKey in animationTypesActive:
            animationTypesActive[animationTypeKey] = False
        # Set active type to true
        animationTypesActive[activeType] = True
            
        # --- Creates rows for each direction, displaying the subfolder name input and a toggle.
        if (animationTypesActive['0000']):
            for animationKey, toggle in Toggles0000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
        
        if (animationTypesActive['1000 monster quadrant']):
            for animationKey, toggle in Toggles1000_monster_quadrant.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['1000 monster multi split bams 0']):
            for animationKey, toggle in Toggles1000_monster_multi_sp0.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['1000 monster multi split bams 1']):
            for animationKey, toggle in Toggles1000_monster_multi_sp1.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['1000 multi new split bams 0']):
            for animationKey, toggle in Toggles1000_multi_new_sp0.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['1000 multi new split bams 1']):
            for animationKey, toggle in Toggles1000_multi_new_sp0.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
        
        if (animationTypesActive['2000']):
            for animationKey, toggle in Toggles2000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
        
        if (animationTypesActive['3000 mirror 0']):
            for animationKey, toggle in Toggles3000_mirror0.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
        
        if (animationTypesActive['3000 mirror 1']):
            for animationKey, toggle in Toggles3000_mirror1.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
        
        if (animationTypesActive['4000']):
            for animationKey, toggle in Toggles4000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['7000 monster split bams 0']):
            for animationKey, toggle in Toggles7000_monster_sp0.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['7000 monster split bams 1']):
            for animationKey, toggle in Toggles7000_monster_sp1.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
        
        if (animationTypesActive['7000 monster old']):
            for animationKey, toggle in Toggles7000_monster_old.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['9000']):
            for animationKey, toggle in Toggles9000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
        
        if (animationTypesActive['A000']):
            for animationKey, toggle in TogglesA000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['B000']):
            for animationKey, toggle in TogglesB000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['C000']):
            for animationKey, toggle in TogglesC000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['D000']):
            for animationKey, toggle in TogglesD000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                
        if (animationTypesActive['E000']):
            for animationKey, toggle in TogglesE000.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, animationKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[animationKey])
                

# --------
# Purpose:
# --------
# This panel defines which weapon animations (Blender Collection) should be rendered
# and how their corresponding output folders/filenames will be named.
# ----------------------------------------------------------------------------------
class IEAS_PT_Collections(Panel):
    """This panel defines which weapon animations (Blender Collection) should be rendered and how they are named in the output."""
    
    # --- Blender specific class variables
    bl_label        = "Collections"
    bl_idname       = 'IEAS_PT_Collections'
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = "IE AutoSpriter"
    bl_parent_id    = 'IEAS_PT_Animation'
    bl_options      = {'DEFAULT_CLOSED'}
    # --- Blender specific function which places elements into GUI
    # This method draws the UI elements for animation selection and naming.
    def draw(self, context):       
        # --- All GUI elments as dict
        animationTypesActive = {
            '0000':                                 False,
            '1000 monster quadrant':                False,
            '1000 monster multi split bams 0':      False,
            '1000 monster multi split bams 1':      False,
            '1000 multi new split bams 0':          False,
            '1000 multi new split bams 1':          False,
            '2000':                                 False,
            '3000 mirror 0':                        False,
            '3000 mirror 1':                        False,
            '4000':                                 False,
            '7000 monster split bams 0':            False,
            '7000 monster split bams 1':            False,
            '7000 monster old':                     False,
            '9000':                                 False,
            'A000':                                 False,
            'B000':                                 False,
            'C000':                                 False,
            'D000':                                 False,
            'E000':                                 False,
            'unique identifier':                    False,# TODO: Delete unique identifier!
        }        
        ToggleWeapons = {
            'Axe':          context.scene.IEAS_properties.Use_A, 'Bow':          context.scene.IEAS_properties.Use_B,
            'Club':         context.scene.IEAS_properties.Use_C, 'Dagger':       context.scene.IEAS_properties.Use_D,
            'Flail':        context.scene.IEAS_properties.Use_F, 'Halberd':      context.scene.IEAS_properties.Use_H,
            'Mace':         context.scene.IEAS_properties.Use_M, 'Sword':        context.scene.IEAS_properties.Use_S,
            'Warhammer':    context.scene.IEAS_properties.Use_W, 'Quarterstaff': context.scene.IEAS_properties.Use_Q,
        }
        ToggleNames = {
            'Axe':          'Use_A',        'Bow':          'Use_B',
            'Club':         'Use_C',        'Dagger':       'Use_D',
            'Flail':        'Use_F',        'Halberd':      'Use_H',
            'Mace':         'Use_M',        'Sword':        'Use_S',
            'Warhammer':    'Use_W',        'Quarterstaff': 'Use_Q',
            'Effect':       'Use_Effect',
        }
        
        # --- Reset and activate
        activeType = context.window_manager.IEAS_properties.Type
        # Reset active types to false
        for animationTypeKey in animationTypesActive:
            animationTypesActive[animationTypeKey] = False
        # Set active type to true
        animationTypesActive[activeType] = True
            
        # --- Creates rows for each direction, displaying the subfolder name input and a toggle.
        if (animationTypesActive['E000'] or animationTypesActive['2000'] or
            animationTypesActive['7000 monster split bams 0'] or animationTypesActive['7000 monster split bams 1']):
            row = self.layout.row()
            row.prop(context.scene.IEAS_properties, "Creature")
            
            for weaponKey, toggle in ToggleWeapons.items():
                # Splits row into two columns            
                split       = self.layout.split(factor=0.7)
                row_input   = split.row() # Left/first column  
                row_toggle  = split.row() # Right/second column 
                # The text input is on the disabled row
                row_input.enabled = toggle
                row_input.prop(context.scene.IEAS_properties, weaponKey)
                # The toggle is on the enabled row
                row_toggle.prop(context.scene.IEAS_properties, ToggleNames[weaponKey])
        elif (animationTypesActive['3000 mirror 0'] or animationTypesActive['3000 mirror 1']):
            row = self.layout.row()
            row.prop(context.scene.IEAS_properties, "Creature")
            row = self.layout.row()
            row.prop(context.scene.IEAS_properties, "Creature_Lower")
        else:
            pass # Show no weapon animation options
        

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
    bpy.utils.register_class(IEAS_PT_Collections)
    bpy.utils.register_class(IEAS_PT_Final)
    
    # Pointers: Registers the PropertyGroup to the scene, making its properties accessible via `bpy.context.scene.IEAS_properties`.
    bpy.types.Scene.IEAS_properties         = bpy.props.PointerProperty(type=IEAS_PGT_Inputs)
    bpy.types.WindowManager.IEAS_properties = bpy.props.PointerProperty(type=IEAS_PGT_Inputs)

    
# --------
# Purpose:
# --------
# Unregisters all classes and cleans up custom properties when the add-on is disabled.
# This prevents data remnants and potential conflicts if the add-on is re-enabled or other add-ons are used(??).
def unregister():
    bpy.utils.unregister_class(IEAS_OT_ShadingNodes)
    bpy.utils.unregister_class(IEAS_OT_Final)
    bpy.utils.unregister_class(IEAS_PGT_Inputs)
    bpy.utils.unregister_class(IEAS_PT_Core)
    bpy.utils.unregister_class(IEAS_PT_GlobalParameters)
    bpy.utils.unregister_class(IEAS_PT_ShadingNodes)
    bpy.utils.unregister_class(IEAS_PT_Camera)
    bpy.utils.unregister_class(IEAS_PT_Animation)
    bpy.utils.unregister_class(IEAS_PT_Collections)
    bpy.utils.unregister_class(IEAS_PT_Final)
    
    # Deletes pointer
    del bpy.types.Scene.IEAS_properties
    del bpy.types.WindowManager.IEAS_properties
    

# --------
# Purpose:
# --------
# Controls script execution: if the script is run directly in Blender's text editor (as main),
# it will call the register function. This is standard practice for Blender add-ons. 
if __name__ == "__main__":
    register()