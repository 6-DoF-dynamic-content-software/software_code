import bpy
import json
import sys
import argparse
from pathlib import Path
 
argv = sys.argv[sys.argv.index('--') + 1:]
parser = argparse.ArgumentParser()
parser.add_argument('-jp', '--json_path', dest='json_path')
parser.add_argument('-frameIdx', '--frame_index', dest='frame_index')
parser.add_argument('-objIdx', '--object_index', dest='object_index')
args = parser.parse_known_args(argv)[0]

# ---------------------------------------------------------------------------- #
#                              Setting parameters                              #
# ---------------------------------------------------------------------------- #
frame = int(args.frame_index)
object_index = int(args.object_index)

jsonFilePath = Path(f"{args.json_path}")
with open(jsonFilePath) as f:
    data = json.load(f)

startFrame = data["startFrame"]
endFrame = data["endFrame"]
step = data["step"]
captureFrames = [i for i in range(startFrame,endFrame,step)]

sceneName = data["sceneName"]
objectNames = data["objectNames"]
materialNamesList = data["materialNamesList"]
upsample_counts = data["upsample_counts"]
render_samples_step = data["render_samples_step"]

projDir = Path(".")/data["projDirName"]
saveImageDir = projDir/data["saveTexDir"]
saveImageDir.mkdir(parents=True, exist_ok=True)
saveObjDir = projDir/data["saveObjDir"]
saveObjDir.mkdir(parents=True, exist_ok=True)

# setting new image
imageWidth = 4096
imageHeight = 4096
imageAlpha = False

def main_pipeline(frameNum, sceneName, 
                  objectName,
                  materialNames,
                  imageSavePath,
                  objSavePath):
    
    # ---------------------------------------------------------------------------- #
    #                                  preprocess                                  #
    # ---------------------------------------------------------------------------- #
    # setting scene
    scene = bpy.data.scenes[sceneName]
    
    # setting render type
    scene.render.engine="CYCLES" 
    scene.cycles.device="GPU"   
    scene.cycles.samples = render_samples_step
    
    # change frame
    scene.frame_set(frameNum)
    
    texImageNodes = []
    
    # ---------------------------------------------------------------------------- #
    #                               select the object                              #
    # ---------------------------------------------------------------------------- #
    print(f"objectName: {objectName}")
    bpy.ops.object.select_all(action='DESELECT')
    obj = scene.objects[objectName]
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # ---------------------------------------------------------------------------- #
    #                                 Upsample mesh                                #
    # ---------------------------------------------------------------------------- #
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    upsample_count = upsample_counts[0]
    for i in range(upsample_count):
        print(f"Upsample {i}")
        bpy.ops.mesh.subdivide()
    bpy.ops.object.mode_set(mode='OBJECT')    
    
    # ---------------------------------------------------------------------------- #
    #          create a new image (might have default unwraping(mapping))          #
    # ---------------------------------------------------------------------------- #
    bpy.ops.image.new(name='bake',width=imageWidth,height=imageHeight,alpha=imageAlpha)
    image = bpy.data.images['bake']
    
    # ---------------------------------------------------------------------------- #
    #                           setup multiple materials                           #
    # ---------------------------------------------------------------------------- #
    for materialName in materialNames:
        print(f"materialName: {materialName}")
        mat = bpy.data.materials[materialName]
        mat.use_nodes = True
        
        # Create Texture Image Node in material for Light Condition
        texImageNode = mat.node_tree.nodes.new("ShaderNodeTexImage") 
        texImageNode.name = "texImageName" 
        texImageNode.image = image
        texImageNode.select = True 
        mat.node_tree.nodes.active = texImageNode
        texImageNodes.append(texImageNode)
    
    # ---------------------------------------------------------------------------- #
    #                  Create a new smart uv layer for bake image                  #
    # ---------------------------------------------------------------------------- #
    obj.data.uv_layers.new(name="UVMapBake")
    obj.data.uv_layers["UVMapBake"].active = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.uv.smart_project(island_margin=0.001)
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.select_set(True)
    
    # ---------------------------------------------------------------------------- #
    #                           Bake With Light Condition                          #
    # ---------------------------------------------------------------------------- #
    # bake settings (w/ light conditions)
    scene.cycles.bake_type = "COMBINED"
    scene.render.bake.use_pass_direct = True
    scene.render.bake.use_pass_indirect = True
    scene.render.bake.use_pass_color = True
    
    # ---------------------------------------------------------------------------- #
    #                                Bake UV texture                               #
    # ---------------------------------------------------------------------------- #
    bpy.ops.object.bake(type="COMBINED",target="IMAGE_TEXTURES",save_mode="INTERNAL")
    
    # ---------------------------------------------------------------------------- #
    #                               Save baked image                               #
    # ---------------------------------------------------------------------------- #
    image.filepath_raw = str(imageSavePath.absolute())
    image.file_format = 'JPEG'
    image.save()
    
    # ---------------------------------------------------------------------------- #
    #                                 Save Obj File                                #
    # ---------------------------------------------------------------------------- #
    # bpy.ops.export_scene.obj(filepath=str(objSavePath),
    #                          use_selection=True, use_normals=False, use_uvs=True, use_materials=True, keep_vertex_order=True,
    #                          path_mode="ABSOLUTE")
    # For blender v4.0
    bpy.ops.wm.obj_export(filepath=str(objSavePath),
                        export_selected_objects=True, export_uv=True, export_normals=False, export_colors=False, export_materials=True,
                        path_mode="ABSOLUTE")
    
    # ---------------------------------------------------------------------------- #
    #                           Clean the image and nodes                          #
    # ---------------------------------------------------------------------------- #
    obj.data.uv_layers.remove(obj.data.uv_layers["UVMapBake"])
    for idx in range(len(materialNames)):
        materialName = materialNames[idx]
        texImageNode = texImageNodes[idx]
        mat = bpy.data.materials[materialName]
        mat.node_tree.nodes.remove(texImageNode)
    bpy.data.images.remove(image)

if __name__ == "__main__":
    frameNum = frame
    idx = object_index
    
    objectName = objectNames[idx]
    saveObjectName = str(objectName).replace("*", "_")
    saveObjectName = saveObjectName.replace("/", "_")
    materialNames = materialNamesList[idx]
    saveImagePath = saveImageDir/f"{saveObjectName}_{frameNum}.jpg"
    objSavePath = saveObjDir/f'{saveObjectName}_{frameNum}.obj'
    
    main_pipeline(frameNum, sceneName, 
                objectName,
                materialNames,
                saveImagePath,
                objSavePath)    
            
    # bpy.ops.wm.save_mainfile(check_existing=False)
    