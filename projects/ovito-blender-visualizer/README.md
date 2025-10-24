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
## Demo — Annealing playback

<video src="../../docs/media/recocido_720p.mp4"
       width="720"
       autoplay
       loop
       muted
       playsinline
       controls></video>

<p>
  <a href="../../docs/media/recocido_720p.mp4">
    <img src="../../docs/media/recocido_poster.jpg" alt="Annealing animation (click to open video)">
  </a>
</p>
