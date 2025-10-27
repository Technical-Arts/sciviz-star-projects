# OVITO → Blender Visualizer

**Goal:** turn OVITO/LAMMPS dumps into **real-time viewport playback** and **deterministic renders** in Blender using Geometry Nodes + PC2/Alembic.

<p align="center">
  <img src="../../docs/media/recocido_480.gif" alt="Annealing demo: GN instancing over per-frame positions" width="480"/>
</p>

## Pipeline
1. **Ingest** OVITO/LAMMPS dump (multi-frame). Typical header: `ITEM: ATOMS id type xs ys zs …`.
2. **Carrier mesh**: one vertex per particle; updated per frame.
3. **GN instancing**: Mesh → Mesh to Points → Instance on Points (Object Info = prototype).
4. **Optional bake**: export **PC2** or **Alembic**; attach **Mesh Cache** (Time Mode = FRAME) for render determinism.

## Requirements
- Blender 3.6+  
- Cycles/Eevee (Cycles recommended for metals)  
- Optional: OVITO for preprocessing; FFmpeg for docs media

## Usage (script)
- Set `OBJ_NAME` (carrier), `PROTO_NAME` (prototype), `GN_NAME`, `MOD_NAME`.  
- Ensure the dump path is correct.  
- Run the script: it creates/cleans the GN group, disables legacy dupli-verts, and wires instancing.  
- **Prototype**: replace `Atom_Proto` with any mesh; hide it (viewport/render) without affecting instances.  
- **Scale**: adjust in GN (AtomScale) or at prototype object level.  
- **Type filtering**: optionally restrict LAMMPS `type` set.

## Rendering
- **Deterministic path**:
  - Export **PC2/Alembic**, then load via **Mesh Cache** (FRAME).  
  - Keep GN **after** Mesh Cache in the stack.  
  - Enable **Deformation Motion Blur** in Cycles if you need MB.  
- **Viewport-only** is fine for inspection; for production renders use the baked cache.

## Gallery
**Initial snapshot (frame 0)**  
![atoms1](../../docs/media/atoms1.png)

**Later snapshot (post-anneal)**  
![atoms2](../../docs/media/atoms2.png)

**Prototype sphere (instanced atom)**  
![atoms3](../../docs/media/atoms3.png)

## Troubleshooting
- **Metal (macOS) warnings** about uniform re-mapping: benign; ensure GN follows Mesh Cache.  
- **Crashes on render**: avoid modifying geometry during render; prefer PC2/Alembic.  
- **Handlers duplicados**: remove previous `frame_change_*` handlers before adding new ones.

## Roadmap
- Per-type material mapping, per-particle radius, clustering overlays, Alembic/PC2 export helpers.

## License
MIT
