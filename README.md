# OVITO → Blender Visualizer (PC2 + Dupli-Verts)

**Goal:** Play OVITO/LAMMPS dumps in Blender 3.6 with per-frame updates, using a vertex instancer and a template sphere.  
**File:** `blender/ovito_viewport_anim.py`

## Features
- Reads multi-frame LAMMPS dump (OVITO format).
- Builds one-vertex-per-atom mesh and instances a template object.
- Updates vertices per frame; playback in viewport.
- Lock interface during render to avoid instability.

## Requirements
- Blender 3.6
- A LAMMPS/OVITO dump file with `ITEM:` headers.

## Quickstart
1. Open Blender → Scripting → load `blender/ovito_viewport_anim.py`.
2. Set `ruta_archivo` to your dump path.
3. Run script. Play timeline.

## Notes
- This script focuses on viewport animation. For stable Cycles renders, bake to PC2 and instance via Geometry Nodes in a separate step.
- License: GPL-3.0-or-later.
