import bpy
import json
import sys
import warnings
from pathlib import Path
sys.path.insert(1, './lib')
import generateJson

    
if __name__ == "__main__":
    
    scene = bpy.data.scenes["Scene"]
    
    collectionNameList = ["Collection"]
    
    objectNames = [
        "Shirt",
        "Body",
        "Helmet",
        "Eyelashes",
        "Pants",
        "Vest",
        "Hair",
        "Boots"
    ]
    materialNamesList = []
    
    for objName in objectNames:
        obj = scene.objects[objName]
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        tmp = []
        for material in obj.material_slots:
            tmp.append(material.name)
        materialNamesList.append(tmp)

    generateJson.generateJson(projName="Worker",
                            objectNames=objectNames,
                            materialNamesList=materialNamesList,
                            upsample_counts=[3 for i in range(len(objectNames))],
                            preprocessBlendDir=Path(".")/"data"/"Worker",
                            projDirName=Path(".")/"results"/"Worker",
                            )
    
    
 
    
    