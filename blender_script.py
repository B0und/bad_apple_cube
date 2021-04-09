import bpy
import numpy as np
import glob

# Global consts
WIDTH = 160
HEIGHT = 120
PROJECT_PATH = "/PATH/TO/bad_apple_blender_cube"
FRAME_COUNT = len(glob.glob(f'{PROJECT_PATH}/frames/*.jpg'))


# Prepare particle system
cube = bpy.data.objects["Cube"]
degp = bpy.context.evaluated_depsgraph_get()
particle_systems = cube.evaluated_get(degp).particle_systems

particle_systems[0].settings.count = WIDTH * HEIGHT
particle_systems[0].settings.lifetime = 99999
particle_systems[0].settings.frame_start = -1
particle_systems[0].settings.frame_end = 1
particle_systems[0].settings.emit_from = 'VOLUME'
particle_systems[0].settings.physics_type = 'NO'
particle_systems[0].settings.render_type = 'OBJECT'
particle_systems[0].settings.instance_object = cube
particle_systems[0].settings.particle_size = 1.0

# reset particle locations
particles = particle_systems[0].particles
total_particles = len(particles)
flat_list = [0]*(3*total_particles)
particles.foreach_set("location", flat_list)

# load all locations into memory
locations_arr = np.zeros(shape=(FRAME_COUNT, WIDTH*HEIGHT*3))
for i in range(FRAME_COUNT):
    temp_arr = np.load(
        f"{PROJECT_PATH}/locations/{i}.npy")
    locations_arr[i] = temp_arr


def particles_location_setter(scene, degp):
    """
        Set particle locations to a flat numpy array
    """
    particle_systems = cube.evaluated_get(degp).particle_systems
    particles = particle_systems[0].particles

    current_frame = scene.frame_current
    particles.foreach_set("location", locations_arr[current_frame])


# clear the post frame handler
bpy.app.handlers.frame_change_post.clear()

# run the function on each frame
bpy.app.handlers.frame_change_post.append(particles_location_setter)
