import bpy
import json
import sys
import warnings
from pathlib import Path
sys.path.insert(1, './lib')
import generateJson

    
if __name__ == "__main__":
    
    scene = bpy.data.scenes["Scene"]
    
    objectNames = []
    materialNamesList = []
    
    allObjects = [ob for ob in bpy.context.view_layer.objects if ob.visible_get()]
    for ob in allObjects:
        if ob.type == 'MESH':
            objectNames.append(ob.name)
    
    for objName in objectNames:
        obj = scene.objects[objName]
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        tmp = []
        for material in obj.material_slots:
            tmp.append(material.name)
        materialNamesList.append(tmp)

    generateJson.generateJson(projName="Amily",
                            objectNames=objectNames,
                            materialNamesList=materialNamesList,
                            upsample_counts=[3 for i in range(len(objectNames))],
                            preprocessBlendDir=Path(".")/"data"/"Amily",
                            projDirName=Path(".")/"results"/"Amily",
                            )
    
    
 
    
    