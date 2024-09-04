import bpy
import math

# Очистка сцены
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Создание куба
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object

# Создание материала
material = bpy.data.materials.new(name="Chrome")
material.use_nodes = True
nodes = material.node_tree.nodes

# Очистка существующих нодов
for node in nodes:
    nodes.remove(node)

# Создание нодов для хромированного материала
node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
node_principled.inputs['Metallic'].default_value = 1.0
node_principled.inputs['Roughness'].default_value = 0.1
node_principled.location = (0, 0)

node_output = nodes.new(type='ShaderNodeOutputMaterial')
node_output.location = (300, 0)

# Соединение нодов
links = material.node_tree.links
link = links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])

# Назначение материала кубу
cube.data.materials.append(material)

# Создание HDRI окружения
world = bpy.context.scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_links = world.node_tree.links

# Очистка существующих нодов мира
for node in world_nodes:
    world_nodes.remove(node)

# Добавление HDRI текстуры
node_env = world_nodes.new(type='ShaderNodeTexEnvironment')
node_env.image = bpy.data.images.load("//path_to_your_hdri.hdr")  # Замените на путь к вашему HDRI файлу
node_env.location = (-300, 0)

node_background = world_nodes.new(type='ShaderNodeBackground')
node_background.location = (0, 0)

node_output = world_nodes.new(type='ShaderNodeOutputWorld')
node_output.location = (300, 0)

# Соединение нодов мира
world_links.new(node_env.outputs['Color'], node_background.inputs['Color'])
world_links.new(node_background.outputs['Background'], node_output.inputs['Surface'])

# Настройка анимации
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120  # 5 секунд при 24 кадрах в секунду

cube.animation_data_create()
cube.animation_data.action = bpy.data.actions.new(name="CubeRotation")

# Анимация вращения по X
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=1)
cube.rotation_euler = (2 * math.pi, 2 * math.pi, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=120)

# Настройка интерполяции для плавного цикла
for fcurve in cube.animation_data.action.fcurves:
    for kf in fcurve.keyframe_points:
        kf.interpolation = 'LINEAR'

# Настройка камеры
bpy.ops.object.camera_add(location=(0, -5, 0))
camera = bpy.context.active_object
camera.rotation_euler = (math.pi/2, 0, 0)

# Установка активной камеры
bpy.context.scene.camera = camera

# Настройка циклического воспроизведения анимации
bpy.context.scene.render.fps = 24
bpy.context.scene.frame_end = 120
bpy.context.scene.frame_current = 1

print("Looping chrome cube animation setup complete!")
