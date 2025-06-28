import bpy
from bpy import context
import sys
import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_args():
    argv = sys.argv
    if "--" not in argv:
        return []
    else:
        return argv[argv.index("--") + 1:]

def uv_project_from_view():
    area_type = 'VIEW_3D'
    areas = [area for area in bpy.context.window.screen.areas if area.type == area_type]
    
    if not areas:
        logging.error("No VIEW_3D area found")
        return False

    region = next((region for region in areas[0].regions if region.type == 'WINDOW'), None)
    if not region:
        logging.error("No WINDOW region found in VIEW_3D area")
        return False

    with bpy.context.temp_override(
        window=bpy.context.window,
        area=areas[0],
        region=region,
        screen=bpy.context.window.screen
    ):
        try:
            bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=True)
            logging.info("UV unwrapping completed using project_from_view")
            return True
        except Exception as e:
            logging.error(f"UV unwrapping failed: {str(e)}")
            return False

def ensure_top_view():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.region_3d.view_perspective = 'ORTHO'
                    space.region_3d.view_rotation = (1, 0, 0, 0)  # Ensure correct orientation for top view
    return True

def main():
    logging.info("Script started")
    # Get command line arguments
    args = get_args()
    if len(args) < 2:
        logging.error("Usage: blender -b template.blend --python script.py -- -i input.svg [-o output.glb]")
        return

    input_file = None
    output_file = None

    for i, arg in enumerate(args):
        if arg == '-i' and i + 1 < len(args):
            input_file = args[i + 1]
        elif arg == '-o' and i + 1 < len(args):
            output_file = args[i + 1]

    if not input_file:
        logging.error("Input file not specified")
        return

    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".glb"

    logging.info(f"Input file: {input_file}")
    logging.info(f"Output file: {output_file}")

    # Clear all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import SVG file
    logging.info("Importing SVG file")
    bpy.ops.import_curve.svg(filepath=input_file)

    # Select all imported curve objects
    curve_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'CURVE']
    
    if not curve_objects:
        logging.error("No curve objects were imported from the SVG file")
        return

    logging.info(f"Number of imported curve objects: {len(curve_objects)}")

    # Select all curve objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in curve_objects:
        obj.select_set(True)

    # Set curves to no fill
    logging.info("Setting curves to no fill")
    for obj in curve_objects:
        logging.info(f"Processing object: {obj.name}, Type: {obj.type}")
        logging.info(f"Current fill mode: {obj.data.fill_mode}")
        try:
            obj.data.fill_mode = 'NONE'
            logging.info("Fill mode set to NONE")
        except Exception as e:
            logging.error(f"Error setting fill mode: {str(e)}")
            logging.info("Available fill modes: " + ", ".join(obj.data.bl_rna.properties['fill_mode'].enum_items.keys()))

    # Join curves if there's more than one
    if len(curve_objects) > 1:
        logging.info("Joining curves")
        bpy.context.view_layer.objects.active = curve_objects[0]  # Set the active object
        bpy.ops.object.join()
    else:
        logging.info("Only one curve object, skipping join operation")

    # Add geometry nodes modifier
    logging.info("Adding geometry nodes modifier")
    bpy.ops.object.modifier_add(type='NODES')

    # Set lod_logo_length
    logging.info("Setting lod_logo_length")
    node_group = bpy.data.node_groups.get("lod_logo_count")
    if node_group:
        bpy.context.object.modifiers["GeometryNodes"].node_group = node_group
        if "Socket_1" in bpy.context.object.modifiers["GeometryNodes"]:
            bpy.context.object.modifiers["GeometryNodes"]["Socket_1"] = 0.001
        else:
            logging.warning("Socket_1 not found in GeometryNodes modifier")
    else:
        logging.warning("Node group 'lod_logo_length' not found")

    # Convert to mesh
    logging.info("Converting to mesh")
    bpy.ops.object.convert(target='MESH')

    # Set top view
    logging.info("Setting top view")
    if not ensure_top_view():
        logging.warning("Failed to set top view")

    # UV unwrap
    logging.info("UV unwrapping")
    if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
        ensure_top_view()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        if not uv_project_from_view():
            logging.error("Failed to UV unwrap using project_from_view")
        
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        logging.error("No active mesh object for UV unwrapping")

    # Create new material
    logging.info("Creating new material")
    material = bpy.data.materials.new(name="Logo Material")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Set blend mode to OPAQUE
    logging.info("Setting blend mode to OPAQUE")
    material.blend_method = 'OPAQUE'
    logging.info(f"Material blend method set to: {material.blend_method}")
    
    # Add Image Texture node
    logging.info("Adding Image Texture node")
    image_texture = nodes.new(type="ShaderNodeTexImage")
    
    # Connect Image Texture to Principled BSDF
    logging.info("Connecting Image Texture to Principled BSDF")
    principled_bsdf = nodes.get("Principled BSDF")
    if principled_bsdf:
        links.new(image_texture.outputs["Color"], principled_bsdf.inputs["Base Color"])
        links.new(image_texture.outputs["Alpha"], principled_bsdf.inputs["Alpha"])
    else:
        logging.error("Principled BSDF node not found in the material")
    
    # Assign material to object
    logging.info("Assigning material to object")
    obj = bpy.context.active_object
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
    
    # Convert SVG to PNG using ImageMagick
    logging.info("Converting SVG to PNG using ImageMagick")
    png_file = os.path.splitext(input_file)[0] + ".png"
    subprocess.run(["convert", "-background", "none", "-trim", "-resize", "2048x2048!", input_file, png_file], check=True)
    
    # Load the PNG as an image texture
    logging.info("Loading PNG as image texture")
    image = bpy.data.images.load(png_file)
    image_texture.image = image
    image.alpha_mode = 'NONE'
    logging.info(f"Image alpha mode set to: {image.alpha_mode}")
    
    # Merge by distance
    logging.info("Merging by distance")
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')

    # Export as GLB
    logging.info("Exporting as GLB")
    bpy.ops.export_scene.gltf(filepath=output_file, export_format='GLB')

    # Clean up scene
    logging.info("Cleaning up scene")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    logging.info(f"Exported to {output_file}")
    logging.info("Script completed")

if __name__ == "__main__":
    main()
