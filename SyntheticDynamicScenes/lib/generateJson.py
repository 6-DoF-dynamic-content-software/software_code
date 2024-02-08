# import bpy
import json
import warnings
from pathlib import Path

def generateJson(projName="test",
                startFrame="", endFrame="", step="",
                sceneName="",
                objectNames=[],
                materialNamesList=[],
                upsample_counts=[],
                render_samples_step="",
                preprocessBlendDir="",
                projDirName="",
                saveTexDir="",
                saveObjDir="",
                savePlyDir="",
                finalResultsDir="",
                voxel_size=""
                ):
    with open('./json/template.json', 'r') as openfile:
        # Reading from json file
        jsonDict = json.load(openfile)
        
    jsonDict["projName"] = projName
    if startFrame:
        jsonDict["startFrame"] = startFrame
    if endFrame:
        jsonDict["endFrame"] = endFrame
    if step:
        jsonDict["step"] = step
    # # not yet
    if objectNames:
        jsonDict["objectNames"] = objectNames
    else:
        warnings.filterwarnings("objectNames should not be empty", category=DeprecationWarning)
    
    if materialNamesList:
        jsonDict["materialNamesList"] = materialNamesList
    else:
        warnings.filterwarnings("materialNamesList should not be empty", category=DeprecationWarning)
    
    if upsample_counts:
        jsonDict["upsample_counts"] = upsample_counts
    else:
        jsonDict["upsample_counts"] = [2 for i in range(len(objectNames))]

    if render_samples_step:
         jsonDict["render_samples_step"] = render_samples_step
    if preprocessBlendDir:
         jsonDict["preprocessBlendDir"] = str(preprocessBlendDir).replace("\\", "/")
    if projDirName:
         jsonDict["projDirName"] = str(projDirName).replace("\\", "/")
    if saveTexDir:
         jsonDict["saveTexDir"] = str(saveTexDir).replace("\\", "/")
    if saveObjDir:
         jsonDict["saveObjDir"] = str(saveObjDir).replace("\\", "/")
    if savePlyDir:
         jsonDict["savePlyDir"] = str(savePlyDir).replace("\\", "/")
    if finalResultsDir:
         jsonDict["finalResultsDir"] = str(finalResultsDir)
    if voxel_size:
         jsonDict["voxel_size"] = voxel_size
    
    # Serializing json
    json_object = json.dumps(jsonDict, indent=4)
    # Writing to sample.json
    with open(f"./json/{projName}.json", "w") as outfile:
        outfile.write(json_object)
    
# if __name__ == "__main__":
    
#     # for collection in bpy.data.collections:
#     #     print(collection.name)
    
#     scene = bpy.data.scenes["Scene"]
    
#     # collectionNameList = ["Collection 1", "Collection 2", "Collection 3", "Collection 11"]
#     collectionNameList = ["Collection 1"]
    
#     objectNames = []
#     materialNamesList = []

#     for collectionName in collectionNameList:
#         collection = bpy.data.collections[collectionName]
#         for obj in collection.objects:
#             objectNames.append(obj.name)
#             bpy.context.view_layer.objects.active = obj
#             obj.select_set(True)
#             tmp = []
#             for material in obj.material_slots:
#                 tmp.append(material.name)
#             materialNamesList.append(tmp)
    
#     generateJson(projName="Lego",
#                 objectNames=objectNames,
#                 materialNamesList=materialNamesList,
#                 preprocessBlendDir=Path(".")/"data"/"Lego.blend",
#                 projDirName=Path(".")/"results"/"Lego",
#                 )