# =============================================================================
# OVITO dump → Blender viewport animation (Dupli-Verts + handler)
# =============================================================================

import bpy

# -----------------------------------------------------------------------------
# Cleanup: objects, meshes, handlers
# -----------------------------------------------------------------------------
old_obj = bpy.data.objects.get("AtomInstancer")
if old_obj:
    bpy.data.objects.remove(old_obj, do_unlink=True)

old_sphere = bpy.data.objects.get("AtomSphere_Template")
if old_sphere:
    bpy.data.objects.remove(old_sphere, do_unlink=True)

old_mesh = bpy.data.meshes.get("AtomInstancer_Mesh")
if old_mesh:
    bpy.data.meshes.remove(old_mesh, do_unlink=True)

old_mesh2 = bpy.data.meshes.get("AtomSphere_Mesh")
if old_mesh2:
    bpy.data.meshes.remove(old_mesh2, do_unlink=True)

for h in bpy.app.handlers.frame_change_pre[:]:
    if h.__name__ == "update_atoms":
        bpy.app.handlers.frame_change_pre.remove(h)

# -----------------------------------------------------------------------------
# Read LAMMPS multi-frame dump (OVITO format)
# -----------------------------------------------------------------------------
ruta_archivo = "/ruta/a/simulacion.dump"  # <-- set your path
positions = {}  # frame -> [(x,y,z), ...]
frame_list = []

with open(ruta_archivo, "r") as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    if lines[i].startswith("ITEM: TIMESTEP"):
        frame = int(lines[i + 1].strip())
        frame_list.append(frame)

        i += 2
        if not lines[i].startswith("ITEM: NUMBER OF ATOMS"):
            print("Unexpected format: expected NUMBER OF ATOMS at line", i)
        num_atoms = int(lines[i + 1].strip())

        i += 3
        if lines[i].startswith("ITEM: BOX BOUNDS"):
            xlo, xhi = map(float, lines[i + 1].split())
            ylo, yhi = map(float, lines[i + 2].split())
            zlo, zhi = map(float, lines[i + 3].split())
            i += 4

        if not lines[i].startswith("ITEM: ATOMS"):
            print("Unexpected format: expected ATOMS at line", i)
        header = lines[i].split()[2:]

        use_scaled = False
        if "x" in header and "y" in header and "z" in header:
            ix, iy, iz = header.index("x"), header.index("y"), header.index("z")
        elif "xs" in header and "ys" in header and "zs" in header:
            ix, iy, iz = header.index("xs"), header.index("ys"), header.index("zs")
            use_scaled = True
        else:
            raise ValueError("No x/y/z or xs/ys/zs fields in header")

        i += 1
        coords = []
        for a in range(num_atoms):
            cols = lines[i + a].split()
            x, y, z = float(cols[ix]), float(cols[iy]), float(cols[iz])
            if use_scaled:
                x = x * (xhi - xlo) + xlo
                y = y * (yhi - ylo) + ylo
                z = z * (zhi - zlo) + zlo
            coords.append((x, y, z))
        positions[frame] = coords
        i += num_atoms
    else:
        i += 1

# -----------------------------------------------------------------------------
# Timeline
# -----------------------------------------------------------------------------
scene = bpy.context.scene
if frame_list:
    scene.frame_start = min(frame_list)
    scene.frame_end = max(frame_list)
scene.render.use_lock_interface = True

# -----------------------------------------------------------------------------
# Build instancer mesh (one vertex per atom)
# -----------------------------------------------------------------------------
mesh = bpy.data.meshes.new("AtomInstancer_Mesh")
base_obj = bpy.data.objects.new("AtomInstancer", mesh)
bpy.context.collection.objects.link(base_obj)

first_frame = scene.frame_start
if first_frame in positions:
    mesh.from_pydata(positions[first_frame], [], [])
else:
    mesh.from_pydata([(0, 0, 0)], [], [])
mesh.update()

base_obj.instance_type = "VERTS"

# -----------------------------------------------------------------------------
# Prototype sphere (child of instancer)
# -----------------------------------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, segments=16, ring_count=8)
sphere = bpy.context.object
sphere.name = "AtomSphere_Template"
sphere.data.name = "AtomSphere_Mesh"

mat = bpy.data.materials.new("AtomMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
sphere.data.materials.append(mat)

sphere.parent = base_obj
sphere.location = (0, 0, 0)

base_obj.hide_viewport = True
base_obj.hide_render = True


# -----------------------------------------------------------------------------
# Frame handler: update atom positions
# -----------------------------------------------------------------------------
def update_atoms(scene):
    frame = scene.frame_current
    if frame not in positions:
        return
    coords = positions[frame]
    me = base_obj.data
    if len(me.vertices) != len(coords):
        me.clear_geometry()
        me.from_pydata(coords, [], [])
        me.update()
        return
    for idx, v in enumerate(me.vertices):
        v.co = coords[idx]
    me.update()


bpy.app.handlers.frame_change_pre.append(update_atoms)
