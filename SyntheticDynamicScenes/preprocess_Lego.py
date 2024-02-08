import bpy
import json
from pathlib import Path

# do not modify
jsonFilePath = Path(".")/"json"/"Lego.json"
with open(jsonFilePath) as f:
    data = json.load(f)

sceneName = data["sceneName"]
objectNames = data["objectNames"]
materialNamesList = data["materialNamesList"]
upsample_counts = data["upsample_counts"]

saveDir = Path('.')/data["preprocessBlendDir"]
saveDir.mkdir(parents=True,exist_ok=True)

if __name__ == "__main__":
    scene = bpy.data.scenes[sceneName]
    
    # ---------------------------------------------------------------------------- #
    #                                  Tricky part                                 #
    # ---------------------------------------------------------------------------- #
    # bpy.context.window.workspace = bpy.data.workspaces['Scripting']
    # bpy.context.screen.areas[1].spaces[0].show_restrict_column_select = True
    # bpy.data.collections["JU0L522A4_Piglet_LookAround"].hide_select = False
    
    # ---------------------------------------------------------------------------- #
    #                        Add an AREA light to the scene                        #
    # ---------------------------------------------------------------------------- #
    # light_data = bpy.data.lights.new(name="area_light", type="AREA")
    # light_object = bpy.data.objects.new(name="area_light", object_data=light_data)
    # bpy.context.collection.objects.link(light_object)
    # bpy.context.view_layer.objects.active = light_object
    # light_object.select_set(True)
    # light_object.location = (0, 0, 0.5)
    # bpy.ops.transform.resize(value=(5.0, 5.0, 5.0))
    
    # ---------------------------------------------------------------------------- #
    #                                 Upsample mesh                                #
    # ---------------------------------------------------------------------------- #
    for idx in range(len(objectNames)):
        objectName = objectNames[idx]
        obj = scene.objects[objectName]
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    upsample_count = upsample_counts[0]
    for i in range(upsample_count):
        print(f"All objects upsample {i}")
        bpy.ops.mesh.subdivide()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    # ---------------------------------------------------------------------------- #
    #                             Save as blender file                             #
    # ---------------------------------------------------------------------------- #
    bpy.ops.wm.save_as_mainfile(filepath=str(saveDir/"Lego.blend"))
