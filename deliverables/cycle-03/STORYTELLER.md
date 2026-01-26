# STORYTELLER

## Core interpretation
The window now breathes: light subtly flickers as if filtered through passing clouds, and dust motes drift in the beam. The motion should be barely perceptible, enhancing atmosphere without distracting from the glasswork.

## Narrative focus
- Motion is slow and delicate; think chapel quiet, not stage lighting.
- Dust motes are sparse, drifting diagonally with slight parallax.
- The light bloom pulses gently, as if the sun shifts behind thin clouds.

## Visual beats
1. A soft rhythmic glow in the upper-left to reinforce directional light.
2. Sporadic dust motes that catch the light near the window edges.
3. A subtle ambient shimmer across the glass, barely visible.

## Direction for CSS execution
- Use low-amplitude keyframe animations on light overlays.
- Keep particle count low; reuse CSS pseudo-elements or a few divs.
- Provide a reduced-motion fallback to disable animation.

## Success criteria
- Motion feels natural and subdued.
- Performance stays smooth on typical laptops.
- Reduced-motion users see a static, polished version.
