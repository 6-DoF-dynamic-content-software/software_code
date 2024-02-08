import os
import json
import re
import time
import imageio.v2 as imageio
import numpy as np
import pandas as pd
from pathlib import Path
from plyfile import PlyData, PlyElement

def newWritePly(saveFilePath, datas, text=True):
    """
    save_path : path to save: '/yy/XX.ply'
    pt: point_cloud: size (N,6) == (x,y,z,red,green,blue)
    """
    points = [(data[0],data[1],data[2],int(data[5]),int(data[6]),int(data[7])) for data in datas]
    vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4'), ('red', 'ubyte'), ('green', 'ubyte'), ('blue', 'ubyte')])
    el = PlyElement.describe(vertex, 'vertex', comments=['vertices'])
    PlyData([el], text=text).write(saveFilePath)
    print(f'Done objParser.py {saveFilePath}')

def AddPlyHeader(saveFilePath, numOfVertex):
    header = 'ply\n'
    header = header + f'format ascii 1.0\n' \
                    + f'element vertex {numOfVertex}\n' \
                    + f'property float x\n' \
                    + f'property float y\n' \
                    + f'property float z\n' \
                    + f'property uchar red\n' \
                    + f'property uchar green\n' \
                    + f'property uchar blue\n' \
                    + f'element face 0\n' \
                    + f'property list uint8 int32 vertex_index\n' \
                    + f'end_header\n'
    with open(str(saveFilePath),"w") as f:
        f.write(header)
    
def AddPlyBody(saveFilePath,datas):
    body = ''
    for num in range(len(datas)):
        body = body + f"{datas[num][0]} {datas[num][1]} {datas[num][2]} {int(datas[num][5])} {int(datas[num][6])} {int(datas[num][7])}\n"
    with open(str(saveFilePath),"a") as f:
        f.write(body)
    print(f'Done objParser.py {saveFilePath}')

def handleObjFile(objFilePath:Path,materialFilePath:Path=None) -> np.array:
    vList = []
    vtList = []
    fList = []
    with open(objFilePath,'r') as f:
        for line in f.readlines():
            if line[0] == 'v':
                if line[1] == ' ':
                    splitLine = line.split()[1:]
                    vList.append(splitLine)
                elif line[1] == 't':
                    splitLine = line.split()[1:]
                    vtList.append(splitLine)
            elif line[0] == 'f' and line[1] == ' ':
                splitLine = line.split()[1:]
                splitLine = [i.split('/')[:2] for i in splitLine]
                fList.extend(splitLine)
                
    # print(f'len(vList): {len(vList)}')
    # print(f'len(vtList): {len(vtList)}')
    # print(f'len(fList): {len(fList)}')

    numOfVertex = len(vList)

    results = np.zeros((numOfVertex, 8))
    for fData in fList:
        vIdx = int(fData[0])-1
        vtIdx = int(fData[1])-1
        mList = vList[vIdx]+vtList[vtIdx]
        for i in range(5):
            results[vIdx][i] = float(mList[i])   
    # print(f'len(results): {len(results)}')
    
    if materialFilePath == None:
        return results

    im = imageio.imread(materialFilePath)
    row,col,channel = im.shape
    for num in range(len(results)):
        u_pixel = min(max(round(results[num][3]*col), 0), 4096-1)
        v_pixel = min(max(round(abs(results[num][4]-1)*row), 0), 4096-1)
        rgb = im[v_pixel,u_pixel]
        results[num][5] = rgb[0]
        results[num][6] = rgb[1]
        results[num][7] = rgb[2]
    return results

def saveToPly(plySavePath:Path, results:np.array):
    newWritePly(plySavePath, results, False)
    # AddPlyHeader(plySavePath,len(results))
    # AddPlyBody(plySavePath,results)

def main(jsonFilePath):
    # ---------------------------------------------------------------------------- #
    #                              Setting parameters                              #
    # ---------------------------------------------------------------------------- #
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

    projDir = Path(".")/data["projDirName"]
    inputTexDir = projDir/data["saveTexDir"]
    inputObjDir = projDir/data["saveObjDir"]
    savePlyDir = projDir/data["savePlyDir"]
    savePlyDir.mkdir(parents=True,exist_ok=True)
    
    # +++++++++++++++++++++++++++++++++ #
    
    for frameNum in captureFrames:
        for objectNum in range(len(objectNames)):
            objectName = objectNames[objectNum]
            
            # [YC] add
            objectName = str(objectName).replace("*", "_")
            objectName = objectName.replace("/", "_")

            objFilePath = inputObjDir/f'{objectName}_{frameNum}.obj'
            materialFilePath = inputTexDir/f'{objectName}_{frameNum}.jpg'
            csvSavePath = savePlyDir/f'{objectName}_{frameNum}.csv'
            plySavePath = savePlyDir/f'{objectName}_{frameNum}.ply'

            results = handleObjFile(objFilePath,materialFilePath)
            saveToPly(plySavePath,results)
            df = pd.DataFrame(results, columns = ['x','y','z','u','v','r','g','b'])
            df.to_csv(csvSavePath)

def main_color(jsonFilePath):
    # ---------------------------------------------------------------------------- #
    #                              Setting parameters                              #
    # ---------------------------------------------------------------------------- #
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

    projDir = Path(".")/data["projDirName"]
    inputTexDir = projDir/data["saveTexDir"]
    inputObjDir = projDir/data["saveObjDir"]
    savePlyDir = projDir/data["savePlyDir"]
    savePlyDir.mkdir(parents=True,exist_ok=True)
    
    # +++++++++++++++++++++++++++++++++ #
    
    for frameNum in captureFrames:
        for objectNum in range(len(objectNames)):
            objectName = objectNames[objectNum]

            objFilePath = inputObjDir/f'{objectName}_{frameNum}.obj'
            materialFilePath = inputTexDir/f'{objectName}_color.jpg'
            csvSavePath = savePlyDir/f'{objectName}_{frameNum}.csv'
            plySavePath = savePlyDir/f'{objectName}_{frameNum}.ply'

            results = handleObjFile(objFilePath,materialFilePath)
            saveToPly(plySavePath,results)
            df = pd.DataFrame(results, columns = ['x','y','z','u','v','r','g','b'])
            df.to_csv(csvSavePath)

if __name__ == "__main__":
    jsonFilePath = Path(".")/"Pig.json"
    main(jsonFilePath)
            