import sys
import time
import argparse
import json
import open3d as o3d
import numpy as np
import pandas as pd
from pathlib import Path
from plyfile import PlyData, PlyElement

argv = sys.argv[sys.argv.index('--') + 1:]
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_path', dest='input_path')
parser.add_argument('-o', '--output_path', dest='output_path')
parser.add_argument('-v', '--voxel_size', dest='voxel_size')
args = parser.parse_known_args(argv)[0]

def voxelization(pcdPath, plyVoxelSavePath, voxel_size=0.01):
    pcd = o3d.io.read_point_cloud(str(pcdPath))
    downsampled_pcd = pcd.voxel_down_sample(voxel_size)
    o3d.io.write_point_cloud(str(plyVoxelSavePath), downsampled_pcd, write_ascii=True, compressed=False, print_progress=False)

if __name__ == "__main__":
    startTime = time.time()
    saveDir = Path(f"{args.output_path}")
    saveDir.mkdir(parents=True, exist_ok=True)
    for pcdPath in Path(f"{args.input_path}").glob("*.ply"):
        plyVoxelSavePath = Path(f"{saveDir/pcdPath.name}")
        voxel_size = float(args.voxel_size)
        voxelization(pcdPath, plyVoxelSavePath, voxel_size)
    endTime = time.time()
    print(endTime-startTime) 