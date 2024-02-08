import sys
import time
import json
sys.path.insert(1, './lib')
import generateJson
# import objParser
# import plyMerge

import argparse
from pathlib import Path

if __name__ == "__main__":
    startTime = time.time()
    # argparser start
    parser = argparse.ArgumentParser()
    parser.add_argument('-jp', '--json_path', dest='json_path',
                        help="Json file")
    args = parser.parse_args()

    with open(args.json_path) as f:
        data = json.load(f)

    startFrame = data["startFrame"]
    endFrame = data["endFrame"]
    step = data["step"]
    captureFrames = [i for i in range(startFrame,endFrame,step)]

    sceneName = data["sceneName"]
    objectNames = data["objectNames"]
    materialNamesList = data["materialNamesList"]
    upsample_counts = data["upsample_counts"]

    projDir = Path(".")/data["projDirName"]
    inputTexDir = projDir/data["saveTexDir"]
    inputObjDir = projDir/data["saveObjDir"]
    projName = data["projName"]
    
    objectNames_additional = []
    materialNamesList_additional = []
    upsample_counts_additional = []
    for frameNum in captureFrames:
        for objectNum in range(len(objectNames)):
            objectName = objectNames[objectNum]
            # [YC] add
            objectName_raw = objectName
            objectName = str(objectName).replace("*", "_")
            objectName = objectName.replace("/", "_")
    
            objFilePath = inputObjDir/f'{objectName}_{frameNum}.obj'
            materialFilePath = inputTexDir/f'{objectName}_{frameNum}.jpg'
            
            if objFilePath.exists() and materialFilePath.exists():
                pass
            else:
                print(f"{objectNames[objectNum]} {materialNamesList[objectNum]} {frameNum} miss")
                if objectNames[objectNum] not in objectNames_additional:
                    objectNames_additional.append(objectNames[objectNum])
                    materialNamesList_additional.append(materialNamesList[objectNum])
                    upsample_counts_additional.append(upsample_counts[objectNum])

    if objectNames_additional:
        generateJson.generateJson(projName=data["projName"]+"_additional",
                                startFrame=data["startFrame"], 
                                endFrame=data["endFrame"], 
                                step=data["step"],
                                objectNames=objectNames_additional,
                                materialNamesList=materialNamesList_additional,
                                upsample_counts=upsample_counts_additional,
                                render_samples_step=data["render_samples_step"],
                                preprocessBlendDir=data["preprocessBlendDir"],
                                projDirName=data["projDirName"],
                                saveTexDir=data["saveTexDir"],
                                saveObjDir=data["saveObjDir"],
                                savePlyDir=data["savePlyDir"],
                                finalResultsDir=data["finalResultsDir"],
                                voxel_size=data["voxel_size"]
                                )
        print("=============================")
        print("There are something missing.")
        print("You should run the command below:")
        oldProjName = data['projName']
        print(f"$ python ./main_bake.py -- -jp ./json/{oldProjName+'_additional'}.json -bp path/to/{oldProjName}.blend")
        print("=============================")
    else:
        print("Everything looks good.")