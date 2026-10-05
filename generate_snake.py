import json
import os

with open('/tmp/contribs.json', 'r') as f:
    data = json.load(f)

contributions = data.get('contributions', [])

# 53 columns, 7 rows
# Grid coordinates
cell_size = 11
gap = 4
pitch = cell_size + gap
start_x = 25
start_y = 25

colors = {
    0: '#161b22',
    1: '#0e4429',
    2: '#006d32',
    3: '#26a641',
    4: '#39d353'
}

rects = []
cols = 53
rows = 7

# Calculate paths for the snake
# Snake will crawl across the active contribution days and loop
active_points = []

for idx, day in enumerate(contributions):
    col = idx // rows
    row = idx % rows
    if col >= cols:
        break
    x = start_x + col * pitch
    y = start_y + row * pitch
    level = day.get('level', 0)
    color = colors.get(level, '#161b22')
    rects.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" ry="2" fill="{color}" />')
    if level > 0:
        active_points.append((x + cell_size/2, y + cell_size/2))

# Build a smooth serpentine path for the animated snake
path_d_parts = []
# Start at top left
current_x = start_x + cell_size/2
current_y = start_y + cell_size/2
path_d_parts.append(f"M {current_x} {current_y}")

# Snake traverse pattern across the board
for c in range(0, cols, 2):
    x1 = start_x + c * pitch + cell_size/2
    y_bottom = start_y + 6 * pitch + cell_size/2
    path_d_parts.append(f"L {x1} {y_bottom}")
    if c + 1 < cols:
        x2 = start_x + (c + 1) * pitch + cell_size/2
        y_top = start_y + cell_size/2
        path_d_parts.append(f"L {x2} {y_bottom}")
        path_d_parts.append(f"L {x2} {y_top}")

# Return back along the top
path_d_parts.append(f"L {start_x + cell_size/2} {start_y + cell_size/2} Z")
snake_path = " ".join(path_d_parts)

width = start_x * 2 + cols * pitch
height = start_y * 2 + rows * pitch + 15

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <linearGradient id="scanner-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00FF66" stop-opacity="0" />
      <stop offset="50%" stop-color="#00FF66" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#00FF66" stop-opacity="0" />
    </linearGradient>
    <path id="snake-track" d="{snake_path}" fill="none" />
  </defs>

  <style>
    .bg {{ fill: #0D1117; stroke: #238636; stroke-width: 1.5; rx: 6px; }}
    .cell {{ transition: all 0.3s; }}
    .grid-label {{ font-family: monospace; font-size: 11px; fill: #7EE787; }}
    .subtext {{ font-family: monospace; font-size: 10px; fill: #00FF66; }}
    
    /* CRT Scanline effect */
    @keyframes scan {{
      0% {{ transform: translateX(-150px); }}
      100% {{ transform: translateX({width + 100}px); }}
    }}
    .scanner {{
      animation: scan 6s linear infinite;
    }}
    
    /* Snake pulsing tail */
    @keyframes pulse {{
      0%, 100% {{ r: 5.5px; opacity: 1; }}
      50% {{ r: 7px; opacity: 0.8; }}
    }}
    .snake-head {{
      fill: #00FF66;
      filter: url(#neon-glow);
      animation: pulse 1.5s ease-in-out infinite;
    }}
  </style>

  <!-- Background terminal box -->
  <rect class="bg" x="1" y="1" width="{width - 2}" height="{height - 2}" />

  <!-- CRT radar sweep line -->
  <rect class="scanner" y="2" width="120" height="{height - 4}" fill="url(#scanner-grad)" opacity="0.6" />

  <!-- Contribution cells -->
  <g>
    {''.join(rects)}
  </g>

  <!-- Snake Body Segments (Motion along the grid path) -->
  <!-- Segment 4 (Tail) -->
  <circle r="3.5" fill="#00AA44" opacity="0.6">
    <animateMotion dur="28s" repeatCount="indefinite" begin="-0.45s">
      <mpath href="#snake-track" />
    </animateMotion>
  </circle>

  <!-- Segment 3 -->
  <circle r="4" fill="#00DD55" opacity="0.8">
    <animateMotion dur="28s" repeatCount="indefinite" begin="-0.3s">
      <mpath href="#snake-track" />
    </animateMotion>
  </circle>

  <!-- Segment 2 -->
  <circle r="4.5" fill="#39d353" opacity="0.9">
    <animateMotion dur="28s" repeatCount="indefinite" begin="-0.15s">
      <mpath href="#snake-track" />
    </animateMotion>
  </circle>

  <!-- Segment 1 (Head with neon glow) -->
  <circle class="snake-head" r="5.5">
    <animateMotion dur="28s" repeatCount="indefinite">
      <mpath href="#snake-track" />
    </animateMotion>
  </circle>

  <!-- Terminal Diagnostics Label at bottom -->
  <text class="grid-label" x="25" y="{height - 7}">[SYS_DIAG: 71 CONTRIBUTIONS LOGGED]</text>
  <text class="subtext" x="{width - 250}" y="{height - 7}">● SENSOR: SNAKE_RADAR_ACTIVE</text>
</svg>
'''

os.makedirs('/Users/mohamedabdelgawad/Desktop/gh/assets', exist_ok=True)
with open('/Users/mohamedabdelgawad/Desktop/gh/assets/github-contribution-grid-snake.svg', 'w') as f:
    f.write(svg_content)

with open('/Users/mohamedabdelgawad/Desktop/gh/assets/github-contribution-grid-snake-dark.svg', 'w') as f:
    f.write(svg_content)

print(f"Generated snake SVG: width={width}, height={height}")
