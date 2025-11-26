# IE-AutoSpriter-
Infinity Engine AutoSpriter is a Blender add-on that automates sprite creation from creature animations.

This is a work in progress and an alpha release. This means that most things are not implemented and the add-on is subject to heavy changes. Use this add-on with caution!!

Please use the latest version instead of the latest commit.

This is also a learning project focused on my personal use and interest. Suggestions are welcome!

## Alpha Version:
* May not work or only work under special conditions.
* May not work due to missing information in the manual.
* May contain issues for various reasons.
* I am not a Blender or Blender API expert, so this may also cause issues.
* Only Tested it with blender version 4.0(It may already work on higher versions)
* The focus of the beta phase will be on bug fixing.
* [Here](https://github.com/Incrementis/IE-AutoSpriter-/issues/52) you will find the currently known issues that will be fixed in the beta phase.
### Performance
The 4.0 blend save files contain the appropriate settings.
#### Render engine "Cycles": 
* Rendering a frame took [0.8 to 1 seconds](https://github.com/Incrementis/IE-AutoSpriter-/issues/18#issuecomment-3079607164)
#### Render engine "EEVEE": 
* Rendering a frame took [0.05 seconds](https://github.com/Incrementis/IE-AutoSpriter-/issues/18#issuecomment-3079719096)

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
* Please note that the demos are not intended as a guide or tutorial. They are intended ONLY to demonstrate/test the features of IE Autospriter.

## Operating Systems
* Windows 11
* May also work on other platforms since Python is a platform-independent language

## Languages
* English

## Special Thanks
Thanks to "The Gibberlings 3" forum users and "Artisan's Corner" discord server users who helped me with hints and information:
* The Artisan
* CamDawg

## Sources(Learning Materials)
* [INI file format: Creature Animations](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/ini_anim.htm)
* [Avatar Naming Schemes](https://gibberlings3.github.io/iesdp/appendices/avatarnaming.htm)
* [IE-Animations](https://github.com/ArtemiusI/IE-Animations) by Artemiusl
* [education/175-Blender-Properties](https://github.com/pagekey/education/tree/main/175-Blender-Properties) by PageKey
* [Your Own Operator | Scripting for Artists [8]](https://www.youtube.com/watch?v=xscQ9tcN4GI&list=LL) by Blender
* [Render 8 Direction Animated Sprites in Blender with Python](https://www.youtube.com/watch?v=l1Io7fLYV4o) by FozleCC
* [Blender documentations](https://docs.blender.org) by Blender
* [Blender Rendering Optimization Tips](https://whoisryosuke.com/blog/2024/blender-rendering-optimization-tips) by Ryo
* [Expressions in Blender 3D](https://www.youtube.com/watch?v=5IMFSC5h0a4) by ukramedia
* [https://b3d.interplanety.org/en/creating-radio-buttons-in-the-blender-add-ons-interface/](Creating radio buttons in the Blender add-ons interface) by Nikita