# SciViz Star Projects

Flagship scientific visualization projects focused on **deterministic, performant pipelines** bridging OVITO/LAMMPS data to Blender for real-time inspection and production-grade rendering.

<p align="center">
  <img src="docs/media/recocido_480.gif" alt="Simulated annealing: OVITO dump → Blender Geometry Nodes instancing" width="480"/>
</p>

## Why
Scientists need **physically faithful** previews and **stable renders**. We avoid re-simulation inside Blender: we ingest ground-truth positions from OVITO/LAMMPS, instance geometry via Geometry Nodes, and—when rendering—use **point caches (PC2/Alembic)** for deterministic playback.

## Repository Layout
projects/
└─ ovito-blender-visualizer/     # OVITO/LAMMPS dump → Blender GN instancing + PC2/Alembic bake
docs/
└─ media/                         # demo GIFs and gallery stills
## Features (engineering-grade)
- **Real-time viewport playback** from multi-frame dumps.
- **Render-safe determinism** via PC2/Alembic + Mesh Cache (Time Mode = FRAME).
- **Geometry Nodes instancing**: replace the atom prototype with any object (spheres, icosahedra, molecules).
- **Shape/scale control** per instance; optional filtering by LAMMPS `type`.
- **Cycles-ready**: supports motion blur (enable Deformation MB), metal backend stability notes for macOS.
- **Production hygiene**: pre-commit (`black`, `flake8`), protected `main`, CODEOWNERS, CI hooks.

## Quickstart
1. Open Blender 3.6+.
2. Load `projects/ovito-blender-visualizer/` script into the Text Editor.
3. Set your dump path (LAMMPS/OVITO). Run the script.
4. Replace **`Atom_Proto`** with your own prototype object if desired; adjust atom scale in GN.
5. Viewport: press Play. Render: bake to PC2/Alembic and attach **Mesh Cache** for deterministic frames.

## Determinism & Point Cache (PC2)
- **PC2 (Point Cache 2)** is a per-frame binary cache of vertex positions. It removes Python/handlers from the render loop.
- Use **Alembic** as an alternative (interchange, stable on DCCs).
- Recommended render path:
  1) Generate carrier mesh (N vertices = N particles).  
  2) Bake PC2/Alembic.  
  3) Attach **Mesh Cache** (Time Mode = FRAME).  
  4) Keep GN *after* Mesh Cache to instance the prototype at baked positions.

## Performance Tips
- Large systems → prefer PC2/Alembic for render.  
- Lower GN draw cost using simpler prototypes (e.g., low-poly spheres).  
- If using GIFs in docs, keep ≤ 10–20 MB (decimate frames, 12 fps, 480–360 px, limited palette).

## Contributing
- Branch from `main`, push feature branches, open PRs.  
- Linting: `pre-commit run --all-files`.  
- Protected `main`: at least 1 CODEOWNER review required.

## License
MIT. See `LICENSE`.

## Acknowledgments
Inspired by OVITO and Blender communities; tailored for scientific graphics pipelines.
