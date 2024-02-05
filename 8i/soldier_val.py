import bpy
import math
import argparse, sys, os
import json
import mathutils
import numpy as np
from math import radians


def initialization(mesh_path):
    bpy.ops.wm.ply_import(filepath = mesh_path)  # import PLY
    model = bpy.context.active_object
    scale = 2.3 / model.dimensions[1]
    model.scale = (scale, scale, scale)  # scale
    model.rotation_euler = (math.pi / 2, 0, 0)  # rotation
    model.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')  # Change origin
    model.location = (0, 0, 0)  # move to the center

    # assign material
    mat = bpy.data.materials.new(name="test")
    model.data.materials.append(mat)
    mat.use_nodes = True
    mat.node_tree.nodes.new(type="ShaderNodeAttribute")
    mat.node_tree.nodes["Attribute"].attribute_name = "Col"
    diffuse = mat.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
    input = diffuse.inputs["Color"]
    output = mat.node_tree.nodes["Attribute"].outputs["Color"]
    mat.node_tree.links.new(input, output)

    right = mat.node_tree.nodes['Material Output'].inputs['Surface']
    left = diffuse.outputs[0]
    mat.node_tree.links.new(left, right)


    bpy.ops.node.new_geometry_nodes_modifier()
    node_group = bpy.context.object.modifiers[0].node_group
    nodes = node_group.nodes

    cube = nodes.new(type="GeometryNodeMeshCube")
    nodes['Cube'].inputs[0].default_value = (2.0, 2.0, 2.0)
    set_material = nodes.new(type="GeometryNodeSetMaterial")
    set_material.inputs[2].default_value = mat
    IoP = nodes.new(type="GeometryNodeInstanceOnPoints")
    RI = nodes.new(type="GeometryNodeRealizeInstances")
    link_left = nodes["Group Input"].outputs["Geometry"]
    link_right = IoP.inputs["Points"]
    links = node_group.links
    links.new(link_left, link_right)

    link_left = IoP.outputs[0]
    link_right = RI.inputs[0]
    links.new(link_left, link_right)

    link_left = RI.outputs[0]
    link_right = nodes["Group Output"].inputs[0]
    links.new(link_left, link_right)

    link_left = cube.outputs["Mesh"]
    link_right = set_material.inputs["Geometry"]
    links.new(link_left, link_right)

    link_left = set_material.outputs[0]
    link_right = IoP.inputs["Instance"]
    links.new(link_left, link_right)


def parent_obj_to_camera(b_camera):
    origin = (0, 0, 0)
    b_empty = bpy.data.objects.new("Empty", None)
    b_empty.location = origin
    b_camera.parent = b_empty  # setup parenting

    scn = bpy.context.scene
    scn.collection.objects.link(b_empty)
    bpy.context.view_layer.objects.active = b_empty
    # scn.objects.active = b_empty
    return b_empty


def listify_matrix(matrix):
    matrix_list = []
    for row in matrix:
        matrix_list.append(list(row))
    return matrix_list


def get_name(file):
    name = ''
    for c in file:
        if c == '.':
            return name
        else:
            name = name + c

def get_folder(folder_name):
    name = ''
    for c in folder_name:
        if c == '_':
            return name
        else:
            name = name + c

DEBUG = False

VIEWS = 20 #num views to generates
RESOLUTION = 800
DEPTH_SCALE = 1.4
COLOR_DEPTH = 8
FORMAT = 'PNG'
RANDOM_VIEWS = True
UPPER_VIEWS = True
delete = True



ply_path = "/home/jackzhu/Downloads/dataset_test/soldier/"
files = os.listdir(ply_path)
files.sort()
for file in files[:]:
    file_path = ply_path + file
    name = get_name(file) + '_val/'
    fp = "/home/jackzhu/Downloads/soldier/" + name

    if not os.path.exists(fp):
        os.makedirs(fp)
        initialization(file_path)
        out_data = {
            'camera_angle_x': bpy.data.objects['Camera'].data.angle_x,
        }

        # Render Optimizations
        bpy.context.scene.render.use_persistent_data = True

        # Set up rendering of depth map.
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        links = tree.links

        bpy.context.scene.view_layers["RenderLayer"].use_pass_diffuse_color = True
        bpy.context.scene.view_layers["RenderLayer"].use_pass_diffuse_direct = False
        bpy.context.scene.view_layers["RenderLayer"].use_pass_diffuse_indirect = False
        bpy.context.scene.render.image_settings.file_format = str(FORMAT)
        bpy.context.scene.render.image_settings.color_depth = str(COLOR_DEPTH)

        if not DEBUG:
            # Create input render layer node.
            render_layers = tree.nodes.new('CompositorNodeRLayers')
            tree.nodes.new('CompositorNodeComposite')
            left = tree.nodes['Render Layers'].outputs['DiffCol']

            tree.nodes.new('CompositorNodeSetAlpha')
            tree.nodes['Set Alpha'].mode = 'APPLY'

            right = tree.nodes['Set Alpha'].inputs['Image']
            tree.links.new(left, right)

            left = tree.nodes['Render Layers'].outputs['Alpha']
            right = tree.nodes['Set Alpha'].inputs['Alpha']
            tree.links.new(left, right)

            left = tree.nodes['Set Alpha'].outputs['Image']
            right = tree.nodes['Composite'].inputs['Image']
            tree.links.new(left, right)

            depth_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
            depth_file_output.label = 'Depth Output'
            if FORMAT == 'OPEN_EXR':
                links.new(render_layers.outputs['Depth'], depth_file_output.inputs[0])
            else:
                # Remap as other types can not represent the full range of depth.
                map = tree.nodes.new(type="CompositorNodeMapValue")
                # Size is chosen kind of arbitrarily, try out until you're satisfied with resulting depth map.
                map.offset = [-0.7]
                map.size = [DEPTH_SCALE]
                map.use_min = True
                map.min = [0]
                links.new(render_layers.outputs['Depth'], map.inputs[0])

                links.new(map.outputs[0], depth_file_output.inputs[0])


        # Background
        bpy.context.scene.render.dither_intensity = 0.0
        bpy.context.scene.render.film_transparent = True

        # Create collection for objects not to render with background

        scene = bpy.context.scene
        scene.render.resolution_x = RESOLUTION
        scene.render.resolution_y = RESOLUTION
        scene.render.resolution_percentage = 100

        cam = scene.objects['Camera']

        cam.location = (0, 4.0, 0.5)
        cam_constraint = cam.constraints.new(type='TRACK_TO')
        cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        cam_constraint.up_axis = 'UP_Y'
        b_empty = parent_obj_to_camera(cam)
        cam_constraint.target = b_empty

        scene.render.image_settings.file_format = 'PNG'  # set output format to .png

        stepsize = 360.0 / VIEWS
        rotation_mode = 'XYZ'

        out_data['frames'] = []
        np.random.seed(3)
        for i in range(0, VIEWS):
            if RANDOM_VIEWS:
                scene.render.filepath = fp + '/r_' + str(i)
                if UPPER_VIEWS:
                    rot = np.random.uniform(0, 1, size=3) * (1, 0, 2 * np.pi)
                    rot[0] = np.abs(np.arccos(1 - 2 * rot[0]) - np.pi / 2)
                    b_empty.rotation_euler = rot
                else:
                    b_empty.rotation_euler = np.random.uniform(0, 2 * np.pi, size=3)
            else:
                print("Rotation {}, {}".format((stepsize * i), radians(stepsize * i)))
                scene.render.filepath = fp + '/r_{0:03d}'.format(int(i * stepsize))


            if DEBUG:
                break
            else:
                bpy.ops.render.render(write_still=True)  # render still
            frame_data = {
                'file_path': scene.render.filepath,
                'rotation': radians(stepsize),
                'transform_matrix': listify_matrix(cam.matrix_world)
            }
            out_data['frames'].append(frame_data)

            if RANDOM_VIEWS:
                if UPPER_VIEWS:
                    rot = np.random.uniform(0, 1, size=3) * (1, 0, 2 * np.pi)
                    rot[0] = np.abs(np.arccos(1 - 2 * rot[0]) - np.pi / 2)
                    b_empty.rotation_euler = rot
                else:
                    b_empty.rotation_euler = np.random.uniform(0, 2 * np.pi, size=3)
            else:
                b_empty.rotation_euler[2] += radians(stepsize)

        if not DEBUG:
            with open(fp + '/' + 'transforms.json', 'w') as out_file:
                json.dump(out_data, out_file, indent=4)

        if delete:
            bpy.data.objects.remove(bpy.data.objects[get_name(file)], do_unlink=True)
