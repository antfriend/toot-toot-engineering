# IMAGE_ASSETS (cycle-01)

## Generated assets
- `deliverables/cycle-01/assets/frames/earth_frame_00.svg` through `earth_frame_23.svg`
  - 24-frame sequence, 1920x804 (2.39:1)
  - Stylized Earth with shifting surface bands to simulate rotation
  - Static deep-space starfield background
- `deliverables/cycle-01/assets/frames_png/earth_frame_00.png` through `earth_frame_23.png`
  - Rasterized from SVG at 960px width for GIF assembly
- `deliverables/cycle-01/assets/earth_palette.png`
  - Palette generated from PNG frames for GIF compression
- `deliverables/cycle-01/assets/banner/hello-world-banner.svg`
  - Cinematic banner source with visible \"HELLO WORLD!\" text
- `deliverables/cycle-01/assets/banner/hello-world-banner.png`
  - Rasterized banner used for the final GIF

## How they were generated
- Used a small Perl script to procedurally create SVG frames with a consistent starfield and a clipped Earth surface texture that shifts each frame.
- Rasterized SVG frames with Inkscape and built a GIF palette using ffmpeg.
- Designed a new banner SVG and rasterized it with Inkscape before GIF encoding.

## Usage notes
- These SVG frames are intended as source plates for rasterization into GIF frames.
- The PNG frames and palette are used to assemble `earth-rotate.gif`.
- The banner and logo are not yet composited; Core worker can add them during GIF assembly.

## Sources
- No third-party assets used; all elements are procedurally generated.
