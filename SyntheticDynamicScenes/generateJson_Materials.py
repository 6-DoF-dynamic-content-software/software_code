import bpy
import json
import sys
import warnings
from pathlib import Path
sys.path.insert(1, './lib')
import generateJson

    
if __name__ == "__main__":
    
    scene = bpy.data.scenes["Scene"]
    
    collectionNameList = ["Collection 1"]
    
    objectNames = []
    materialNamesList = []

    for collectionName in collectionNameList:
        collection = bpy.data.collections[collectionName]
        for obj in collection.objects:
            objectNames.append(obj.name)
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            tmp = []
            for material in obj.material_slots:
                tmp.append(material.name)
            materialNamesList.append(tmp)
    
    generateJson.generateJson(projName="Materials",
                            objectNames=objectNames,
                            materialNamesList=materialNamesList,
                            upsample_counts=[3 for i in range(len(objectNames))],
                            preprocessBlendDir=Path(".")/"data"/"Materials",
                            projDirName=Path(".")/"results"/"Materials",
                            )
    
    
 
    
    