import os
import re
import imageio
import time
import argparse
import json
import open3d as o3d
import numpy as np
import pandas as pd
from pathlib import Path
from plyfile import PlyData, PlyElement

def newWritePly(saveFilePath, datas, text=True):
    """
    save_path : path to save: '/yy/XX.ply'
    pt: point_cloud: size (N,6) == (x,y,z,red,green,blue)
    """
    points = [(data[0],data[1],data[2],int(data[3]),int(data[4]),int(data[5])) for data in datas]
    vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4'), ('red', 'ubyte'), ('green', 'ubyte'), ('blue', 'ubyte')])
    el = PlyElement.describe(vertex, 'vertex', comments=['vertices'])
    PlyData([el], text=text).write(saveFilePath)
    print(f'Done objParser.py {saveFilePath}')

def AddPlyHeader(saveFilePath, numOfVertex):
    header = 'ply\n'
    header = header + f'format ascii 1.0\n' \
                    + f'comment made by Yuan-Chun Sun\n' \
                    + f'comment this file is about merging all the element\n' \
                    + f'element vertex {numOfVertex}\n' \
                    + f'property float x\n' \
                    + f'property float y\n' \
                    + f'property float z\n' \
                    + f'property uchar red\n' \
                    + f'property uchar green\n' \
                    + f'property uchar blue\n' \
                    + f'end_header\n'
    with open(str(saveFilePath),"w") as f:
        f.write(header)
    
def AddPlyBody(saveFilePath,datas):
    body = ''
    for data in datas:
        body = body + f"{data[0]} {data[1]} {data[2]} {int(data[3])} {int(data[4])} {int(data[5])} \n"
    with open(str(saveFilePath),"a") as f:
        f.write(body)
    print(f'done {saveFilePath}')

def saveToPly(plySavePath:Path,results:list):
    newWritePly(plySavePath, results, False)
    # AddPlyHeader(plySavePath,len(results))
    # AddPlyBody(plySavePath,results)
    
def voxelization(pcdPath, plyVoxelSavePath, voxel_size=0.01, write_ascii=True):
    pcd = o3d.io.read_point_cloud(str(pcdPath))
    downsampled_pcd = pcd.voxel_down_sample(voxel_size)
    o3d.io.write_point_cloud(str(plyVoxelSavePath), downsampled_pcd, write_ascii=write_ascii, compressed=False, print_progress=False)

def main(jsonFilePath, write_ascii=True):
    # ---------------------------------------------------------------------------- #
    #                              Setting parameters                              #
    # ---------------------------------------------------------------------------- #
    with open(jsonFilePath) as f:
        data = json.load(f)

    projName = data["projName"]
    startFrame = data["startFrame"]
    endFrame = data["endFrame"]
    step = data["step"]
    captureFrames = [i for i in range(startFrame,endFrame,step)]

    sceneName = data["sceneName"]
    objectNames = data["objectNames"]
    materialNamesList = data["materialNamesList"]
    upsample_counts = data["upsample_counts"]

    projDir = Path(".")/data["projDirName"]
    inputPlyDir = projDir/data["savePlyDir"]
    saveFinalResultsDir = projDir/data["finalResultsDir"]
    saveFinalResultsDir.mkdir(parents=True,exist_ok=True)
    
    voxel_size = data["voxel_size"]
    # +++++++++++++++++++++++++++++++++ #
    
    for frameNum in captureFrames:
        datas = []
        for objectNum in range(len(objectNames)):
            objectName = objectNames[objectNum]
            
            objectName = str(objectName).replace("*", "_")
            objectName = objectName.replace("/", "_")
            
            plyFilePath = inputPlyDir/f'{objectName}_{frameNum}.ply'
            # print(plyFilePath)
            ply_data = PlyData.read(plyFilePath)
            data = ply_data.elements[0].data
            data_pd = pd.DataFrame(data)
            data_list = data_pd.values.tolist()
            datas.extend(data_list)
        
        plySavePath = saveFinalResultsDir/f'{projName}_frame{frameNum}.ply'
        saveToPly(plySavePath, datas)
        plyVoxelSavePath = saveFinalResultsDir/f'{projName}_frame{frameNum}_voxel.ply'    
        voxelization(plySavePath, plyVoxelSavePath, voxel_size)
        print(f"Done plyMerge.py {plySavePath}")
        
if __name__ == "__main__":
    jsonFilePath = Path(".")/"Pig.json"
    main(jsonFilePath)