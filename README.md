# A Software Toolkit and Dataset for Dynamic 6-DoF Content.
## Dependencies
Blender > 3.5 <br />
Numpy <br />
Mathutils
### This code is for Blender version > 4.0
### For Blender version < 3.9
To import PLY into Blender correctly, follow the instructions from [import ply as verts](https://github.com/TombstoneTumbleweedArt/import-ply-as-verts).
If you install Blender through Snap in Ubuntu, try [Overlay](https://snapcraft.io/overlay) to get permission to modify the source files of Blender. Then **modify** 
```bash
bpy.ops.wm.ply_import(filepath = mesh_path)
```  
to
```bash
bpy.ops.import_mesh.ply(filepath=mesh_path, use_verts=True)
```
in ```initialization() ```function.

**Set**
``` bash
bpy.context.scene.view_settings.view_transform = 'Raw'
```
## Running a Script in Linux Terminal
To execute a script in the Linux terminal, use the following command format:

```bash
blender -b /path/to/.blend_file -P /path/to/script.py
```

Example command:
```bash
blender -b lego.blend -P lego_train.py
```
To generate datasets for point clouds, use ```train.blend```. 

## Original dataset
[8iVFB](http://plenodb.jpeg.org/pc/8ilabs/)  
[vsenseVVDB2](https://v-sense.scss.tcd.ie/research/vsensevvdb2-v-sense-volumetric-video-quality-database-2/)  
[Lego](https://drive.google.com/drive/folders/128yBriW1IG_3NJ5Rp7APSTZsJqdJdfc1)  
[Pig](https://blendermarket.com/products/piggy-animations-vfx-grace)  
[Amy](https://studio.blender.org/characters/5f1ed640e9115ed35ea4b3fb/showcase/1/)  







