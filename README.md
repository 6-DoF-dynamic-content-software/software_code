# A Software Toolkit and Dataset for Dynamic 6-DoF Content
Mufeng Zhu, Yuan-Chun Sun, Na Li, Jin Zhou, Songqing Chen, Cheng-Hsin Hsu, Yao Liu<br>
| [Webpage](https://6-dof-dynamic-content-software.github.io/) | [Full Paper](#) |

This repository contains the official implementation for [A Software Toolkit and Dataset for Dynamic 6-DoF Content](https://6-dof-dynamic-content-software.github.io/).

Abstract: *Volumetric video streaming has become increasingly popular in recent years due to its flexibility to be explored with 6 degrees-of-freedom (6-DoF). Today, point clouds that capture the geometry and color attribute information are widely used for representing real-world scenes. Due to its large sizes, many research efforts have focused on efficient compression dynamic point clouds, e.g., via video-based point cloud compression (V-PCC). In recent years, neural-based representations, such as neural radiance fields (NeRF), are also receiving much attention in the research community due to its photorealistic novel view synthesis. While neural-based methods have achieved good visual quality of rendered views for static scenes, their application in dynamic scenarios remain challenging. Typically, an efficient design needs to explore the trade-offs between the size of the representation and the compute needed to render neural-based representations. In this paper, we introduce a software toolkit for creating a dataset of volumetric videos in both the point cloud and neural-based representations.With this toolkit, we aim to facilitate research from the multimedia systems community to support practical volumetric streaming. Starting with 3D assets that are freely available online, our software toolkit uses the Blender Python API for generating training and testing datasets that can be used for neural-based dynamic volumetric model training. The created datasets are compliant with existing neural-based model training and rendering frameworks. We also provide software that constructs point cloud sequences derived from synthetic dynamic 3D models. This further facilitates the comparison between point clouds and neural-based methods for volumetric video representation. We release the software toolkit along with the a partial set of generated datasets of sequences, in compliance the permissions granted by the original 3D asset creators.*



## Neural-based approach dataset generation
### Dependencies
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
### Running a Script in Linux Terminal
To execute a script in the Linux terminal, use the following command format:

```bash
blender -b /path/to/.blend_file -P /path/to/script.py
```

Example command:
```bash
blender -b lego.blend -P lego_train.py
```
To generate datasets for point clouds, use ```train.blend```. 

## Point cloud sequence dataset generation (Synthetic Dynamic Scenes)
If you want to generate the dataset by yourself, you can follow the [README](https://github.com/6-DoF-dynamic-content-software/software_code/tree/main/SyntheticDynamicScenes#blender-to-point-cloud) descriptions.
And the codes to generate the dataset are all in `./SyntheticDynamicScenes`.

## Original dataset
You can download the original datasets in the following links:
- [8iVFB](http://plenodb.jpeg.org/pc/8ilabs/)  
- [vsenseVVDB2](https://v-sense.scss.tcd.ie/research/vsensevvdb2-v-sense-volumetric-video-quality-database-2/)
- Synthetic Dynamic Scenes
    - [Lego](https://drive.google.com/drive/folders/128yBriW1IG_3NJ5Rp7APSTZsJqdJdfc1)  
    - [Pig](https://blendermarket.com/products/piggy-animations-vfx-grace)  
    - [Amy](https://studio.blender.org/characters/5f1ed640e9115ed35ea4b3fb/showcase/1/) 

<section class="section" id="citation">
  <div class="container is-max-desktop content">
    <h2 class="title">Citation</h2>
    <pre><code>@Article{XXX,
      author       = {Zhu, Mufeng and Sun, Yuan-Chun and Li,Na and Zhou, Jin and Chen, Songqing and Hsu, Cheng-Hsin and Liu, Yao},
      title        = {A Software Toolkit and Dataset for Dynamic 6-DoF Content},
      journal      = {XXX},
      number       = {XXX},
      volume       = {XXX},
      month        = {XXX},
      year         = {XXX},
      url          = {https://6-dof-dynamic-content-software.github.io/}
}</code></pre>
  </div>
</section>





