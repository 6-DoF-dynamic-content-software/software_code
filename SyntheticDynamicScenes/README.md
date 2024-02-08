# Blender to Point Cloud

All tests are done in Windows 10 and Blender version 4.0.
Hopefully, they can work well in Ubuntu and MacOS.

## Environment

```bash
conda env create -f environment.yml
conda activate blender_env
```

## Usage

### Setting the experiment environment

1. Create a `data` directory
```bash
mkdir data
```

2. Save all blender file in `data` directory.  
```
.
└── data/
    ├── JU0L522A4_Piglet_Blender/
    │   └── JU0L522A4_Piglet_LookAround_2.83.5.blend
    └── JU0L522A4_Piglet_textures/
        ├── JU0L522A4_Piglet_Body_Hair_BaseColor.png
        ├── JU0L522A4_Piglet_Body_Skin_BaseColor.png
        └── ...
```

- **NOTE:** `path/to/Blender` is usually set as `"C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"` in Windows, and `/Applications/Blender.app/Contents/MacOS/Blender` in MacOS.
- **NOTE:** Use `"C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"` in Windows CMD instead of `C:/"Program Files"/"Blender Foundation"/"Blender 4.0"/blender.exe`.

### For Pig scene

**With ours light settings**

1. Make sure there is the json file.

2. Execute prerun code `preprocess_Pig.py` 
```bash
path/to/Blender -b ./data/Pig/Pig.blend -P ./preprocess_Pig.py
```

3. Execute baking code `main_bake.py` 
```bash
path/to/Blender -b ./data/Pig/Pig.blend -P ./main_bake.py -- --json_path ./json/Pig.json
```

4. Execute merging code `main_mergePcd.py` 
```bash
python ./main_mergePcd.py --json_path ./json/Pig.json
```

**Without light settings**

1. Make sure there is the json file.

2. Execute prerun code `preprocess_Pig.py` 
```bash
path/to/Blender -b ./data/Pig/Pig.blend -P ./preprocess_Pig.py
```

3. Execute baking code `bake_color.py` 
```bash
path/to/Blender -b ./data/Pig/Pig.blend -P ./bake_color.py -- --json_path ./json/Pig.json
```

4. Execute merging code `mergePcd_color.py` 
```bash
python ./mergePcd_color.py --json_path ./json/Pig.json
```

### For Lego scene

1. (Skip) Make sure there is the json file.
If not, then execute `generateJson_Lego.py`.
```bash
path/to/Blender -b ./data/Lego_download/Lego.blend -P ./generateJson_Lego.py
```

2. (Skip) Execute prerun code `preprocess_Lego.py`
```bash
path/to/Blender -b ./data/Lego_download/Lego.blend -P ./preprocess_Lego.py
```

3. Execute baking code `main_bake.py` 
```bash
python ./main_bake.py -- -jp ./json/Lego.json -bp ./data/Lego/Lego.blend
```

4. Execute check code `main_checkBake.py` to check if all the necessary exist
```bash
python ./main_checkBake.py -jp ./json/Lego.json
```

5. Execute merging code `main_mergePcd.py` 
```bash
python ./main_mergePcd.py -jp ./json/Lego.json
```

### For Worker scene

1. Make sure there is the json file.
If not, then execute `generateJson_Worker.py`.
```bash
"C:/Program Files/Blender Foundation/Blender 4.0/blender.exe" -b ./data/Worker_raw/Worker.blend -P ./generateJson_Worker.py
```

2. Execute prerun code `preprocess_Worker.py` 
```bash
"C:/Program Files/Blender Foundation/Blender 4.0/blender.exe" -b ./data/Worker_raw/Worker.blend -P ./preprocess_Worker.py
```

3. Execute baking code `main_bake.py` 
```bash
python ./main_bake.py -- -jp ./json/Worker.json -bp ./data/Worker/Worker.blend
```

4. Execute merging code `main_mergePcd.py` 
```bash
python ./main_mergePcd.py -jp ./json/Worker.json
```

### For Amily scene

1. Make sure there is the json file.
If not, then execute `generateJson_Amily.py`.
```bash
"C:/Program Files/Blender Foundation/Blender 4.0/blender.exe" -b ./data/Amily/Amily.blend -P ./generateJson_Amily.py
```

2. Execute prerun code `preprocess_Amily.py` 
```bash
C:/"Program Files"/"Blender Foundation"/"Blender 4.0"/blender.exe -b ./data/restaurant_anim_test/rain_restaurant_ami.blend -P ./preprocess_Amily.py
```

3. Execute baking code `main_bake.py` 
```bash
python ./main_bake.py -- -jp ./json/Amily.json -bp ./data/Amily/Amily.blend
```

4. Execute merging code `main_mergePcd.py` 
```bash
python ./main_mergePcd.py -jp ./json/Amily.json
```

## Other tools

### Pcd Voxelization `voxelPcd.py`

```bash
python ./main_voxelPcd.py -- -i path/to/intputPcd.ply -o path/to/outputPcd.ply -v 0.01
```
