# STORYTELLER (cycle-01)

## The creative/quality thread
This is a “restoration” story: we take a raw scan (truthful but rough) and return it to something that looks **intentional**, like it came off a designer’s bench rather than a point cloud.

The top rim is the hero feature. It’s the part the eye reads first (silhouette, highlight line, tactile feel), and it’s the part most punished by scan faceting. Our narrative: **preserve function, elevate finish**.

## Translate “nice smooth curves” into acceptance criteria
Define success in ways that can be checked.

### 1) What exactly is “top rim”
- The continuous upper edge/loop of the object: the boundary you would run your finger around at the top.
- Operationally for editing/measurement: a “rim band” defined as the topmost region between **Z = Zmax down to Z = Zmax - (band height)**, where band height will be chosen after inspecting the scan (typical starting guess: 3–8 mm depending on scale).

### 2) What “smooth” means (observable)
- **Visual continuity**: in renders, the highlight along the rim should form a continuous, even line without chatter/facets.
- **Geometric continuity**:
  - Reduce high-frequency surface noise on the rim band.
  - Rim edge should be close to circular/consistent curvature unless the photo shows a deliberate shape variation.
- **Printability**: no razor-thin spikes, self-intersections, or non-manifold edges introduced by smoothing.

### 3) Preservation of the object’s “identity”
- The revised rim should not “melt” the design: keep the rim’s overall profile (height and thickness) consistent with the scan.
- Suggestion for tolerance target (to be confirmed by Orchestrator/Core worker after measuring):
  - **Rim surface deviation** from scan: aim for ≤ 0.5–1.0 mm average, with controlled exceptions where scan noise is clearly erroneous.

## Reference use: the photo
The photo is not a measuring tool; it’s a style judge.
- Use it to confirm whether the rim is intended to be round, elliptical, or has a specific lip/flare.
- Use it to judge edge sharpness: is it a soft roll-over (fillet) or a crisp edge.

## Deliverables I expect downstream
- Before/after visuals (at least 2 angles) emphasizing the rim highlight.
- A short “rim band” description (how it was selected) so future cycles can iterate.
- A single improved STL that is watertight/manifold.

## Guidance to Orchestrator
Add explicit checks to the plan:
- Rim band definition recorded (Z-range or vertex selection criteria).
- Validation report required (watertight/manifold, bounding box, triangle count).
- Keep a copy of the original scan STL in outputs for comparison (no modifications-in-place).
