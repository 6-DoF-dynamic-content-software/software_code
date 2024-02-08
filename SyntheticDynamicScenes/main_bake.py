import os
import json
import sys
import time
import argparse
from pathlib import Path
 
argv = sys.argv[sys.argv.index('--') + 1:]
parser = argparse.ArgumentParser()
parser.add_argument('-jp', '--json_path', dest='json_path')
parser.add_argument('-bp', '--blend_path', dest='blend_path')
args = parser.parse_known_args(argv)[0]

# ---------------------------------------------------------------------------- #
#                              Setting parameters                              #
# ---------------------------------------------------------------------------- #
jsonFilePath = f"{args.json_path}"
with open(jsonFilePath) as f:
    data = json.load(f)
blendFilePath = Path(f"{args.blend_path}")

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

def main_pipeline(frameNum, objIdx):
    # os.system(f"/Applications/Blender.app/Contents/MacOS/Blender -b ./data/lego.blend -P blenderBake.py -- -jp {jsonFilePath} -f {frameNum} -objIdx {idx}")
    os.system(f'"C:/Program Files/Blender Foundation/Blender 4.0/blender.exe" -b {blendFilePath} -P bake.py -- -jp {jsonFilePath} -frameIdx {frameNum} -objIdx {objIdx}')
    # os.system(f'"C:/Program Files/Blender Foundation/Blender 4.0/blender.exe" -b ./data/Worker/Worker.blend -P newBake.py -- -jp {jsonFilePath} -frameIdx {frameNum} -objIdx {objIdx}')
    # os.system(f'"C:/Program Files/Blender Foundation/Blender 4.0/blender.exe" -b ./data/Amily/Amily.blend -P newBake.py -- -jp {jsonFilePath} -frameIdx {frameNum} -objIdx {objIdx}')

# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    startTime = time.time()
    for frameNum in captureFrames:
        for objIdx in range(len(objectNames)):
            # objectName = objectNames[objIdx]
            # materialNames = materialNamesList[objIdx]
            # saveImagePath = saveImageDir/f"{objectName}_{frameNum}.jpg"
            # objSavePath = saveObjDir/f'{objectName}_{frameNum}.obj'
            main_pipeline(frameNum, objIdx)  
    endTime = time.time()
    print(endTime-startTime)  
            