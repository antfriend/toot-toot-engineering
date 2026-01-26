# SOLUTION

## Assets
- `deliverables/cycle-03/lighting-demo-animated.html`

## Approach
The lighting demo extends the CSS overlays from cycle-02 with subtle animation: slow light flicker on bloom layers and drifting dust motes. The SVG artwork remains unchanged and is embedded inline for consistent compositing.

## Motion design notes
- Light flicker uses low-amplitude opacity animation to suggest passing clouds.
- Dust motes drift diagonally with gentle vertical bobbing.
- Animation durations range from 12s to 24s to avoid obvious looping.
- A reduced-motion media query disables animation for sensitive users.

## How to view
Open `deliverables/cycle-03/lighting-demo-animated.html` in a modern browser.
