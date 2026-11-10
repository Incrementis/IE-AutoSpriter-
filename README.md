# IE-AutoSpriter-
Infinity Engine AutoSpriter is a Blender add-on that automates sprite creation from creature animations.

This is a work in progress and an beta release. This means that most things are implemented, but the add-on is still subject to heavy changes. Use this add-on with caution!!

Please use the latest release version instead of the latest commit.

This is also a learning project focused on my personal use and interest. Suggestions are welcome!

## Note
* Before rendering all animations in all directions, start with just one animation and one direction to see if everything works correctly. 
* The latest version of IE Autospriter for Blender 4.0 can be found in the branch "v0.36.3-legacy-for-blender4.0".
* Further versions will be implemented and tested on newer Blender 4.5.5 LTS. This also includes the manual.

## Beta Version:
* May not work or only work under special conditions.
* May not work due to missing information in the manual.
* May contain issues for various reasons.
* I am not a Blender or Blender API expert, so this may also cause issues.
* Currently only rudimentary tested with Blender 4.5.5 LTS version.
* The focus of the beta phase will be mainly on bug fixing.
* [Here](https://github.com/Incrementis/IE-AutoSpriter-/issues/52) you will find the currently known issues that will be fixed in the beta phase.

### Performance
The 4.5.5 LTS blend save files contain the appropriate settings.

#### Render engine "Cycles": 
* Not tested on Blender 4.5.5 LTS
* Rendering a frame took [0.8 to 1 seconds](https://github.com/Incrementis/IE-AutoSpriter-/issues/18#issuecomment-3079607164) (tested in blender 4.0)

#### Render engine "EEVEE":
* Not tested on Blender 4.5.5 LTS
* Rendering a frame took [0.05 seconds](https://github.com/Incrementis/IE-AutoSpriter-/issues/18#issuecomment-3079719096) (tested in blender 4.0)

## Discussion
* [Beamdog Forums](https://forums.beamdog.com/discussion/89525/blender-add-on-ie-autospriter)
* [G3 Forums](https://www.gibberlings3.net/forums/topic/39792-blender-add-on-ie-autospriter)
* [GitHub](https://github.com/Incrementis/IE-AutoSpriter-/discussions)

## Key Features
* Keeps parameters in a Blender file (reduces workflow)
* Automated rendering
* Provides steps for better usability
* Provides many useful parameters
* To make it work on higher Blender versions

## Guides
The functions are explained in detail in the manual.
* [manual.pdf](https://github.com/Incrementis/IE-AutoSpriter-/blob/main/manual.pdf)
* Please note that the demos are not intended as an ideal guide or tutorial. They are intended ONLY to demonstrate/test the features of IE Autospriter.

## Operating Systems
* Windows 11
* May also work on other platforms since Python is a platform-independent language

## Languages
* English

## Special Thanks
Thanks to "The Gibberlings 3" forum users, "Artisan's Corner" discord server users, SHS discord server users, Infinity Engine discord server users and Mystara discord server users who helped me with hints and information:
* The Artisan
* CamDawg
* Argent77
* exhuman
* moggadeet
* Bubb
* lynx
* skellytz
* FallDamage312
* Serpens
* Sam.

## Sources and Learning Materials
| Title | Author | Link |
| :--- | :--- | :--- |
| NearInfinity | Argent77 | https://github.com/Argent77/NearInfinity |
| INI file format: Creature Animations | --- | https://gibberlings3.github.io/iesdp/file_formats/ie_formats/ini_anim.htm |
| Avatar Naming Schemes | --- | https://gibberlings3.github.io/iesdp/appendices/avatarnaming.htm |
| IE-Animations | Artemiusl | https://github.com/ArtemiusI/IE-Animations |
| education/175-Blender-Properties | PageKey | https://github.com/pagekey/education/tree/main/175-Blender-Properties |
| Your Own Operator \| Scripting for Artists [8] | Blender | https://www.youtube.com/watch?v=xscQ9tcN4GI&list=LL |
| Render 8 Direction Animated Sprites in Blender with Python | FozleCC | https://www.youtube.com/watch?v=l1Io7fLYV4o |
| Blender documentations | Blender | https://docs.blender.org |
| Blender Rendering Optimization Tips | Ryo | https://whoisryosuke.com/blog/2024/blender-rendering-optimization-tips |
| Expressions in Blender 3D | ukramedia | https://www.youtube.com/watch?v=5IMFSC5h0a4 |
| Creating radio buttons in the Blender add-ons interface | Nikita | https://b3d.interplanety.org/en/creating-radio-buttons-in-the-blender-add-ons-interface/ |
| Add a Predefined Meta-Rig | blender | https://docs.blender.org/manual/en/2.81/addons/rigging/rigify.html?highlight=horse |
| Make Animals In Blender 3 - The Easy Way | Grant Abbitt (Gabbitt) | https://www.youtube.com/watch?v=tEZOXuDhTJ0 |
| Make a Detailed Sword in Blender :Topology Tips & Hard Surface Techniques | Grant Abbitt(Gabbitt) | https://www.youtube.com/watch?v=f320TtEpGYQ |
| Create Low Poly Characters in Blender (Beginner Tutorial) | Ryan King Art | https://www.youtube.com/watch?v=BL6fyBeldHA |
| How to Grow Tendrils Over Any Object (Blender Tutorial) | Pixel Me That | https://www.youtube.com/watch?v=ufRygCrYsx4 |
| A Different approach to making FIRE in Blender! | Kenan Proffitt | https://www.youtube.com/watch?v=cUfc4iWG9qI |
| Blender 4.0 RIGIFY ＃6-1: Custom Rigs (theory) | CGDive (Blender Rigging Tuts) | https://youtu.be/Cq2Vw6EFXy0?list=PLdcL5aF8ZcJuG3kKcVgQQz36E3JXzijEH |
| Color difference | Wikipedia | https://en.wikipedia.org/wiki/Color_difference#CIEDE2000 |
| How to Make Animated PIXEL ART Characters Sprites with Blender 2.9 \| Quick and Easy TUTORIAL | Soyaa | https://www.youtube.com/watch?v=eSqb6II3WMM |
| Blender Skull - Part 1,2,3 - Main Head Shape, Top Teeth, Jaw \| Basic Modeling Course (No Sculpt!) | Blender Frenzy | https://www.youtube.com/watch?v=Yjvq7QTJtPs&list=PLH3QvbpQe8WRjEbi5CbqTwcauq_HBRI0T&index=1 |
| Blender 2.9 \| How to make a Halloween Ghost Cloth Simulation + Easy Procedural Textures \| TUTORIAL | Aria Faith Jones | https://www.youtube.com/watch?v=VsK_8JeWRyw |
| Damped Track Constraint \| Blender Rigging Tutorial | --- | https://www.youtube.com/watch?v=7glB4GTVTnM |
| Make The Dune Sandworm \| Blender Tutorial - Part 1 | PIXXO 3D | https://www.youtube.com/watch?v=0UC7XGMPC6g |
| Make The Dune Sandworm \| Blender Tutorial - Part 2 | PIXXO 3D | https://www.youtube.com/watch?v=ZRPWcBfPYGs |
| Make The Dune Sandworm \| Blender Tutorial - Part 3 | PIXXO 3D | https://www.youtube.com/watch?v=BxsLvWfamS8 |
| Mongolian death worm | Wikipedia | https://en.wikipedia.org/wiki/Mongolian_death_worm |
| How to Make a Three Point Lighting Setup in Blender  | Ryan King Art | https://www.youtube.com/watch?v=sN8hS2vLG4o |
| Blender 3D: Noob to Pro/Modeling a volcano  | WIKIBOOKS | https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Modeling_a_volcano |